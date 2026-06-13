# Project Overview: IPL Data Analysis Dashboard

## What this project does
This project builds an **interactive Streamlit dashboard** for analyzing IPL data using two datasets:
- **Match-level dataset** (`matches.csv`): teams, toss decision, match outcomes, venue/city.
- **Ball-by-ball dataset** (`deliveries.csv`): batting events by over/ball, batter runs, dismissal type, bowler.

The dashboard provides several pre-defined analysis views so you can quickly explore common cricket analytics.

## Dashboard sections
The Streamlit app (`ipl_dashboard.py`) contains these views:

### 1) Toss Decision
Shows distribution of `toss_decision` in `matches.csv`.
- Bar chart (count)
- Pie chart (percentage)

### 2) Top Cities
Shows top 10 cities by `city` match count.
- Bar chart
- Pie chart

### 3) Top Batsmen
Shows top 10 batters by total runs.
- Computed from `deliveries.csv`:
  - `deliveries.groupby('batter')['batsman_runs'].sum()`

### 4) Top Bowlers
Shows top 10 wicket-takers excluding run-outs.
- Filters out `dismissal_kind == 'run out'`
- Counts dismissals per bowler

### 5) Dismissal Types
Shows the distribution of `dismissal_kind` in `deliveries.csv`.
- Count plot ordered by frequency

### 6) Over Summary
Provides over-wise aggregation of:
- `total_runs`
- `is_wicket`
- `extra_runs`
- `batsman_runs`

Then plots line charts across overs.

## How to modify / extend
To add a new analysis section:
1. Add a new option to the sidebar radio list.
2. Implement an `elif section == "Your New View"` block.
3. Use pandas groupby/aggregations on `matches` and/or `deliveries`.
4. Render plots with matplotlib/seaborn.

