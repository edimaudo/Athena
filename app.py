from flask import Flask, render_template, request
from data_manager import GridDataManager
from analytics_engine import ReconEngine
import os
from dotenv import load_dotenv

# Load environment variables (useful for local development)
load_dotenv()

app = Flask(__name__)

# Initialize GridDataManager with the API key from Vercel/Environment
# This replaces the string assignment and uses the key to create the object instance.
GRID_KEY = os.getenv('GRID_API_KEY')
grid = GridDataManager(api_key=GRID_KEY)

@app.route('/')
def index():
    """Main Dashboard Landing Page."""
    return render_template('index.html')

@app.route('/help')
def help_page():
    """Information and Guide page."""
    return render_template('help.html')

@app.route('/about')
def about():
    """Project and Platform information."""
    return render_template('about.html')

@app.route('/recon', methods=['GET', 'POST'])
def recon():
    """Scouts an opponent using live GRID data."""
    # title_id "3" corresponds to League of Legends in GRID
    tournaments = grid.get_tournaments(title_id="3") 
    report = None
    
    if request.method == 'POST':
        t_id = request.form.get('tournament_id')
        
        # 1. SCOUR: Fetch actual series IDs from the selected tournament
        raw_series_list = grid.get_recent_series(t_id)
        
        # 2. PROCESS: Iterate through series to fetch granular match data
        # Replacing the previous mock list with actual API calls
        processed_matches = []
        for series in raw_series_list[:10]:  # Limit to last 10 for performance
            series_id = series.get('id')
            # Assuming data_manager has a method to fetch state details
            match_stats = grid.get_series_stats(series_id) 
            if match_stats:
                processed_matches.append(match_stats)
        
        # 3. ANALYZE: Generate the report using the real match history
        if processed_matches:
            report = ReconEngine.generate_full_report(processed_matches, team_id=t_id)
        else:
            # Handle cases where no data is returned
            report = {"error": "No match data found for the selected tournament."}

    return render_template('recon.html', tournaments=tournaments, report=report)

@app.route('/draft', methods=['GET', 'POST'])
def draft():
    """Draft Coach module for turn-by-turn pick prediction."""
    # Placeholder for the upcoming Draft Coach logic
    return render_template('draft.html')

if __name__ == '__main__':
    # Vercel typically manages the port, but local testing uses 5000
    app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)
