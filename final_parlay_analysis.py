#!/usr/bin/env python3

"""
FINAL PARLAY ANALYSIS - July 23, 2025
Complete breakdown of the 6-leg $30 parlay
"""

from dataclasses import dataclass
from typing import List, Dict
import math

@dataclass
class ParlayLeg:
    pick: str
    sport: str
    odds: int
    confidence: float
    reasoning: str
    risk_factors: List[str]
    supporting_factors: List[str]
    value_rating: str  # "EXCELLENT", "GOOD", "FAIR", "POOR"

class FinalParlayAnalyzer:
    def __init__(self):
        self.setup_parlay_legs()
    
    def setup_parlay_legs(self):
        """Setup the user's final 6-leg parlay"""
        
        self.parlay_legs = [
            ParlayLeg(
                pick="Houston Astros ML",
                sport="MLB",
                odds=-280,
                confidence=88.0,
                reasoning="Elite team vs worst in AL, massive talent gap",
                risk_factors=["Heavy favorite juice", "Any Given Sunday effect"],
                supporting_factors=["Playoff team vs tanking team", "Home field", "Pitching advantage"],
                value_rating="GOOD"
            ),
            
            ParlayLeg(
                pick="Blue Jays vs Tigers Under 9",
                sport="MLB", 
                odds=-110,
                confidence=75.0,
                reasoning="Tigers struggle to score, solid pitching matchup",
                risk_factors=["Only 1 run cushion", "Rogers Centre can play high"],
                supporting_factors=["Tigers worst offense", "Both teams Under trends", "Starting pitcher quality"],
                value_rating="EXCELLENT"
            ),
            
            ParlayLeg(
                pick="Seattle Mariners ML",
                sport="MLB",
                odds=-140,
                confidence=72.0,
                reasoning="Better overall team, Angels struggling",
                risk_factors=["Road favorite", "Angels desperate at home", "Division rival"],
                supporting_factors=["Superior pitching", "Angels poor record", "Mariners playoff push"],
                value_rating="GOOD"
            ),
            
            ParlayLeg(
                pick="Ben Shelton ML",
                sport="Tennis",
                odds=-350,
                confidence=85.0,
                reasoning="Massive ranking gap (20 vs 115), serve advantage",
                risk_factors=["Heavy juice", "Tennis volatility", "Qualifier upset potential"],
                supporting_factors=["Huge ranking difference", "Hard court suits Shelton", "US Open motivation"],
                value_rating="FAIR"
            ),
            
            ParlayLeg(
                pick="Naomi Osaka ML",
                sport="Tennis",
                odds=130,
                confidence=75.0,
                reasoning="Plus odds on former #1, hard court specialist",
                risk_factors=["Mental game issues", "Putintseva can be tricky", "Comeback form question"],
                supporting_factors=["Plus odds value", "2x US Open champion", "Hard court advantage", "Experience edge"],
                value_rating="EXCELLENT"
            ),
            
            ParlayLeg(
                pick="Orioles vs Guardians NRFI",
                sport="MLB",
                odds=-115,
                confidence=70.0,
                reasoning="Both teams have solid first inning pitching",
                risk_factors=["Lowest confidence pick", "Orioles can start hot", "Weather factors"],
                supporting_factors=["Recent NRFI trends", "Starting pitcher quality", "Both teams disciplined"],
                value_rating="GOOD"
            )
        ]
    
    def calculate_parlay_odds(self):
        """Calculate true parlay odds and probability"""
        
        total_decimal = 1.0
        true_probability = 1.0
        
        for leg in self.parlay_legs:
            # Convert to decimal odds
            if leg.odds > 0:
                decimal = (leg.odds / 100) + 1
            else:
                decimal = (100 / abs(leg.odds)) + 1
            
            total_decimal *= decimal
            true_probability *= (leg.confidence / 100)
        
        payout = 30 * total_decimal
        american_odds = int((total_decimal - 1) * 100)
        
        return {
            "decimal_odds": total_decimal,
            "american_odds": american_odds,
            "payout": payout,
            "true_probability": true_probability * 100,
            "expected_value": (payout * true_probability) - 30
        }
    
    def analyze_risk_factors(self):
        """Analyze overall risk profile"""
        
        risk_analysis = {
            "high_risk_legs": [],
            "correlation_risks": [],
            "value_plays": [],
            "concerns": []
        }
        
        # Identify high risk legs
        for leg in self.parlay_legs:
            if leg.confidence < 75:
                risk_analysis["high_risk_legs"].append(leg.pick)
        
        # Check for correlations
        mlb_count = sum(1 for leg in self.parlay_legs if leg.sport == "MLB")
        tennis_count = sum(1 for leg in self.parlay_legs if leg.sport == "Tennis")
        
        if mlb_count >= 4:
            risk_analysis["correlation_risks"].append(f"Heavy MLB exposure ({mlb_count}/6 picks)")
        
        # Identify value plays
        for leg in self.parlay_legs:
            if leg.value_rating == "EXCELLENT":
                risk_analysis["value_plays"].append(leg.pick)
        
        # Major concerns
        if any(leg.confidence < 72 for leg in self.parlay_legs):
            risk_analysis["concerns"].append("Some picks below 72% confidence")
        
        heavy_favorites = [leg for leg in self.parlay_legs if leg.odds <= -280]
        if heavy_favorites:
            risk_analysis["concerns"].append("Heavy favorites reduce payout potential")
        
        return risk_analysis
    
    def run_complete_analysis(self):
        """Run comprehensive parlay analysis"""
        
        print("🔬 COMPLETE PARLAY ANALYSIS")
        print("=" * 70)
        print("📊 6-LEG PARLAY: $30 TO WIN BIG")
        
        # Calculate odds and probability
        stats = self.calculate_parlay_odds()
        
        print(f"\n💰 FINANCIAL BREAKDOWN:")
        print(f"  Bet Amount: $30")
        print(f"  Potential Payout: ${stats['payout']:.0f}")
        print(f"  Net Profit: ${stats['payout'] - 30:.0f}")
        print(f"  American Odds: +{stats['american_odds']}")
        print(f"  True Probability: {stats['true_probability']:.2f}%")
        print(f"  Expected Value: ${stats['expected_value']:.2f}")
        
        # Leg-by-leg analysis
        print(f"\n🎯 LEG-BY-LEG BREAKDOWN:")
        
        for i, leg in enumerate(self.parlay_legs, 1):
            print(f"\n  LEG {i}: {leg.pick} ({leg.odds:+d})")
            print(f"    Confidence: {leg.confidence:.1f}%")
            print(f"    Value Rating: {leg.value_rating}")
            print(f"    Reasoning: {leg.reasoning}")
            
            if leg.risk_factors:
                print(f"    🚩 Risks: {', '.join(leg.risk_factors)}")
            
            if leg.supporting_factors:
                print(f"    ✅ Support: {', '.join(leg.supporting_factors)}")
        
        # Risk analysis
        risks = self.analyze_risk_factors()
        
        print(f"\n⚠️  RISK ASSESSMENT:")
        
        if risks["high_risk_legs"]:
            print(f"  High Risk Legs: {', '.join(risks['high_risk_legs'])}")
        else:
            print(f"  High Risk Legs: None (all 70%+ confidence)")
        
        if risks["correlation_risks"]:
            print(f"  Correlation Risks: {', '.join(risks['correlation_risks'])}")
        
        if risks["value_plays"]:
            print(f"  Value Plays: {', '.join(risks['value_plays'])}")
        
        if risks["concerns"]:
            print(f"  Major Concerns:")
            for concern in risks["concerns"]:
                print(f"    - {concern}")
        
        # Strength analysis
        print(f"\n💪 PARLAY STRENGTHS:")
        
        avg_confidence = sum(leg.confidence for leg in self.parlay_legs) / len(self.parlay_legs)
        print(f"  Average Confidence: {avg_confidence:.1f}%")
        
        excellent_value = len([leg for leg in self.parlay_legs if leg.value_rating == "EXCELLENT"])
        print(f"  Excellent Value Plays: {excellent_value}/6")
        
        high_confidence = len([leg for leg in self.parlay_legs if leg.confidence >= 80])
        print(f"  High Confidence Picks (80%+): {high_confidence}/6")
        
        # Scenarios
        print(f"\n📈 SUCCESS SCENARIOS:")
        print(f"  Best Case: All 6 legs hit → ${stats['payout']:.0f}")
        print(f"  5/6 Hit: Parlay loses → $0")
        print(f"  Probability: {stats['true_probability']:.2f}% chance of success")
        print(f"  Risk/Reward: ~{stats['true_probability']:.0f}% chance for {(stats['payout']/30):.1f}x return")
        
        # Final verdict
        print(f"\n🏆 FINAL ANALYSIS VERDICT:")
        
        if stats['expected_value'] > 0:
            print(f"  ✅ POSITIVE EXPECTED VALUE (+${stats['expected_value']:.2f})")
        else:
            print(f"  ❌ NEGATIVE EXPECTED VALUE (${stats['expected_value']:.2f})")
        
        if stats['true_probability'] >= 20:
            print(f"  ✅ REASONABLE PROBABILITY ({stats['true_probability']:.2f}%)")
        else:
            print(f"  ⚠️  LOW PROBABILITY ({stats['true_probability']:.2f}%)")
        
        if avg_confidence >= 75:
            print(f"  ✅ STRONG AVERAGE CONFIDENCE ({avg_confidence:.1f}%)")
        else:
            print(f"  ⚠️  MODERATE CONFIDENCE ({avg_confidence:.1f}%)")
        
        # Overall recommendation
        print(f"\n🎯 RECOMMENDATION:")
        
        if (stats['expected_value'] > 0 and 
            stats['true_probability'] >= 15 and 
            avg_confidence >= 74):
            print(f"  🚀 STRONG PARLAY - GOOD VALUE!")
            print(f"  📊 Math supports this bet")
            print(f"  🎲 {stats['true_probability']:.1f}% is reasonable for {(stats['payout']/30):.1f}x payout")
        elif stats['true_probability'] >= 12:
            print(f"  ✅ DECENT PARLAY - MANAGEABLE RISK")
            print(f"  ⚖️  Balanced risk/reward ratio")
        else:
            print(f"  ⚠️  HIGH RISK PARLAY")
            print(f"  🎰 Low probability but huge upside")
        
        return stats

if __name__ == "__main__":
    analyzer = FinalParlayAnalyzer()
    results = analyzer.run_complete_analysis()