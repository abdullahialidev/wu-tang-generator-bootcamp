#!/usr/bin/env python3
"""
Tennis Betting Analysis System
Comprehensive analysis of tennis matches including fatigue, surface, and player props
"""

import json
import requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import time
import sqlite3
import logging
from collections import defaultdict
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PlayerStats:
    """Player statistics and metrics"""
    name: str
    ranking: int
    age: int
    country: str
    height: int  # cm
    weight: int  # kg
    plays: str  # R/L
    prize_money: float
    
    # Surface-specific records
    hard_wins: int = 0
    hard_losses: int = 0
    clay_wins: int = 0
    clay_losses: int = 0
    grass_wins: int = 0
    grass_losses: int = 0
    
    # Service stats
    aces_per_match: float = 0.0
    double_faults_per_match: float = 0.0
    first_serve_percentage: float = 0.0
    first_serve_win_percentage: float = 0.0
    second_serve_win_percentage: float = 0.0
    service_games_won_percentage: float = 0.0
    
    # Return stats
    break_points_converted: float = 0.0
    break_points_saved: float = 0.0
    return_games_won_percentage: float = 0.0
    
    # Form and fatigue
    recent_matches: List[Dict] = None
    days_since_last_match: int = 0
    matches_last_7_days: int = 0
    matches_last_14_days: int = 0
    sets_played_last_14_days: int = 0
    
    # Head-to-head
    h2h_wins: int = 0
    h2h_losses: int = 0

@dataclass
class MatchPrediction:
    """Match prediction with analysis"""
    player1: str
    player2: str
    surface: str
    tournament: str
    round: str
    
    # Predictions
    winner_prediction: str
    confidence: float
    set_prediction: str
    
    # Analysis factors
    surface_advantage: Dict[str, float]
    fatigue_factor: Dict[str, float]
    form_factor: Dict[str, float]
    h2h_factor: Dict[str, float]
    
    # Player props
    double_fault_props: Dict[str, Dict]
    break_props: Dict[str, Dict]
    aces_props: Dict[str, Dict]
    
    # Final recommendation
    recommended_bets: List[str]
    risk_level: str

class TennisAnalyzer:
    def __init__(self):
        self.setup_database()
        self.surface_factors = {
            'hard': {'speed': 'medium', 'bounce': 'medium'},
            'clay': {'speed': 'slow', 'bounce': 'high'},
            'grass': {'speed': 'fast', 'bounce': 'low'},
            'indoor_hard': {'speed': 'fast', 'bounce': 'medium'}
        }
        
    def setup_database(self):
        """Initialize SQLite database for storing match data"""
        self.conn = sqlite3.connect('tennis_data.db')
        self.create_tables()
        
    def create_tables(self):
        """Create database tables"""
        cursor = self.conn.cursor()
        
        # Players table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                ranking INTEGER,
                country TEXT,
                age INTEGER,
                height INTEGER,
                weight INTEGER,
                plays TEXT,
                prize_money REAL
            )
        ''')
        
        # Matches table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY,
                date TEXT,
                tournament TEXT,
                round TEXT,
                surface TEXT,
                player1 TEXT,
                player2 TEXT,
                winner TEXT,
                score TEXT,
                duration INTEGER,
                aces_p1 INTEGER,
                aces_p2 INTEGER,
                double_faults_p1 INTEGER,
                double_faults_p2 INTEGER,
                first_serve_p1 REAL,
                first_serve_p2 REAL,
                break_points_p1 TEXT,
                break_points_p2 TEXT
            )
        ''')
        
        self.conn.commit()

    def get_upcoming_matches(self) -> List[Dict]:
        """Get tomorrow's tennis matches from various sources"""
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime('%Y-%m-%d')
        
        # Simulated upcoming matches (in real implementation, fetch from tennis APIs)
        upcoming_matches = [
            {
                'date': tomorrow_str,
                'tournament': 'Washington Open',
                'round': 'Round of 32',
                'surface': 'hard',
                'player1': 'Taylor Fritz',
                'player2': 'Ben Shelton',
                'court': 'Center Court',
                'time': '19:00'
            },
            {
                'date': tomorrow_str,
                'tournament': 'Washington Open',
                'round': 'Round of 32',
                'surface': 'hard',
                'player1': 'Alex de Minaur',
                'player2': 'Frances Tiafoe',
                'court': 'Court 1',
                'time': '21:00'
            },
            {
                'date': tomorrow_str,
                'tournament': 'Kitzbuhel Open',
                'round': 'Round of 16',
                'surface': 'clay',
                'player1': 'Casper Ruud',
                'player2': 'Sebastian Baez',
                'court': 'Center Court',
                'time': '16:00'
            },
            {
                'date': tomorrow_str,
                'tournament': 'Umag Open',
                'round': 'Quarterfinals',
                'surface': 'clay',
                'player1': 'Lorenzo Musetti',
                'player2': 'Francisco Cerundolo',
                'court': 'Stadium Court',
                'time': '18:00'
            }
        ]
        
        return upcoming_matches

    def get_player_stats(self, player_name: str) -> PlayerStats:
        """Get comprehensive player statistics"""
        # Simulated player data (in real implementation, fetch from tennis databases)
        player_data = {
            'Taylor Fritz': {
                'ranking': 7, 'age': 27, 'country': 'USA', 'height': 196, 'weight': 88, 'plays': 'R',
                'hard_wins': 45, 'hard_losses': 12, 'clay_wins': 8, 'clay_losses': 15, 'grass_wins': 12, 'grass_losses': 6,
                'aces_per_match': 12.5, 'double_faults_per_match': 2.8, 'first_serve_percentage': 65.2,
                'first_serve_win_percentage': 75.8, 'second_serve_win_percentage': 55.4,
                'break_points_converted': 42.1, 'break_points_saved': 68.9,
                'days_since_last_match': 5, 'matches_last_7_days': 0, 'matches_last_14_days': 3
            },
            'Ben Shelton': {
                'ranking': 8, 'age': 22, 'country': 'USA', 'height': 193, 'weight': 86, 'plays': 'L',
                'hard_wins': 38, 'hard_losses': 15, 'clay_wins': 5, 'clay_losses': 12, 'grass_wins': 8, 'grass_losses': 4,
                'aces_per_match': 15.2, 'double_faults_per_match': 4.1, 'first_serve_percentage': 62.8,
                'first_serve_win_percentage': 78.9, 'second_serve_win_percentage': 52.3,
                'break_points_converted': 38.7, 'break_points_saved': 62.4,
                'days_since_last_match': 8, 'matches_last_7_days': 0, 'matches_last_14_days': 2
            },
            'Alex de Minaur': {
                'ranking': 10, 'age': 25, 'country': 'AUS', 'height': 183, 'weight': 75, 'plays': 'R',
                'hard_wins': 42, 'hard_losses': 18, 'clay_wins': 12, 'clay_losses': 20, 'grass_wins': 15, 'grass_losses': 8,
                'aces_per_match': 4.8, 'double_faults_per_match': 1.9, 'first_serve_percentage': 68.1,
                'first_serve_win_percentage': 71.2, 'second_serve_win_percentage': 58.9,
                'break_points_converted': 47.3, 'break_points_saved': 71.8,
                'days_since_last_match': 6, 'matches_last_7_days': 0, 'matches_last_14_days': 3
            },
            'Frances Tiafoe': {
                'ranking': 29, 'age': 26, 'country': 'USA', 'height': 188, 'weight': 86, 'plays': 'R',
                'hard_wins': 35, 'hard_losses': 22, 'clay_wins': 8, 'clay_losses': 18, 'grass_wins': 6, 'grass_losses': 9,
                'aces_per_match': 8.9, 'double_faults_per_match': 3.2, 'first_serve_percentage': 64.7,
                'first_serve_win_percentage': 73.1, 'second_serve_win_percentage': 54.8,
                'break_points_converted': 41.2, 'break_points_saved': 65.9,
                'days_since_last_match': 4, 'matches_last_7_days': 1, 'matches_last_14_days': 4
            },
            'Casper Ruud': {
                'ranking': 9, 'age': 25, 'country': 'NOR', 'height': 183, 'weight': 79, 'plays': 'R',
                'hard_wins': 28, 'hard_losses': 18, 'clay_wins': 48, 'clay_losses': 12, 'grass_wins': 4, 'grass_losses': 8,
                'aces_per_match': 6.2, 'double_faults_per_match': 2.1, 'first_serve_percentage': 66.9,
                'first_serve_win_percentage': 69.8, 'second_serve_win_percentage': 56.7,
                'break_points_converted': 44.8, 'break_points_saved': 69.2,
                'days_since_last_match': 3, 'matches_last_7_days': 2, 'matches_last_14_days': 5
            },
            'Sebastian Baez': {
                'ranking': 30, 'age': 23, 'country': 'ARG', 'height': 170, 'weight': 68, 'plays': 'R',
                'hard_wins': 18, 'hard_losses': 15, 'clay_wins': 32, 'clay_losses': 14, 'grass_wins': 2, 'grass_losses': 6,
                'aces_per_match': 3.1, 'double_faults_per_match': 2.8, 'first_serve_percentage': 63.4,
                'first_serve_win_percentage': 67.9, 'second_serve_win_percentage': 52.1,
                'break_points_converted': 46.7, 'break_points_saved': 64.3,
                'days_since_last_match': 2, 'matches_last_7_days': 3, 'matches_last_14_days': 6
            },
            'Lorenzo Musetti': {
                'ranking': 6, 'age': 22, 'country': 'ITA', 'height': 185, 'weight': 76, 'plays': 'R',
                'hard_wins': 32, 'hard_losses': 16, 'clay_wins': 28, 'clay_losses': 12, 'grass_wins': 8, 'grass_losses': 6,
                'aces_per_match': 7.4, 'double_faults_per_match': 2.9, 'first_serve_percentage': 65.8,
                'first_serve_win_percentage': 72.3, 'second_serve_win_percentage': 55.9,
                'break_points_converted': 43.1, 'break_points_saved': 67.8,
                'days_since_last_match': 4, 'matches_last_7_days': 1, 'matches_last_14_days': 4
            },
            'Francisco Cerundolo': {
                'ranking': 15, 'age': 26, 'country': 'ARG', 'height': 185, 'weight': 79, 'plays': 'R',
                'hard_wins': 24, 'hard_losses': 18, 'clay_wins': 35, 'clay_losses': 15, 'grass_wins': 5, 'grass_losses': 8,
                'aces_per_match': 5.8, 'double_faults_per_match': 3.4, 'first_serve_percentage': 64.2,
                'first_serve_win_percentage': 70.1, 'second_serve_win_percentage': 53.7,
                'break_points_converted': 42.9, 'break_points_saved': 66.1,
                'days_since_last_match': 1, 'matches_last_7_days': 4, 'matches_last_14_days': 7
            }
        }
        
        if player_name in player_data:
            data = player_data[player_name]
            return PlayerStats(
                name=player_name,
                ranking=data['ranking'],
                age=data['age'],
                country=data['country'],
                height=data['height'],
                weight=data['weight'],
                plays=data['plays'],
                prize_money=0.0,
                hard_wins=data['hard_wins'],
                hard_losses=data['hard_losses'],
                clay_wins=data['clay_wins'],
                clay_losses=data['clay_losses'],
                grass_wins=data['grass_wins'],
                grass_losses=data['grass_losses'],
                aces_per_match=data['aces_per_match'],
                double_faults_per_match=data['double_faults_per_match'],
                first_serve_percentage=data['first_serve_percentage'],
                first_serve_win_percentage=data['first_serve_win_percentage'],
                second_serve_win_percentage=data['second_serve_win_percentage'],
                break_points_converted=data['break_points_converted'],
                break_points_saved=data['break_points_saved'],
                days_since_last_match=data['days_since_last_match'],
                matches_last_7_days=data['matches_last_7_days'],
                matches_last_14_days=data['matches_last_14_days']
            )
        
        # Default stats for unknown players
        return PlayerStats(name=player_name, ranking=100, age=25, country='UNK', 
                          height=180, weight=75, plays='R', prize_money=0.0)

    def calculate_surface_advantage(self, player1: PlayerStats, player2: PlayerStats, surface: str) -> Dict[str, float]:
        """Calculate surface-specific advantage"""
        surface_map = {
            'hard': ('hard_wins', 'hard_losses'),
            'clay': ('clay_wins', 'clay_losses'),
            'grass': ('grass_wins', 'grass_losses')
        }
        
        if surface not in surface_map:
            surface = 'hard'
        
        wins_attr, losses_attr = surface_map[surface]
        
        p1_wins = getattr(player1, wins_attr)
        p1_losses = getattr(player1, losses_attr)
        p1_win_rate = p1_wins / (p1_wins + p1_losses) if (p1_wins + p1_losses) > 0 else 0.5
        
        p2_wins = getattr(player2, wins_attr)
        p2_losses = getattr(player2, losses_attr)
        p2_win_rate = p2_wins / (p2_wins + p2_losses) if (p2_wins + p2_losses) > 0 else 0.5
        
        return {
            player1.name: p1_win_rate,
            player2.name: p2_win_rate,
            'advantage': player1.name if p1_win_rate > p2_win_rate else player2.name,
            'difference': abs(p1_win_rate - p2_win_rate)
        }

    def calculate_fatigue_factor(self, player1: PlayerStats, player2: PlayerStats) -> Dict[str, float]:
        """Calculate player fatigue based on recent matches"""
        def fatigue_score(player):
            # More matches = more fatigue
            recent_fatigue = player.matches_last_7_days * 0.3 + player.matches_last_14_days * 0.1
            
            # Rest advantage
            rest_bonus = max(0, (player.days_since_last_match - 3) * 0.1)
            
            # Too much rest can be bad (rust factor)
            if player.days_since_last_match > 14:
                rest_bonus -= 0.2
                
            return max(0, 1.0 - recent_fatigue + rest_bonus)
        
        p1_fatigue = fatigue_score(player1)
        p2_fatigue = fatigue_score(player2)
        
        return {
            player1.name: p1_fatigue,
            player2.name: p2_fatigue,
            'advantage': player1.name if p1_fatigue > p2_fatigue else player2.name,
            'difference': abs(p1_fatigue - p2_fatigue)
        }

    def analyze_player_props(self, player: PlayerStats, opponent: PlayerStats, surface: str) -> Dict[str, Dict]:
        """Analyze player prop betting opportunities"""
        props = {}
        
        # Double fault analysis
        expected_df = player.double_faults_per_match
        if surface == 'grass':
            expected_df *= 1.2  # Grass courts typically have more DFs
        elif surface == 'clay':
            expected_df *= 0.9  # Clay courts typically have fewer DFs
            
        props['double_faults'] = {
            'expected': round(expected_df, 1),
            'over_2_5': 'YES' if expected_df > 2.5 else 'NO',
            'over_3_5': 'YES' if expected_df > 3.5 else 'NO',
            'confidence': min(0.9, abs(expected_df - 3.0) * 0.3 + 0.5)
        }
        
        # Aces analysis
        expected_aces = player.aces_per_match
        if surface == 'grass':
            expected_aces *= 1.3
        elif surface == 'clay':
            expected_aces *= 0.7
            
        props['aces'] = {
            'expected': round(expected_aces, 1),
            'over_5_5': 'YES' if expected_aces > 5.5 else 'NO',
            'over_8_5': 'YES' if expected_aces > 8.5 else 'NO',
            'over_12_5': 'YES' if expected_aces > 12.5 else 'NO',
            'confidence': min(0.9, abs(expected_aces - 8.0) * 0.1 + 0.5)
        }
        
        # Break opportunities
        break_chance = (100 - opponent.break_points_saved) * player.break_points_converted / 100 / 100
        expected_breaks = break_chance * 12  # Approximate service games
        
        props['breaks'] = {
            'expected': round(expected_breaks, 1),
            'over_1_5': 'YES' if expected_breaks > 1.5 else 'NO',
            'over_2_5': 'YES' if expected_breaks > 2.5 else 'NO',
            'confidence': min(0.9, abs(expected_breaks - 2.0) * 0.2 + 0.5)
        }
        
        return props

    def predict_match(self, match: Dict) -> MatchPrediction:
        """Predict match outcome with comprehensive analysis"""
        player1_stats = self.get_player_stats(match['player1'])
        player2_stats = self.get_player_stats(match['player2'])
        
        # Surface analysis
        surface_advantage = self.calculate_surface_advantage(player1_stats, player2_stats, match['surface'])
        
        # Fatigue analysis
        fatigue_factor = self.calculate_fatigue_factor(player1_stats, player2_stats)
        
        # Form factor (simplified)
        form_factor = {
            player1_stats.name: 0.7 + (100 - player1_stats.ranking) / 200,
            player2_stats.name: 0.7 + (100 - player2_stats.ranking) / 200,
            'advantage': player1_stats.name if player1_stats.ranking < player2_stats.ranking else player2_stats.name,
            'difference': abs(player1_stats.ranking - player2_stats.ranking) / 100
        }
        
        # H2H factor (simplified)
        h2h_factor = {
            player1_stats.name: 0.5,
            player2_stats.name: 0.5,
            'advantage': 'neutral',
            'difference': 0.0
        }
        
        # Calculate overall probability
        p1_score = (surface_advantage[player1_stats.name] * 0.3 + 
                   fatigue_factor[player1_stats.name] * 0.2 + 
                   form_factor[player1_stats.name] * 0.4 + 
                   h2h_factor[player1_stats.name] * 0.1)
        
        p2_score = (surface_advantage[player2_stats.name] * 0.3 + 
                   fatigue_factor[player2_stats.name] * 0.2 + 
                   form_factor[player2_stats.name] * 0.4 + 
                   h2h_factor[player2_stats.name] * 0.1)
        
        winner_prediction = player1_stats.name if p1_score > p2_score else player2_stats.name
        confidence = abs(p1_score - p2_score)
        
        # Set prediction
        if confidence > 0.15:
            set_prediction = "2-0" if confidence > 0.25 else "2-1"
        else:
            set_prediction = "2-1"
        
        # Player props
        p1_props = self.analyze_player_props(player1_stats, player2_stats, match['surface'])
        p2_props = self.analyze_player_props(player2_stats, player1_stats, match['surface'])
        
        # Generate betting recommendations
        recommended_bets = []
        
        if confidence > 0.2:
            recommended_bets.append(f"Winner: {winner_prediction}")
        
        if confidence > 0.15:
            recommended_bets.append(f"Set Betting: {set_prediction}")
        
        # Prop bets
        for player_name, props in [(player1_stats.name, p1_props), (player2_stats.name, p2_props)]:
            if props['aces']['confidence'] > 0.7:
                if props['aces']['over_8_5'] == 'YES':
                    recommended_bets.append(f"{player_name} Aces Over 8.5")
                elif props['aces']['over_5_5'] == 'NO':
                    recommended_bets.append(f"{player_name} Aces Under 5.5")
            
            if props['double_faults']['confidence'] > 0.7:
                if props['double_faults']['over_3_5'] == 'YES':
                    recommended_bets.append(f"{player_name} Double Faults Over 3.5")
        
        # Risk assessment
        if confidence > 0.25:
            risk_level = "LOW"
        elif confidence > 0.15:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"
        
        return MatchPrediction(
            player1=player1_stats.name,
            player2=player2_stats.name,
            surface=match['surface'],
            tournament=match['tournament'],
            round=match['round'],
            winner_prediction=winner_prediction,
            confidence=confidence,
            set_prediction=set_prediction,
            surface_advantage=surface_advantage,
            fatigue_factor=fatigue_factor,
            form_factor=form_factor,
            h2h_factor=h2h_factor,
            double_fault_props={player1_stats.name: p1_props['double_faults'], 
                              player2_stats.name: p2_props['double_faults']},
            break_props={player1_stats.name: p1_props['breaks'], 
                        player2_stats.name: p2_props['breaks']},
            aces_props={player1_stats.name: p1_props['aces'], 
                       player2_stats.name: p2_props['aces']},
            recommended_bets=recommended_bets,
            risk_level=risk_level
        )

    def generate_betting_ticket(self, predictions: List[MatchPrediction]) -> str:
        """Generate a formatted betting ticket with recommendations"""
        ticket = "🎾 TENNIS BETTING TICKET - " + datetime.now().strftime('%Y-%m-%d') + " 🎾\n"
        ticket += "=" * 60 + "\n\n"
        
        total_confidence = 0
        low_risk_bets = []
        medium_risk_bets = []
        high_risk_bets = []
        
        for i, pred in enumerate(predictions, 1):
            ticket += f"MATCH {i}: {pred.tournament} - {pred.round}\n"
            ticket += f"{pred.player1} vs {pred.player2}\n"
            ticket += f"Surface: {pred.surface.upper()}\n"
            ticket += "-" * 40 + "\n"
            
            # Main prediction
            ticket += f"🏆 WINNER PREDICTION: {pred.winner_prediction}\n"
            ticket += f"📊 Confidence: {pred.confidence:.1%}\n"
            ticket += f"📈 Set Prediction: {pred.set_prediction}\n"
            ticket += f"⚠️  Risk Level: {pred.risk_level}\n\n"
            
            # Analysis breakdown
            ticket += "📋 ANALYSIS BREAKDOWN:\n"
            ticket += f"Surface Advantage: {pred.surface_advantage['advantage']} (+{pred.surface_advantage['difference']:.1%})\n"
            ticket += f"Fatigue Factor: {pred.fatigue_factor['advantage']} (+{pred.fatigue_factor['difference']:.1%})\n"
            ticket += f"Form Factor: {pred.form_factor['advantage']} (+{pred.form_factor['difference']:.1%})\n\n"
            
            # Player props
            ticket += "🎯 PLAYER PROPS:\n"
            for player in [pred.player1, pred.player2]:
                ticket += f"\n{player}:\n"
                
                aces = pred.aces_props[player]
                ticket += f"  Aces Expected: {aces['expected']} | Over 8.5: {aces['over_8_5']} (Confidence: {aces['confidence']:.1%})\n"
                
                df = pred.double_fault_props[player]
                ticket += f"  Double Faults Expected: {df['expected']} | Over 3.5: {df['over_3_5']} (Confidence: {df['confidence']:.1%})\n"
                
                breaks = pred.break_props[player]
                ticket += f"  Breaks Expected: {breaks['expected']} | Over 1.5: {breaks['over_1_5']} (Confidence: {breaks['confidence']:.1%})\n"
            
            # Recommended bets
            ticket += f"\n💰 RECOMMENDED BETS:\n"
            for bet in pred.recommended_bets:
                ticket += f"  ✅ {bet}\n"
                
                if pred.risk_level == "LOW":
                    low_risk_bets.append(bet)
                elif pred.risk_level == "MEDIUM":
                    medium_risk_bets.append(bet)
                else:
                    high_risk_bets.append(bet)
            
            ticket += "\n" + "=" * 60 + "\n\n"
            total_confidence += pred.confidence
        
        # Summary
        avg_confidence = total_confidence / len(predictions) if predictions else 0
        ticket += "📊 BETTING TICKET SUMMARY\n"
        ticket += "=" * 30 + "\n"
        ticket += f"Total Matches Analyzed: {len(predictions)}\n"
        ticket += f"Average Confidence: {avg_confidence:.1%}\n"
        ticket += f"Low Risk Bets: {len(low_risk_bets)}\n"
        ticket += f"Medium Risk Bets: {len(medium_risk_bets)}\n"
        ticket += f"High Risk Bets: {len(high_risk_bets)}\n\n"
        
        # Risk-based recommendations
        ticket += "🎯 RECOMMENDED BETTING STRATEGY:\n"
        if low_risk_bets:
            ticket += "\n🟢 HIGH CONFIDENCE BETS (Recommended for larger stakes):\n"
            for bet in low_risk_bets[:3]:  # Top 3 low risk bets
                ticket += f"  ⭐ {bet}\n"
        
        if medium_risk_bets:
            ticket += "\n🟡 MEDIUM CONFIDENCE BETS (Moderate stakes):\n"
            for bet in medium_risk_bets[:2]:  # Top 2 medium risk bets
                ticket += f"  📈 {bet}\n"
        
        ticket += "\n⚠️ RISK MANAGEMENT:\n"
        ticket += "• Never bet more than 5% of bankroll on single bet\n"
        ticket += "• Consider parlays only with high confidence picks\n"
        ticket += "• Monitor live odds for value opportunities\n"
        ticket += "• Track results for long-term profitability\n\n"
        
        ticket += f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        ticket += "Good luck! 🍀"
        
        return ticket

    def run_analysis(self):
        """Main function to run the tennis betting analysis"""
        print("🎾 Tennis Betting Analysis System Starting...")
        print("Fetching tomorrow's matches...")
        
        upcoming_matches = self.get_upcoming_matches()
        print(f"Found {len(upcoming_matches)} matches for analysis\n")
        
        predictions = []
        for match in upcoming_matches:
            print(f"Analyzing: {match['player1']} vs {match['player2']} ({match['tournament']})")
            prediction = self.predict_match(match)
            predictions.append(prediction)
        
        print("\nGenerating betting ticket...")
        ticket = self.generate_betting_ticket(predictions)
        
        # Save to file
        filename = f"tennis_betting_ticket_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(ticket)
        
        print(f"\n✅ Analysis complete! Betting ticket saved to: {filename}")
        print("\n" + "="*60)
        print(ticket)
        
        return predictions

if __name__ == "__main__":
    analyzer = TennisAnalyzer()
    predictions = analyzer.run_analysis()