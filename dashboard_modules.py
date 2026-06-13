import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


def _set_theme():
    plt.style.use('dark_background')
    sns.set_style("darkgrid", {
        "axes.facecolor": "#0e1117", 
        "figure.facecolor": "#0e1117", 
        "grid.color": "#1f2937"
    })


def clean_matches_deliveries(matches: pd.DataFrame, deliveries: pd.DataFrame):
    """Replicates the notebook's basic cleaning so plots work."""
    if matches is not None:
        matches = matches.copy()
        # Team name normalization
        matches['team1'] = matches['team1'].replace({'Rising Pune Supergiants': 'Rising Pune Supergiant'})
        matches['team2'] = matches['team2'].replace({'Rising Pune Supergiants': 'Rising Pune Supergiant'})
        matches['toss_winner'] = matches['toss_winner'].replace({'Rising Pune Supergiants': 'Rising Pune Supergiant'})
        matches['winner'] = matches['winner'].replace({'Rising Pune Supergiants': 'Rising Pune Supergiant'})

        matches['team1'] = matches['team1'].replace({'Rising Pune Supergiants': 'Royal Challengers Bangalore'})
        matches['team2'] = matches['team2'].replace({'Rising Pune Supergiants': 'Royal Challengers Bangalore'})
        matches['toss_winner'] = matches['toss_winner'].replace({'Rising Pune Supergiants': 'Royal Challengers Bangalore'})
        matches['winner'] = matches['winner'].replace({'Rising Pune Supergiants': 'Royal Challengers Bangalore'})

        # Missing values
        if 'city' in matches.columns:
            matches['city'] = matches['city'].fillna('unknown')

        if 'method' in matches.columns:
            matches['method'] = matches['method'].fillna('Non D/L')

    if deliveries is not None:
        deliveries = deliveries.copy()
        deliveries['batting_team'] = deliveries['batting_team'].replace({'Rising Pune Supergiants': 'Rising Pune Supergiant'})
        deliveries['bowling_team'] = deliveries['bowling_team'].replace({'Rising Pune Supergiants': 'Rising Pune Supergiant'})

    return matches, deliveries


def get_kpis(matches: pd.DataFrame, deliveries: pd.DataFrame):
    """Calculates top-level Key Performance Indicators for the dashboard."""
    total_matches = len(matches) if matches is not None else 0
    total_venues = matches['venue'].nunique() if matches is not None and 'venue' in matches.columns else 0

    total_runs = 0
    total_wickets = 0
    if deliveries is not None:
        total_runs = int(deliveries['total_runs'].sum()) if 'total_runs' in deliveries.columns else 0
        
        if 'is_wicket' in deliveries.columns:
            total_wickets = int(deliveries['is_wicket'].sum())
        else:
            total_wickets = len(deliveries[deliveries['dismissal_kind'].notna()])
    
    return total_matches, total_runs, total_wickets, total_venues


def player_of_match_plot(matches: pd.DataFrame, top_n: int = 10):
    """Returns an interactive Plotly chart of the top Player of the Match winners."""
    pom = matches['player_of_match'].value_counts().reset_index()
    pom.columns = ['Player', 'Awards']
    pom = pom.head(top_n)
    
    fig = px.bar(pom, x='Player', y='Awards', text='Awards',
                 title=f'Top {top_n} Match Winners (Player of the Match)',
                 color='Awards', color_continuous_scale='Blues', template='plotly_dark')
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def toss_impact_plot(matches: pd.DataFrame):
    """Returns an interactive Plotly pie chart analyzing if toss winners win the match."""
    matches['toss_impact'] = (matches['toss_winner'] == matches['winner']).map({True: 'Won Match', False: 'Lost Match'})
    impact_counts = matches['toss_impact'].value_counts().reset_index()
    impact_counts.columns = ['Outcome', 'Count']
    
    fig = px.pie(impact_counts, values='Count', names='Outcome', hole=0.4,
                 title='Toss Impact: Does winning the Toss mean winning the Match?',
                 color_discrete_sequence=['#22C55E', '#EF4444'], template='plotly_dark')
    return fig


def toss_decision_plots(matches: pd.DataFrame):
    _set_theme()
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.countplot(x='toss_decision', data=matches, ax=ax1, palette='pastel')
    ax1.set_title('Toss Decision: Bat or Field')
    ax1.set_xlabel('Decision after Winning Toss')
    ax1.set_ylabel('Number of Matches')
    fig1.tight_layout()

    toss_counts = matches['toss_decision'].value_counts()
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    ax2.pie(
        toss_counts.values,
        labels=toss_counts.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=['#3B82F6', '#22C55E'][: len(toss_counts)],
        textprops={'color': "w"}
    )
    ax2.set_title('Toss Decisions in IPL')
    ax2.axis('equal')
    fig2.tight_layout()

    return fig1, fig2


def top_cities_plots(matches: pd.DataFrame, top_n: int = 10):
    _set_theme()
    top_cities = matches['city'].value_counts().reset_index(name='Match Count')
    top_cities.rename(columns={'index': 'City'}, inplace=True)
    top_cities = top_cities.head(top_n)

    fig1, ax1 = plt.subplots(figsize=(10, 8))
    ax1.pie(
        top_cities['Match Count'],
        labels=top_cities['City'],
        autopct='%1.1f%%',
        startangle=140,
        colors=sns.color_palette("pastel"),
        textprops={'color': "w"}
    )
    ax1.set_title(f'Top {top_n} IPL Cities by Number of Matches', fontsize=16)
    ax1.axis('equal')
    fig1.tight_layout()

    fig2, ax2 = plt.subplots(figsize=(12, 5))
    sns.barplot(x='City', y='Match Count', data=top_cities, ax=ax2, palette='rocket')
    ax2.set_title(f'Top {top_n} IPL Cities by Number of Matches')
    ax2.set_xlabel('City')
    ax2.set_ylabel('Match Count')
    ax2.tick_params(axis='x', rotation=45)
    fig2.tight_layout()

    return fig2, fig1


def top_batsmen_total_runs(deliveries: pd.DataFrame, top_n: int = 10):
    _set_theme()
    top_batsmen = (
        deliveries.groupby('batter')['batsman_runs'].sum().reset_index(name='Total Runs')
        .sort_values(by='Total Runs', ascending=False)
        .head(top_n)
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_batsmen, x='batter', y='Total Runs', ax=ax, palette='rocket')
    ax.set_title(f'Top {top_n} IPL Batsmen by Total Runs', fontsize=16)
    ax.set_xlabel('Batsman', fontsize=12)
    ax.set_ylabel('Total Runs', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()
    return fig


def top_batsmen_strike_rate(deliveries: pd.DataFrame, top_n: int = 10):
    """Uses notebook logic: strike rate per match then barplot of top innings SR."""
    _set_theme()
    batsmen_score = (
        deliveries.groupby(['match_id', 'batter'])['batsman_runs'].sum().reset_index(name='Innings Runs')
    )
    batsman_ball_faced = (
        deliveries.groupby(['match_id', 'batter'])['batsman_runs'].count().reset_index(name='Balls Faced')
    )

    batsmen_performance = pd.merge(batsmen_score, batsman_ball_faced, how='inner', on=['match_id', 'batter'])
    batsmen_performance['Strike Rate For Match'] = (
        batsmen_performance['Innings Runs'] / batsmen_performance['Balls Faced']
    ) * 100

    top_strike_innings = batsmen_performance.sort_values(
        by='Strike Rate For Match', ascending=False
    ).head(top_n)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x='batter',
        y='Strike Rate For Match',
        data=top_strike_innings,
        ax=ax,
        palette='magma',
    )
    ax.set_title(f'Top {top_n} Highest Strike Rate Innings')
    ax.set_xlabel('Batter')
    ax.set_ylabel('Strike Rate')
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()
    return fig


def top_bowlers_wickets_excluding_run_out(deliveries: pd.DataFrame, top_n: int = 10):
    _set_theme()
    bowling_wickets = deliveries[
        deliveries['dismissal_kind'].notna() & (deliveries['dismissal_kind'] != 'run out')
    ]
    top_bowlers = (
        bowling_wickets.groupby('bowler')['dismissal_kind']
        .count()
        .reset_index(name='wickets')
        .sort_values(by='wickets', ascending=False)
        .head(top_n)
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_bowlers, x='bowler', y='wickets', ax=ax, palette='crest')
    ax.set_title(f'Top {top_n} IPL Wicket Takers (Excluding Run Outs)')
    ax.set_xlabel('Bowler')
    ax.set_ylabel('Wickets')
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()
    return fig


def dismissal_types_plot(deliveries: pd.DataFrame):
    _set_theme()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(x='dismissal_kind', data=deliveries, ax=ax, palette='Set2')
    ax.set_title('Count of Each Dismissal Kind in IPL')
    ax.set_xlabel('Dismissal Kind')
    ax.set_ylabel('Count')
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()
    return fig


def over_summary_plot(deliveries: pd.DataFrame):
    _set_theme()
    over_summary = deliveries.groupby('over')[['total_runs', 'is_wicket', 'extra_runs', 'batsman_runs']].sum()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=over_summary, x=over_summary.index, y='total_runs', marker='o', color='#3B82F6', ax=ax)
    ax.set_title('Total Runs Scored Per Over (All Matches)', fontsize=14)
    ax.set_xlabel('Over')
    ax.set_ylabel('Total Runs')
    ax.grid(True)
    fig.tight_layout()
    return fig


def additional_feature_runs_per_wicket_top_bowlers(deliveries: pd.DataFrame, top_n: int = 10):
    """Notebook-derived: runs conceded per wicket for match-bowler pair, then top 10."""
    _set_theme()
    match_bowler_runs = deliveries.groupby(['match_id', 'bowler'])['total_runs'].sum().reset_index(name='Runs Conceded')

    wickets = deliveries[
        deliveries['dismissal_kind'].notna() & (deliveries['dismissal_kind'] != 'run out')
    ]
    match_bowler_wickets = wickets.groupby(['match_id', 'bowler'])['dismissal_kind'].count().reset_index(name='Wickets')

    match_bowler_performance = pd.merge(match_bowler_runs, match_bowler_wickets, how='inner', on=['match_id', 'bowler'])
    match_bowler_performance['Runs per Wicket'] = np.round(
        match_bowler_performance['Runs Conceded'] / match_bowler_performance['Wickets'], 2
    )

    top_bowler_efficiency = match_bowler_performance.sort_values(by='Runs per Wicket').head(top_n)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        data=top_bowler_efficiency,
        x='bowler',
        y='Runs per Wicket',
        marker='o',
        linewidth=2.5,
        color='#22C55E',
        ax=ax,
    )
    ax.set_title('Top 10 Bowlers by Best Runs per Wicket Ratio', fontsize=14)
    ax.set_xlabel('Bowler')
    ax.set_ylabel('Runs per Wicket')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)
    fig.tight_layout()
    return fig


def head_to_head_plot(matches: pd.DataFrame, team1: str, team2: str):
    """Generates an interactive pie chart comparing wins between two specific teams."""
    h2h = matches[((matches['team1'] == team1) & (matches['team2'] == team2)) |
                  ((matches['team1'] == team2) & (matches['team2'] == team1))]
    if h2h.empty:
        return None
    win_counts = h2h['winner'].value_counts().reset_index()
    win_counts.columns = ['Team', 'Wins']
    
    fig = px.pie(win_counts, values='Wins', names='Team', hole=0.4,
                 title=f'Head-to-Head Wins: {team1} vs {team2}',
                 color_discrete_sequence=['#3B82F6', '#F59E0B'], template='plotly_dark')
    return fig


def season_matches_plot(matches: pd.DataFrame):
    """Generates a line chart tracking the number of matches played per season."""
    season_counts = matches['season'].value_counts().reset_index()
    season_counts.columns = ['Season', 'Matches Played']
    season_counts = season_counts.sort_values('Season')
    
    fig = px.area(season_counts, x='Season', y='Matches Played', markers=True,
                  title='IPL Matches Played per Season',
                  color_discrete_sequence=['#3B82F6'], template='plotly_dark')
    fig.update_layout(xaxis_type='category') # Prevents years from formatting as floats (e.g. 2,008)
    return fig


def team_vs_team_heatmap(matches: pd.DataFrame):
    """Generates an advanced Plotly Heatmap showing win counts between teams."""
    # Create a cross-tabulation of team1 vs team2 wins
    heatmap_data = pd.crosstab(matches['team1'], matches['winner'])
    
    fig = px.imshow(heatmap_data, 
                    labels=dict(x="Winning Team", y="Opponent Team", color="Wins"),
                    x=heatmap_data.columns,
                    y=heatmap_data.index,
                    title="Advanced Analytics: Team vs Team Win Heatmap",
                    color_continuous_scale="Blues", 
                    template='plotly_dark')
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def predict_win_probability(team1: str, team2: str, toss_winner: str, venue: str):
    """
    Simulates an ML Model output for Win Probability.
    In production, replace this with: model = joblib.load('model.pkl'); return model.predict_proba(...)
    """
    # Dummy heuristic logic for demonstration purposes in a portfolio
    base_prob = 50.0
    if toss_winner == team1:
        base_prob += 5.5
    elif toss_winner == team2:
        base_prob -= 5.5
        
    # Add slight random variance to simulate complex model interactions
    np.random.seed(len(team1) + len(team2)) 
    variance = np.random.uniform(-4.0, 4.0)
    t1_prob = min(max(base_prob + variance, 10.0), 90.0)
    
    return round(t1_prob, 1), round(100.0 - t1_prob, 1)
