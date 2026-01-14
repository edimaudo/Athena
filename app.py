from flask import Flask, render_template, request, jsonify
from data_manager import GridDataManager
from analytics_engine import ReconEngine

app = Flask(__name__)
# Replace with your actual key or use environment variables
grid_manager = GridDataManager(api_key="YOUR_GRID_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recon', methods=['GET', 'POST'])
def recon():
    tournaments = grid_manager.get_tournaments()
    report = None
    
    if request.method == 'POST':
        # 1. Fetch data from GRID
        t_id = request.form.get('tournament_id')
        raw_matches = grid_manager.get_recent_series(t_id) # Mocking detail here
        
        # 2. Process with Engine
        stats = ReconEngine.calculate_macro_stats(raw_matches)
        insights = ReconEngine.generate_how_to_win(stats)
        charts = ReconEngine.create_plots(raw_matches)
        
        report = {
            "stats": stats,
            "insights": insights,
            "charts": charts
        }
        
    return render_template('recon.html', tournaments=tournaments, report=report)

if __name__ == '__main__':
    app.run(debug=True)
