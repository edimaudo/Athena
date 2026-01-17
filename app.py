from flask import Flask, render_template, request
from data_manager import GridDataManager
from analytics_engine import ReconEngine
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Initialize Data Manager
GRID_KEY = os.getenv('GRID_API_KEY')
grid = GridDataManager(api_key=GRID_KEY)

@app.route('/')
def index():
    """Main Dashboard Landing Page."""
    return render_template('index.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/recon', methods=['GET', 'POST'])
def recon():
    # Fetch Teams to populate the opponent selection dropdown
    opponents = grid.get_teams(title_id="3") 
    report = None
    
    if request.method == 'POST':
        team_id = request.form.get('team_id')
        
        # 1. SCOUR: Fetch the last 10 series for this specific opponent
        raw_series_list = grid.get_recent_series_by_team(team_id)
        
        # 2. PROCESS: Fetch granular match and participant data
        processed_matches = []
        for series in raw_series_list[:10]:
            series_id = series.get('id')
            match_stats = grid.get_series_stats(series_id) 
            if match_stats:
                # This returns a list of matches; we append it to our history
                processed_matches.append(match_stats)
        
        # 3. ANALYZE: Pass to engine to generate dynamic insights
        if processed_matches:
            report = ReconEngine.generate_full_report(processed_matches, team_id=team_id)
        else:
            report = {"error": "No match data found for this opponent."}

    return render_template('recon.html', opponents=opponents, report=report)

@app.route('/draft', methods=['GET', 'POST'])
def draft():
    return render_template('draft.html')

if __name__ == '__main__':
    app.run(debug=True)
