# Analysis Report (High-level)

## Objective
Explore IPL match and ball-by-ball data to answer questions such as:
- What are common toss decisions?
- Where are matches commonly hosted?
- Which batters score the most runs?
- Which bowlers take the most wickets (excluding run-outs)?
- What are the most frequent dismissal types?
- How do runs/wickets/extras change across overs?

## Data
- `matches.csv`: match-level information (toss, winner, city, etc.)
- `deliveries.csv`: ball-level events including batter runs, bowler, dismissal kind, over.

## Key computations used
- **Top batsmen**: total runs by batter
- **Top bowlers**: count dismissals by bowler excluding run-outs
- **Dismissal types**: frequency of `dismissal_kind`
- **Over summary**: sum of run-related and wicket/extras related indicators by `over`

## Deliverables
- Streamlit dashboard with interactive sidebar sections.
- Documentation files:
  - `USAGE.md`
  - `PROJECT_OVERVIEW.md`
  - `REPORT.md`

