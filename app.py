from flask import Flask, render_template, request, jsonify
from data_manager import GridDataManager

app = Flask(__name__)
# Replace with your actual key or use environment variables
grid_manager = GridDataManager(api_key="YOUR_GRID_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recon', methods=['GET', 'POST'])
def recon():
    tournaments = grid_manager.get_tournaments(title_id="3") # LoL
    scouting_data = None
    
    if request.method == 'POST':
        t_id = request.form.get('tournament_id')
        # Fetch data and pass it to our analytics logic (to be built)
        scouting_data = grid_manager.get_recent_series(t_id)
        
    return render_template('recon.html', tournaments=tournaments, data=scouting_data)

if __name__ == '__main__':
    app.run(debug=True)
