import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import json

class ReconEngine:
    @staticmethod
    def generate_full_report(match_history, team_id):
        # LOGIC FIX: Flatten the list of lists from app.py
        flat_matches = []
        for item in match_history:
            if isinstance(item, list):
                flat_matches.extend(item)
            else:
                flat_matches.append(item)
        
        if not flat_matches:
            return {"error": "No valid match data to analyze."}

        df = pd.DataFrame(flat_matches)
        
        # 1. DYNAMIC MACRO CALCULATION
        # Calculate rates based on actual API data provided
        fb_rate = df['first_blood'].mean() if 'first_blood' in df else 0
        fd_rate = df['first_dragon'].mean() if 'first_dragon' in df else 0
        avg_gd15 = df['gold_diff_15'].mean() if 'gold_diff_15' in df else 0

        # 2. DYNAMIC COMPOSITION & PLAYER TENDENCIES
        all_participants = []
        for m in flat_matches:
            all_participants.extend(m.get('participants', []))
        
        pdf = pd.DataFrame([
            {
                'name': p['player']['name'], 
                'hero': p['hero']['name'], 
                'role': p['role'],
                'kda': (p['kills'] + p['assists']) / max(1, p['deaths'])
            } for p in all_participants
        ])

        # Identify most played heroes (Compositions)
        common_comps = pdf['hero'].value_counts().head(5).to_dict()

        # Identify Player Outliers (Target Ban Logic)
        player_intel = []
        for name in pdf['name'].unique():
            p_subset = pdf[pdf['name'] == name]
            top_hero = p_subset['hero'].mode()[0]
            # Calculate if they rely on one hero (>40% pick rate)
            is_specialist = (p_subset['hero'] == top_hero).mean() > 0.4
            player_intel.append({
                "name": name,
                "top_hero": top_hero,
                "status": "Priority Ban" if is_specialist else "Flexible"
            })

        # 3. DYNAMIC INSIGHTS (No hardcoding)
        recommendations = []
        if fb_rate > 0.6:
            recommendations.append(f"🎯 **Strategy:** Opponent wins {int(fb_rate*100)}% of early duels. Recommend defensive jungle pathing.")
        
        if fd_rate < 0.4:
            recommendations.append(f"🐉 **Exploit:** Team neglects early Dragons ({int(fd_rate*100)}% contested). Focus bot-side priority.")

        return {
            "macro": {
                "style": "Early Aggression" if fb_rate > 0.55 else "Scaling",
                "gd15": int(avg_gd15)
            },
            "player_stats": player_intel[:5],
            "common_comps": common_comps,
            "recommendations": recommendations,
            "charts": ReconEngine._create_visuals(df)
        }

    @staticmethod
    def _create_visuals(df):
        # Dynamic Radar Chart based on API results
        metrics = ['first_blood', 'first_tower', 'first_dragon', 'first_herald']
        values = [df[m].mean() * 100 if m in df else 0 for m in metrics]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=['First Blood', 'First Tower', 'First Dragon', 'First Herald'],
            fill='toself',
            marker=dict(color='#c8aa6e')
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            polar=dict(radialaxis=dict(visible=False))
        )
        return {"radar_chart": json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)}
