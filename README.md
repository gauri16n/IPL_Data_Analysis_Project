# IPL Data Analysis Dashboard (Streamlit)

This repository contains an interactive Streamlit dashboard for exploring IPL data using:
- `matches.csv` (match-level)
- `deliveries.csv` (ball-by-ball)

## Features
- Toss Decision distribution
- Top Cities by match count
- Top Batsmen by total runs
- Top Bowlers by wickets (excluding run-outs)
- Dismissal Types distribution
- Over-wise summary (runs/wickets/extras)

## Project docs
- `USAGE.md` — how to run and use the dashboard
- `PROJECT_OVERVIEW.md` — section-by-section explanation
- `REPORT.md` — high-level report/summary

## Run locally (Windows)
1. Open Command Prompt / PowerShell in this folder
2. Run:

```bat
run_streamlit.bat
```

Then open:
- http://localhost:8501

## Run locally (all platforms)
```bash
python -m streamlit run ipl_dashboard.py --server.port 8501
```

