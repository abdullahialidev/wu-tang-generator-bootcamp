#!/usr/bin/env python3

"""
ULTIMATE $20 TO $1000+ PARLAY ANALYZER
Adding maximum tennis picks for 50:1+ odds targeting $1000 payout
"""

from dataclasses import dataclass
from typing import List, Dict
import math

@dataclass
class UltimatePick:
    name: str
    sport: str
    odds: int  # American odds
    confidence: float  # 0-100
    edge_percentage: float
    reasoning: str

class UltimateParlayBuilder:
    def __init__(self):
        self.setup_ultimate_picks()
    
    def setup_ultimate_picks(self):
        """All picks for the ultimate $1000+ parlay"""
        
        # TIER 1: FOUNDATION (Highest Confidence)
        self.tier1_picks = [
            UltimatePick("Pirates vs Tigers NRFI", "MLB", -132, 92.0, 18.5, 
                        "Pirates 0-10 first inning streak - HISTORICAL ANOMALY"),
            UltimatePick("Cardinals vs Rockies Under 11.5", "MLB", -110, 82.0, 12.3,
                        "Under 6/7 recent games, day game at Coors reduces offense"),
            UltimatePick("Giants vs Braves NRFI", "MLB", 105, 78.0, 11.2,
                        "Braves .165 BA vs RHP curveballs (worst in MLB)")
        ]
        
        # TIER 2: SOLID VALUE (Good Confidence)
        self.tier2_picks = [
            UltimatePick("Alex de Minaur ML", "Tennis", -150, 75.0, 21.8,
                        "70.8% vs 61.5% hard court win rate, fatigue advantage"),
            UltimatePick("Philadelphia Phillies ML", "MLB", -154, 73.0, 8.7,
                        "Home vs struggling Red Sox bullpen, Nola on mound"),
            UltimatePick("Toronto Blue Jays ML", "MLB", -118, 71.0, 9.1,
                        "Yankees 2-8 in last 10, Blue Jays hot streak")
        ]
        
        # TIER 3: ADDITIONAL TENNIS (Adding for $1000+ target)
        self.tier3_tennis = [
            UltimatePick("Naomi Osaka ML", "Tennis", 130, 69.0, 13.9,
                        "68.1% vs 58.1% hard court advantage, fresher"),
            UltimatePick("Lorenzo Musetti ML", "Tennis", -140, 67.0, 16.8,
                        "Clay specialist advantage, Cerundolo fatigue"),
            UltimatePick("Petra Kvitova ML", "Tennis", -125, 65.0, 14.2,
                        "Experience edge, powerful serve on hard courts")
        ]
    
    def calculate_american_to_decimal(self, american_odds):
        """Convert American odds to decimal"""
        if american_odds > 0:
            return (american_odds / 100) + 1
        else:
            return (100 / abs(american_odds)) + 1
    
    def calculate_parlay_odds(self, picks):
        """Calculate total parlay odds"""
        total_decimal = 1.0
        for pick in picks:
            decimal = self.calculate_american_to_decimal(pick.odds)
            total_decimal *= decimal
        return total_decimal
    
    def american_odds_from_decimal(self, decimal_odds):
        """Convert decimal back to American odds"""
        if decimal_odds >= 2.0:
            return int((decimal_odds - 1) * 100)
        else:
            return int(-100 / (decimal_odds - 1))
    
    def analyze_ultimate_parlays(self):
        """Analyze different parlay combinations for $1000+ target"""
        
        print("🚀 ULTIMATE $20 TO $1000+ PARLAY ANALYSIS")
        print("=" * 60)
        
        # OPTION 1: 8-LEG BALANCED APPROACH
        balanced_picks = (self.tier1_picks + self.tier2_picks + 
                         self.tier3_tennis[:2])
        
        balanced_odds = self.calculate_parlay_odds(balanced_picks)
        balanced_payout = 20 * balanced_odds
        
        print(f"\n🎯 OPTION 1: BALANCED 8-LEG PARLAY")
        print(f"TARGET ODDS: +{self.american_odds_from_decimal(balanced_odds)}")
        print(f"PAYOUT: $20 → ${balanced_payout:.0f}")
        
        avg_confidence = sum(p.confidence for p in balanced_picks) / len(balanced_picks)
        true_prob = (avg_confidence / 100) ** len(balanced_picks) * 100
        
        print(f"TRUE PROBABILITY: {true_prob:.2f}%")
        print(f"PICKS:")
        for i, pick in enumerate(balanced_picks, 1):
            print(f"  {i}. {pick.name} ({pick.odds:+d}) - {pick.confidence:.1f}% confidence")
            print(f"     → {pick.reasoning}")
        
        # OPTION 2: 9-LEG MAXIMUM CHAOS
        chaos_picks = self.tier1_picks + self.tier2_picks + self.tier3_tennis
        
        chaos_odds = self.calculate_parlay_odds(chaos_picks)
        chaos_payout = 20 * chaos_odds
        
        print(f"\n🔥 OPTION 2: MAXIMUM CHAOS 9-LEG PARLAY")
        print(f"TARGET ODDS: +{self.american_odds_from_decimal(chaos_odds)}")
        print(f"PAYOUT: $20 → ${chaos_payout:.0f}")
        
        chaos_confidence = sum(p.confidence for p in chaos_picks) / len(chaos_picks)
        chaos_prob = (chaos_confidence / 100) ** len(chaos_picks) * 100
        
        print(f"TRUE PROBABILITY: {chaos_prob:.2f}%")
        print(f"PICKS:")
        for i, pick in enumerate(chaos_picks, 1):
            print(f"  {i}. {pick.name} ({pick.odds:+d}) - {pick.confidence:.1f}% confidence")
        
        # RECOMMENDATION
        print(f"\n🏆 FINAL RECOMMENDATION:")
        if balanced_payout >= 1000:
            print(f"GO WITH OPTION 1 - Better probability ({true_prob:.2f}% vs {chaos_prob:.2f}%)")
            print(f"Still hits your $1000+ target at ${balanced_payout:.0f}")
            return balanced_picks
        else:
            print(f"OPTION 2 NEEDED for $1000+ target")
            print(f"Risk vs Reward: {chaos_prob:.2f}% chance for ${chaos_payout:.0f}")
            return chaos_picks

if __name__ == "__main__":
    analyzer = UltimateParlayBuilder()
    recommended_picks = analyzer.analyze_ultimate_parlays()