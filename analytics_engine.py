import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import json

class ReconEngine:
    @staticmethod
    def generate_full_report(match_history, team_id, current_patch="16.1"):
        # Handle single dictionary or list of matches
        flat_matches = []
        if isinstance(match_history, list) and isinstance(match_history[0], list):
            for series in match_history: flat_matches.extend(series)
        else:
            flat_matches = [match_history] if isinstance(match_history, dict) else match_history
            
        df = pd.DataFrame(flat_matches)
        
        # 1. Macro Analysis
        macro = {
            "aggression": "High" if df['first_blood'].mean() > 0.6 else "Scaling",
            "obj_priority": "Dragon" if df['first_dragon'].mean() > df['first_herald'].mean() else "Tempo/Herald",
            "avg_gd15": int(df['gold_diff_15'].mean())
        }

        # 2. Player & Comp Analysis (New Logic)
        all_participants = []
        for match in flat_matches:
            all_participants.extend(match.get('participants', []))
        
        p_df = pd.DataFrame([
            {
                'name': p['player']['name'], 
                'hero': p['hero']['name'], 
                'kda': (p['kills'] + p['assists']) / max(1, p['deaths'])
            } for p in all_participants
        ])

        # Get top 5 most played champions (Compositions)
        common_comps = p_df['hero'].value_counts().head(5).to_dict()

        # Identify Key Player Tendencies
        player_stats = []
        for name in p_df['name'].unique():
            p_subset = p_df[p_df['name'] == name]
            player_stats.append({
                "name": name,
                "top_hero": p_subset['hero'].mode()[0],
                "avg_kda": round(p_subset['kda'].mean(), 1)
            })

        # 3. Enhanced "How to Win" Logic
        recommendations = []
        if macro['aggression'] == "High":
            recommendations.append("⚠️ **Anti-Snowball:** Opponent relies on early kills. Prioritize safe lane-neutralizing picks.")
        
        # Direct Counter-Strategy Example
        if any(h in common_comps for h in ["LeBlanc", "Zed", "Akali"]):
            recommendations.append("🎯 **Counter-Strategy:** High frequency of assassins detected. Recommend picking **Lissandra** or **Vex** for lockdown.")

        return {
            "macro": macro,
            "player_stats": player_stats[:5], # Top 5 players
            "common_comps": common_comps,
            "recommendations": recommendations,
            "charts": ReconEngine._create_visuals(df)
        }

    @staticmethod
    def _create_visuals(df):
        # Objective Radar
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[df['first_blood'].mean()*100, df['first_tower'].mean()*100, df['first_dragon'].mean()*100, df['first_herald'].mean()*100],
            theta=['First Blood', 'First Tower', 'First Dragon', 'First Herald'],
            fill='toself', marker=dict(color='#c8aa6e')
        ))
        fig_radar.update_layout(template="plotly_dark", polar=dict(radialaxis=dict(visible=False)), paper_bgcolor='rgba(0,0,0,0)', height=300)

        return {
            "radar_chart": json.dumps(fig_radar, cls=plotly.utils.PlotlyJSONEncoder)
        }
