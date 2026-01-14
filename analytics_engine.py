import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import plotly.utils

class ReconEngine:
    @staticmethod
    def generate_full_report(match_history, team_id, current_patch="16.1"):
        df = pd.DataFrame(match_history)
        
        # 1. Macro Analysis
        macro = {
            "aggression": "High" if df['first_blood'].mean() > 0.6 else "Scaling",
            "obj_priority": "Dragon" if df['first_dragon'].mean() > df['first_herald'].mean() else "Tempo/Herald",
            "avg_gd15": int(df['gold_diff_15'].mean())
        }

        # 2. Side & Patch Analysis
        blue_side = df[df['side'] == 'blue']
        red_side = df[df['side'] == 'red']
        patch_matches = df[df['patch'] == current_patch]
        
        side_stats = {
            "blue_winrate": round(blue_side['win'].mean() * 100, 1) if not blue_side.empty else 0,
            "red_winrate": round(red_side['win'].mean() * 100, 1) if not red_side.empty else 0
        }

        # 3. How to Win Logic (The "Actionable" Part)
        recommendations = []
        # General Strategy
        if macro['aggression'] == "High":
            recommendations.append("⚠️ **Anti-Snowball:** Opponent relies on First Blood. Avoid Level 3 jungle invades.")
        
        # Side-Specific Logic
        if side_stats['blue_winrate'] > side_stats['red_winrate'] + 10:
            recommendations.append("🔴 **Side Exploit:** Opponent struggles on Red side. Force them to pick Red to disrupt their comfort.")
        
        # Patch-Specific Logic
        if patch_matches['win'].mean() < df['win'].mean():
            recommendations.append(f"📉 **Patch Weakness:** Team has a lower winrate on {current_patch}. Their core champion pool was likely nerfed.")

        return {
            "macro": macro,
            "side_stats": side_stats,
            "recommendations": recommendations,
            "charts": ReconEngine._create_visuals(df, side_stats)
        }

    @staticmethod
    def _create_visuals(df, side_stats):
        # Side Winrate Comparison
        fig_side = go.Figure(data=[
            go.Bar(name='Blue Side', x=['Winrate'], y=[side_stats['blue_winrate']], marker_color='#005a82'),
            go.Bar(name='Red Side', x=['Winrate'], y=[side_stats['red_winrate']], marker_color='#ae1e1e')
        ])
        fig_side.update_layout(template="plotly_dark", barmode='group', paper_bgcolor='rgba(0,0,0,0)', height=300)

        # Objective Priority Radar
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[df['first_blood'].mean()*100, df['first_tower'].mean()*100, df['first_dragon'].mean()*100, df['first_herald'].mean()*100],
            theta=['First Blood', 'First Tower', 'First Dragon', 'First Herald'],
            fill='toself', marker=dict(color='#c8aa6e')
        ))
        fig_radar.update_layout(template="plotly_dark", polar=dict(radialaxis=dict(visible=True, range=[0, 100])), paper_bgcolor='rgba(0,0,0,0)', height=300)

        return {
            "side_chart": json.dumps(fig_side, cls=plotly.utils.PlotlyJSONEncoder),
            "radar_chart": json.dumps(fig_radar, cls=plotly.utils.PlotlyJSONEncoder)
        }
