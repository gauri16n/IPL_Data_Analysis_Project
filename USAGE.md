# Usage (IPL Dashboard + Data)

## 1) Files in this project
- `ipl_dashboard.py` — Streamlit app that renders multiple IPL analytics views.
- `matches.csv` — IPL match-level data (uploaded to the dashboard).
- `deliveries.csv` — IPL ball-by-ball data (expected by the dashboard; upload it in the app).
- `run_streamlit.bat` — Windows batch file to start the app.
- `requirements.txt` — List of all required Python packages.

## 2) Install dependencies
Before running the app, ensure you have all required libraries installed. Open Command Prompt / PowerShell in this folder and run:

```bash
pip install -r requirements.txt
```

## 3) Start the dashboard (Windows)
1. Open Command Prompt / PowerShell in this project folder.
2. Run:

```bat
run_streamlit.bat
```

3. Open your browser to:
- http://localhost:8501

## 4) Run command (without .bat)
From the project folder:

```bat
python -m streamlit run ipl_dashboard.py --server.port 8501
```

## 4) Use the dashboard
1. In the app, upload **both** files:
   - `matches.csv`
   - `deliveries.csv`
2. Select a section from the sidebar:
   - Toss Decision
   - Top Cities
   - Top Batsmen
   - Top Bowlers
   - Dismissal Types
   - Over Summary

## 5) Notes / requirements
- `ipl_dashboard.py` expects the CSV columns referenced in each section (e.g., `toss_decision`, `city`, `batter`, `bowler`, `dismissal_kind`, `over`, etc.).
- If a column is missing, the app shows an error message for that section.
