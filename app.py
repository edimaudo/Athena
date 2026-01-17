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
    # Logic Change: Fetch Teams instead of Tournaments for the dropdown
    opponents = grid.get_teams(title_id="3") 
    report = None
    
    if request.method == 'POST':
        # Get the Team ID from the form
        team_id = request.form.get('team_id')
        
        # 1. SCOUR: Fetch series specifically for this team
        raw_series_list = grid.get_recent_series_by_team(team_id)
        
        # ... rest of your processing logic ...
    
    return render_template('recon.html', opponents=opponents, report=report)

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
