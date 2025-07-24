#!/usr/bin/env python3

"""
Enhanced Tennis Motivation Analyzer - July 23, 2025
Factoring in player motivation based on year performance and upcoming events
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
import math
from datetime import datetime, timedelta

@dataclass
class PlayerMotivationProfile:
    name: str
    current_ranking: int
    year_start_ranking: int
    titles_won_2025: int
    prize_money_2025: float  # millions
    recent_form: str  # "hot", "cold", "steady"
    upcoming_events: List[str]
    motivation_factors: Dict[str, float]
    motivation_score: float  # 0-100
    seriousness_level: str  # "maximum", "high", "moderate", "low"

class TennisMotivationAnalyzer:
    def __init__(self):
        self.setup_motivation_factors()
        self.setup_player_profiles()
        self.setup_upcoming_events()
    
    def setup_motivation_factors(self):
        """Define motivation factors and their weights"""
        self.motivation_weights = {
            "ranking_trajectory": 0.25,      # Rising/falling in rankings
            "prize_money_needs": 0.20,       # Financial motivation
            "major_preparation": 0.20,       # US Open preparation
            "career_stage": 0.15,            # Young gun vs veteran
            "recent_results": 0.10,          # Confidence from recent wins
            "personal_goals": 0.10           # Tournament-specific goals
        }
    
    def setup_upcoming_events(self):
        """Major upcoming events that affect motivation"""
        self.upcoming_schedule = {
            "us_open_2025": {
                "date": "August 26 - September 8, 2025",
                "days_away": 34,
                "importance": "MAJOR",
                "surface": "hard",
                "prize_money": "$75M total"
            },
            "cincinnati_masters": {
                "date": "August 12-18, 2025", 
                "days_away": 20,
                "importance": "MASTERS",
                "surface": "hard",
                "prize_money": "$6.8M total"
            },
            "toronto_masters": {
                "date": "August 5-11, 2025",
                "days_away": 13,
                "importance": "MASTERS", 
                "surface": "hard",
                "prize_money": "$6.8M total"
            }
        }
    
    def setup_player_profiles(self):
        """Setup detailed motivation profiles for each player"""
        
        self.player_profiles = {
            "Alex de Minaur": PlayerMotivationProfile(
                name="Alex de Minaur",
                current_ranking=10,
                year_start_ranking=12,
                titles_won_2025=2,
                prize_money_2025=3.2,
                recent_form="hot",
                upcoming_events=["Toronto Masters", "Cincinnati Masters", "US Open"],
                motivation_factors={
                    "ranking_trajectory": 85.0,    # Moving up rankings (12→10)
                    "prize_money_needs": 70.0,     # Solid earnings but wants more
                    "major_preparation": 90.0,     # US Open is huge for him
                    "career_stage": 85.0,          # Prime age (26), peak years
                    "recent_results": 80.0,        # Good recent form
                    "personal_goals": 85.0         # Wants first Grand Slam
                },
                motivation_score=82.0,
                seriousness_level="maximum"
            ),
            
            "Frances Tiafoe": PlayerMotivationProfile(
                name="Frances Tiafoe",
                current_ranking=29,
                year_start_ranking=16,
                titles_won_2025=0,
                prize_money_2025=1.8,
                recent_form="cold",
                upcoming_events=["Toronto Masters", "Cincinnati Masters", "US Open"],
                motivation_factors={
                    "ranking_trajectory": 30.0,    # Dropped significantly (16→29)
                    "prize_money_needs": 85.0,     # Needs results for money
                    "major_preparation": 95.0,     # US Open at home crucial
                    "career_stage": 75.0,          # Age 27, still has time
                    "recent_results": 40.0,        # Poor recent form
                    "personal_goals": 90.0         # Desperately wants breakthrough
                },
                motivation_score=71.0,
                seriousness_level="maximum"
            ),
            
            "Naomi Osaka": PlayerMotivationProfile(
                name="Naomi Osaka",
                current_ranking=25,
                year_start_ranking=47,
                titles_won_2025=1,
                prize_money_2025=2.1,
                recent_form="steady",
                upcoming_events=["Toronto WTA", "Cincinnati WTA", "US Open"],
                motivation_factors={
                    "ranking_trajectory": 90.0,    # Major comeback (47→25)
                    "prize_money_needs": 40.0,     # Already wealthy
                    "major_preparation": 85.0,     # 2x US Open champion
                    "career_stage": 95.0,          # Age 27, proven champion
                    "recent_results": 70.0,        # Steady improvement
                    "personal_goals": 80.0         # Wants return to top 10
                },
                motivation_score=77.0,
                seriousness_level="high"
            ),
            
            "Emma Raducanu": PlayerMotivationProfile(
                name="Emma Raducanu",
                current_ranking=52,
                year_start_ranking=28,
                titles_won_2025=0,
                prize_money_2025=0.9,
                recent_form="cold",
                upcoming_events=["Toronto WTA", "Cincinnati WTA", "US Open"],
                motivation_factors={
                    "ranking_trajectory": 25.0,    # Significant drop (28→52)
                    "prize_money_needs": 75.0,     # Needs results
                    "major_preparation": 80.0,     # 2021 US Open champion
                    "career_stage": 90.0,          # Age 22, all the time in world
                    "recent_results": 30.0,        # Struggling with form
                    "personal_goals": 70.0         # Trying to find consistency
                },
                motivation_score=58.0,
                seriousness_level="moderate"
            ),
            
            "Lorenzo Musetti": PlayerMotivationProfile(
                name="Lorenzo Musetti",
                current_ranking=18,
                year_start_ranking=23,
                titles_won_2025=1,
                prize_money_2025=2.4,
                recent_form="hot",
                upcoming_events=["Toronto Masters", "Cincinnati Masters", "US Open"],
                motivation_factors={
                    "ranking_trajectory": 80.0,    # Moving up (23→18)
                    "prize_money_needs": 65.0,     # Decent earnings
                    "major_preparation": 70.0,     # Hard courts not his best
                    "career_stage": 90.0,          # Age 23, rising star
                    "recent_results": 85.0,        # Great recent form
                    "personal_goals": 75.0         # Wants to crack top 15
                },
                motivation_score=76.0,
                seriousness_level="high"
            ),
            
            "Francisco Cerundolo": PlayerMotivationProfile(
                name="Francisco Cerundolo",
                current_ranking=35,
                year_start_ranking=19,
                titles_won_2025=0,
                prize_money_2025=1.3,
                recent_form="cold",
                upcoming_events=["Toronto Masters", "Cincinnati Masters", "US Open"],
                motivation_factors={
                    "ranking_trajectory": 20.0,    # Major drop (19→35)
                    "prize_money_needs": 80.0,     # Needs results badly
                    "major_preparation": 60.0,     # Clay specialist struggling on hard
                    "career_stage": 70.0,          # Age 26, prime but pressure
                    "recent_results": 35.0,        # Poor recent form
                    "personal_goals": 85.0         # Desperate to stop slide
                },
                motivation_score=58.0,
                seriousness_level="moderate"
            ),
            
            "Petra Kvitova": PlayerMotivationProfile(
                name="Petra Kvitova",
                current_ranking=22,
                year_start_ranking=18,
                titles_won_2025=1,
                prize_money_2025=1.9,
                recent_form="steady",
                upcoming_events=["Toronto WTA", "Cincinnati WTA", "US Open"],
                motivation_factors={
                    "ranking_trajectory": 60.0,    # Slight drop (18→22)
                    "prize_money_needs": 30.0,     # Established, wealthy
                    "major_preparation": 75.0,     # 2x Wimbledon champion
                    "career_stage": 40.0,          # Age 35, veteran stage
                    "recent_results": 65.0,        # Decent but inconsistent
                    "personal_goals": 60.0         # Playing for enjoyment mostly
                },
                motivation_score=55.0,
                seriousness_level="moderate"
            ),
            
            "Linda Noskova": PlayerMotivationProfile(
                name="Linda Noskova",
                current_ranking=31,
                year_start_ranking=45,
                titles_won_2025=1,
                prize_money_2025=1.6,
                recent_form="hot",
                upcoming_events=["Toronto WTA", "Cincinnati WTA", "US Open"],
                motivation_factors={
                    "ranking_trajectory": 95.0,    # Major rise (45→31)
                    "prize_money_needs": 85.0,     # Young, needs prize money
                    "major_preparation": 80.0,     # First real US Open shot
                    "career_stage": 95.0,          # Age 20, unlimited potential
                    "recent_results": 90.0,        # Excellent recent form
                    "personal_goals": 90.0         # Wants to break top 20
                },
                motivation_score=87.0,
                seriousness_level="maximum"
            )
        }
    
    def calculate_motivation_impact(self, player_name: str) -> Dict[str, float]:
        """Calculate how motivation affects performance predictions"""
        
        if player_name not in self.player_profiles:
            return {"motivation_adjustment": 0.0, "confidence_boost": 0.0}
        
        profile = self.player_profiles[player_name]
        
        # Base motivation impact
        motivation_multiplier = profile.motivation_score / 100.0
        
        # Seriousness level impact
        seriousness_boosts = {
            "maximum": 1.15,
            "high": 1.08,
            "moderate": 1.0,
            "low": 0.92
        }
        
        seriousness_boost = seriousness_boosts[profile.seriousness_level]
        
        # US Open preparation boost (hard court matches matter more)
        us_open_prep_boost = 1.0
        if "US Open" in profile.upcoming_events:
            days_to_us_open = self.upcoming_schedule["us_open_2025"]["days_away"]
            if days_to_us_open <= 40:  # Within US Open prep window
                us_open_prep_boost = 1.05 + (profile.motivation_factors["major_preparation"] / 2000)
        
        # Calculate final adjustments
        total_motivation_impact = motivation_multiplier * seriousness_boost * us_open_prep_boost
        
        # Convert to percentage adjustments
        motivation_adjustment = (total_motivation_impact - 1.0) * 100
        confidence_boost = min(motivation_adjustment * 0.3, 10.0)  # Cap at 10% boost
        
        return {
            "motivation_adjustment": motivation_adjustment,
            "confidence_boost": confidence_boost,
            "motivation_score": profile.motivation_score,
            "seriousness_level": profile.seriousness_level,
            "us_open_factor": us_open_prep_boost,
            "key_motivators": self._get_key_motivators(profile)
        }
    
    def _get_key_motivators(self, profile: PlayerMotivationProfile) -> List[str]:
        """Identify the strongest motivation factors for a player"""
        motivators = []
        
        for factor, score in profile.motivation_factors.items():
            if score >= 80:
                motivators.append(factor)
        
        return motivators
    
    def analyze_enhanced_tennis_picks(self):
        """Run enhanced analysis with motivation factors"""
        
        print("🎾 ENHANCED TENNIS MOTIVATION ANALYSIS - July 23, 2025")
        print("=" * 70)
        print("🏆 Factoring in: Year performance, US Open prep, player seriousness")
        
        # Define the matches with original analysis
        matches = [
            {
                "player1": "Alex de Minaur",
                "player2": "Frances Tiafoe", 
                "original_confidence": 75.0,
                "original_reasoning": "70.8% vs 61.5% hard court win rate, fatigue advantage"
            },
            {
                "player1": "Naomi Osaka",
                "player2": "Emma Raducanu",
                "original_confidence": 69.0,
                "original_reasoning": "68.1% vs 58.1% hard court advantage, fresher"
            },
            {
                "player1": "Lorenzo Musetti", 
                "player2": "Francisco Cerundolo",
                "original_confidence": 67.0,
                "original_reasoning": "Clay specialist advantage, Cerundolo fatigue"
            },
            {
                "player1": "Petra Kvitova",
                "player2": "Linda Noskova", 
                "original_confidence": 65.0,
                "original_reasoning": "Experience edge, powerful serve on hard courts"
            }
        ]
        
        enhanced_picks = []
        
        for match in matches:
            p1_name = match["player1"]
            p2_name = match["player2"]
            
            p1_motivation = self.calculate_motivation_impact(p1_name)
            p2_motivation = self.calculate_motivation_impact(p2_name)
            
            print(f"\n🎯 MATCH: {p1_name} vs {p2_name}")
            print(f"📊 MOTIVATION ANALYSIS:")
            
            # Player 1 analysis
            print(f"\n   {p1_name}:")
            print(f"     Motivation Score: {p1_motivation['motivation_score']:.1f}/100")
            print(f"     Seriousness Level: {p1_motivation['seriousness_level'].upper()}")
            print(f"     Key Motivators: {', '.join(p1_motivation['key_motivators'])}")
            print(f"     Performance Boost: {p1_motivation['motivation_adjustment']:+.1f}%")
            
            # Player 2 analysis  
            print(f"\n   {p2_name}:")
            print(f"     Motivation Score: {p2_motivation['motivation_score']:.1f}/100")
            print(f"     Seriousness Level: {p2_motivation['seriousness_level'].upper()}")
            print(f"     Key Motivators: {', '.join(p2_motivation['key_motivators'])}")
            print(f"     Performance Boost: {p2_motivation['motivation_adjustment']:+.1f}%")
            
            # Calculate motivation differential
            motivation_edge = p1_motivation['motivation_score'] - p2_motivation['motivation_score']
            
            # Adjust original confidence based on motivation
            motivation_adjustment = motivation_edge * 0.3  # 30% weight on motivation
            enhanced_confidence = match["original_confidence"] + motivation_adjustment
            enhanced_confidence = max(50.0, min(95.0, enhanced_confidence))  # Cap between 50-95%
            
            # Determine recommendation
            if motivation_edge > 15:
                recommendation = f"{p1_name} ML"
                recommendation_confidence = enhanced_confidence
            elif motivation_edge < -15:
                recommendation = f"{p2_name} ML"  
                recommendation_confidence = 100 - enhanced_confidence
            else:
                # Stick with original analysis
                recommendation = f"{p1_name} ML (original pick)"
                recommendation_confidence = match["original_confidence"]
            
            print(f"\n   📈 MOTIVATION IMPACT:")
            print(f"     Motivation Edge: {p1_name} +{motivation_edge:.1f} points")
            print(f"     Original Confidence: {match['original_confidence']:.1f}%")
            print(f"     Enhanced Confidence: {enhanced_confidence:.1f}%")
            print(f"     Adjustment: {motivation_adjustment:+.1f}%")
            
            print(f"\n   🎯 ENHANCED RECOMMENDATION:")
            print(f"     BET: {recommendation}")
            print(f"     CONFIDENCE: {recommendation_confidence:.1f}%")
            
            enhanced_picks.append({
                "match": f"{p1_name} vs {p2_name}",
                "recommendation": recommendation,
                "confidence": recommendation_confidence,
                "motivation_edge": motivation_edge,
                "original_confidence": match["original_confidence"],
                "enhanced_confidence": enhanced_confidence
            })
        
        # Summary and parlay update
        print(f"\n🏆 MOTIVATION-ENHANCED SUMMARY:")
        print(f"   US OPEN PREPARATION FACTOR: All players highly motivated")
        print(f"   34 days until US Open - Peak preparation time")
        
        significant_changes = [p for p in enhanced_picks if abs(p["confidence"] - p["original_confidence"]) > 5]
        
        if significant_changes:
            print(f"\n⚡ SIGNIFICANT MOTIVATION ADJUSTMENTS:")
            for pick in significant_changes:
                change = pick["confidence"] - pick["original_confidence"]
                print(f"     {pick['match']}: {change:+.1f}% confidence change")
        
        return enhanced_picks

if __name__ == "__main__":
    analyzer = TennisMotivationAnalyzer()
    enhanced_picks = analyzer.analyze_enhanced_tennis_picks()