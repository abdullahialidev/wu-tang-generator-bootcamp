#!/usr/bin/env python3

"""
FINAL MOTIVATION-ENHANCED PARLAY - $20 TO $1000+
Incorporating tennis motivation analysis based on year performance and US Open prep
"""

from dataclasses import dataclass
from typing import List, Dict
import math

@dataclass
class FinalPick:
    name: str
    sport: str
    odds: int
    confidence: float
    reasoning: str
    motivation_notes: str = ""

class FinalParlayBuilder:
    def __init__(self):
        self.setup_final_picks()
    
    def setup_final_picks(self):
        """Setup final picks with motivation enhancements"""
        
        # CORE MLB FOUNDATION (Unchanged - still rock solid)
        self.core_mlb_picks = [
            FinalPick(
                name="Pirates vs Tigers NRFI",
                sport="MLB",
                odds=-132,
                confidence=92.0,
                reasoning="Pirates 0-10 first inning streak - HISTORICAL ANOMALY",
                motivation_notes="N/A - Baseball pick"
            ),
            FinalPick(
                name="Cardinals vs Rockies Under 11.5",
                sport="MLB", 
                odds=-110,
                confidence=82.0,
                reasoning="Under 6/7 recent games, day game reduces Coors offense",
                motivation_notes="N/A - Baseball pick"
            ),
            FinalPick(
                name="Giants vs Braves NRFI",
                sport="MLB",
                odds=105,
                confidence=78.0,
                reasoning="Braves .165 BA vs RHP curveballs (WORST IN MLB)",
                motivation_notes="N/A - Baseball pick"
            ),
            FinalPick(
                name="Philadelphia Phillies ML",
                sport="MLB",
                odds=-154,
                confidence=73.0,
                reasoning="Home vs struggling Red Sox bullpen, Nola on mound",
                motivation_notes="N/A - Baseball pick"
            ),
            FinalPick(
                name="Toronto Blue Jays ML",
                sport="MLB",
                odds=-118,
                confidence=71.0,
                reasoning="Yankees 2-8 in last 10, Blue Jays hot streak",
                motivation_notes="N/A - Baseball pick"
            )
        ]
        
        # ENHANCED TENNIS PICKS (Based on motivation analysis)
        self.enhanced_tennis_picks = [
            FinalPick(
                name="Alex de Minaur ML",
                sport="Tennis",
                odds=-150,
                confidence=78.3,  # Enhanced from 75.0%
                reasoning="70.8% vs 61.5% hard court win rate + fatigue advantage",
                motivation_notes="MAXIMUM seriousness, +11 motivation edge over Tiafoe, US Open prep boost"
            ),
            FinalPick(
                name="Naomi Osaka ML", 
                sport="Tennis",
                odds=130,
                confidence=74.7,  # Enhanced from 69.0%
                reasoning="68.1% vs 58.1% hard court advantage + fresher",
                motivation_notes="HIGH motivation (+19 over Raducanu), major comeback year, 2x US Open champion"
            ),
            FinalPick(
                name="Lorenzo Musetti ML",
                sport="Tennis", 
                odds=-140,
                confidence=72.4,  # Enhanced from 67.0%
                reasoning="Clay specialist advantage + Cerundolo fatigue",
                motivation_notes="HIGH motivation (+18 over Cerundolo), rising star with hot form"
            )
        ]
        
        # SURPRISING CHANGE: Linda Noskova based on motivation
        self.motivation_surprise = FinalPick(
            name="Linda Noskova ML",
            sport="Tennis",
            odds=145,  # Plus odds!
            confidence=55.4,  # Flipped from Kvitova
            reasoning="Young gun motivation vs veteran coasting",
            motivation_notes="MAXIMUM seriousness (87/100 vs 55/100), massive +32 motivation edge, career-best year"
        )
    
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
    
    def build_final_parlays(self):
        """Build final parlay options with motivation enhancements"""
        
        print("🎾 FINAL MOTIVATION-ENHANCED PARLAY BUILDER")
        print("=" * 70)
        print("🏆 Incorporating US Open prep motivation + year performance analysis")
        
        # OPTION 1: Conservative with proven picks
        conservative_picks = (self.core_mlb_picks + 
                             self.enhanced_tennis_picks[:2])  # de Minaur + Osaka
        
        conservative_odds = self.calculate_parlay_odds(conservative_picks)
        conservative_payout = 20 * conservative_odds
        
        print(f"\n🎯 OPTION 1: MOTIVATION-ENHANCED CONSERVATIVE (7-LEG)")
        print(f"TARGET ODDS: +{self.american_odds_from_decimal(conservative_odds)}")
        print(f"PAYOUT: $20 → ${conservative_payout:.0f}")
        
        avg_confidence = sum(p.confidence for p in conservative_picks) / len(conservative_picks)
        true_prob = (avg_confidence / 100) ** len(conservative_picks) * 100
        
        print(f"TRUE PROBABILITY: {true_prob:.2f}%")
        print(f"MOTIVATION ENHANCEMENTS:")
        for i, pick in enumerate(conservative_picks, 1):
            marker = "📈" if pick.motivation_notes and "Enhanced" in pick.motivation_notes or "motivation" in pick.motivation_notes else "✅"
            print(f"  {i}. {marker} {pick.name} ({pick.odds:+d}) - {pick.confidence:.1f}% confidence")
            if pick.motivation_notes and pick.motivation_notes != "N/A - Baseball pick":
                print(f"     🎾 {pick.motivation_notes}")
        
        # OPTION 2: All enhanced picks including surprise
        enhanced_picks = (self.core_mlb_picks + 
                         self.enhanced_tennis_picks + 
                         [self.motivation_surprise])
        
        enhanced_odds = self.calculate_parlay_odds(enhanced_picks)
        enhanced_payout = 20 * enhanced_odds
        
        print(f"\n🔥 OPTION 2: FULL MOTIVATION PARLAY (9-LEG)")
        print(f"TARGET ODDS: +{self.american_odds_from_decimal(enhanced_odds)}")
        print(f"PAYOUT: $20 → ${enhanced_payout:.0f}")
        
        enhanced_confidence = sum(p.confidence for p in enhanced_picks) / len(enhanced_picks)
        enhanced_prob = (enhanced_confidence / 100) ** len(enhanced_picks) * 100
        
        print(f"TRUE PROBABILITY: {enhanced_prob:.2f}%")
        print(f"INCLUDES MOTIVATION SURPRISE:")
        print(f"  🚀 {self.motivation_surprise.name} (+{self.motivation_surprise.odds}) - PLUS ODDS!")
        print(f"     🎾 {self.motivation_surprise.motivation_notes}")
        
        # OPTION 3: Hybrid approach (remove weakest, add surprise)
        hybrid_picks = (self.core_mlb_picks[:-1] +  # Remove Blue Jays (weakest MLB)
                       self.enhanced_tennis_picks +
                       [self.motivation_surprise])
        
        hybrid_odds = self.calculate_parlay_odds(hybrid_picks)
        hybrid_payout = 20 * hybrid_odds
        
        print(f"\n⚡ OPTION 3: MOTIVATION HYBRID (8-LEG)")
        print(f"TARGET ODDS: +{self.american_odds_from_decimal(hybrid_odds)}")
        print(f"PAYOUT: $20 → ${hybrid_payout:.0f}")
        
        hybrid_confidence = sum(p.confidence for p in hybrid_picks) / len(hybrid_picks)
        hybrid_prob = (hybrid_confidence / 100) ** len(hybrid_picks) * 100
        
        print(f"TRUE PROBABILITY: {hybrid_prob:.2f}%")
        print(f"STRATEGY: Remove weakest MLB pick, add motivation surprise")
        
        # FINAL RECOMMENDATION
        print(f"\n🏆 FINAL MOTIVATION-ENHANCED RECOMMENDATION:")
        
        if enhanced_payout >= 1000 and enhanced_prob >= 5.0:
            print(f"🚀 GO WITH OPTION 2 - FULL MOTIVATION PARLAY")
            print(f"   Payout: ${enhanced_payout:.0f} (CRUSHES $1000 target)")
            print(f"   Probability: {enhanced_prob:.2f}% (Reasonable for this payout)")
            print(f"   Key Edge: Linda Noskova at +145 with MAXIMUM motivation")
            return enhanced_picks
        elif hybrid_payout >= 1000:
            print(f"🎯 RECOMMEND OPTION 3 - MOTIVATION HYBRID")
            print(f"   Payout: ${hybrid_payout:.0f} (Hits $1000 target)")
            print(f"   Probability: {hybrid_prob:.2f}% (Better odds)")
            print(f"   Balance of safety and motivation edge")
            return hybrid_picks
        else:
            print(f"✅ OPTION 1 - MOTIVATION-ENHANCED CONSERVATIVE")
            print(f"   Payout: ${conservative_payout:.0f}")
            print(f"   Probability: {true_prob:.2f}% (Highest success rate)")
            print(f"   Proven picks with motivation boost")
            return conservative_picks

if __name__ == "__main__":
    builder = FinalParlayBuilder()
    final_picks = builder.build_final_parlays()