
import plotly.utils
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

class ReconEngine:
    @staticmethod
    def generate_report(team_data, match_history):
        """Main entry point to create the full scouting report."""
        macro = ReconEngine._analyze_macro(match_history)
        players = ReconEngine._analyze_players(match_history)
        comps = ReconEngine._analyze_compositions(match_history)
        recommendations = ReconEngine._generate_recommendations(macro, players)
        
        return {
            "macro": macro,
            "players": players,
            "comps": comps,
            "recommendations": recommendations,
            "charts": ReconEngine._generate_charts(macro, players)
        }

    @staticmethod
    def _analyze_macro(matches):
        # Calculate Team-wide patterns
        df = pd.DataFrame(matches)
        return {
            "early_aggression": "High" if df['fb_rate'].mean() > 0.6 else "Moderate",
            "obj_priority": "Dragon" if df['dragon_rate'].mean() > df['herald_rate'].mean() else "Void/Tower",
            "avg_gd15": int(df['gold_diff_15'].mean()),
            "win_rate_when_ahead": f"{int(df[df['lead_15'] == True]['win'].mean() * 100)}%"
        }

    @staticmethod
    def _analyze_players(matches):
        # Logic to find statistical outliers (e.g., Mid laner weak to assassins)
        # This would iterate through match participants in the GRID data
        return [
            {"role": "Mid", "name": "PlayerOne", "pool": ["Azir", "Orianna"], "weakness": "Low mobility, vulnerable to assassins"},
            {"role": "Jng", "name": "JunglerX", "tendency": "Paths top-to-bot 80% of games", "top_champ": "Lee Sin"}
        ]

    @staticmethod
    def _generate_recommendations(macro, players):
        rec = []
        if macro['early_aggression'] == "High":
            rec.append("⚠️ **Defensive Posture:** Opponent seeks early kills. Invest in deep vision at 2:45 to track jungle pathing.")
        
        for p in players:
            if "assassins" in p.get('weakness', '').lower():
                rec.append(f"🎯 **Exploit Weakness:** {p['name']} struggles against assassins. Pick LeBlanc or Zed to neutralize mid-lane scaling.")
        
        return rec

    @staticmethod
    def _generate_charts(macro, players):
        # Chart 1: Gold Difference at 15m (Line Chart)
        # Chart 2: Objective Control (Radar Chart)
        # ... logic similar to previous iteration but with real data structures
        return {} # JSON Plotly objects
