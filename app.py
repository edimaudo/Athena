from flask import Flask, render_template, request
from data_manager import GridDataManager
from analytics_engine import ReconEngine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Initialize with your GRID Key
grid = os.getenv('GRID_API_KEY')##GridDataManager(api_key="YOUR_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/recon', methods=['GET', 'POST'])
def recon():
    tournaments = grid.get_tournaments(title_id="3") # LoL ID
    report = None
    
    if request.method == 'POST':
        t_id = request.form.get('tournament_id')
        # 1. Scour data from GRID
        raw_series = grid.get_recent_series(t_id)
        
        # 2. Mocking expanded data keys for the demonstration 
        # (In production, these come from the deep match-event parsing)
        processed_matches = [
            {"win": 1, "side": "blue", "first_blood": 1, "first_dragon": 1, "first_herald": 0, "first_tower": 1, "gold_diff_15": 1200, "patch": "16.1"},
            {"win": 0, "side": "red", "first_blood": 0, "first_dragon": 0, "first_herald": 1, "first_tower": 0, "gold_diff_15": -400, "patch": "16.1"},
            {"win": 1, "side": "blue", "first_blood": 1, "first_dragon": 1, "first_herald": 1, "first_tower": 1, "gold_diff_15": 2100, "patch": "15.9"},
        ]
        
        # 3. Generate Report
        report = ReconEngine.generate_full_report(processed_matches, team_id=t_id)

    return render_template('recon.html', tournaments=tournaments, report=report)

if __name__ == '__main__':
    app.run(debug=True)
