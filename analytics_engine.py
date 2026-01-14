import pandas as pd
import plotly.express as px
import plotly.utils
import json

class ReconEngine:
    @staticmethod
    def calculate_macro_stats(match_history):
        """Calculates macro-level patterns from a list of matches."""
        # Dummy logic simulating data aggregation from GRID
        total_games = len(match_history)
        first_blood_count = sum(1 for m in match_history if m.get('first_blood', False))
        dragon_priority = sum(1 for m in match_history if m.get('first_dragon', False))
        
        stats = {
            "first_blood_rate": (first_blood_count / total_games) * 100 if total_games > 0 else 0,
            "dragon_priority": (dragon_priority / total_games) * 100 if total_games > 0 else 0,
            "avg_game_time": "32:15"
        }
        return stats

    @staticmethod
    def generate_how_to_win(stats):
        """Generates actionable coaching insights based on statistical thresholds."""
        insights = []
        if stats['first_blood_rate'] > 65:
            insights.append({
                "type": "Warning",
                "text": "Opponent has a high Early Aggression score. Recommend defensive warding at 2:45."
            })
        if stats['dragon_priority'] > 70:
            insights.append({
                "type": "Strategy",
                "text": "High Dragon priority. Draft a bot lane with 'Priority' to contest early drakes."
            })
        return insights

    @staticmethod
    def create_plots(match_history):
        """Generates Plotly charts for the UI."""
        # 1. Champion Pool Bar Chart
        df = pd.DataFrame([{"Champion": "Lee Sin", "Games": 5}, {"Champion": "Viego", "Games": 3}])
        fig_champs = px.bar(df, x='Champion', y='Games', title="Most Played Champions",
                            color_discrete_sequence=['#0ac8b9'])
        fig_champs.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')

        # 2. Objective Radar Chart (Radar requires graph_objects)
        import plotly.graph_objects as go
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[80, 50, 70, 40],
            theta=['First Blood', 'First Tower', 'First Dragon', 'First Herald'],
            fill='toself',
            marker=dict(color='#c8aa6e')
        ))
        fig_radar.update_layout(template="plotly_dark", title="Objective Priority %")

        return {
            "champs": json.dumps(fig_champs, cls=plotly.utils.PlotlyJSONEncoder),
            "radar": json.dumps(fig_radar, cls=plotly.utils.PlotlyJSONEncoder)
        }
