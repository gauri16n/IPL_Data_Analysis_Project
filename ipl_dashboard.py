import io

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

# Optional (AI assistant) dependency. Dashboard will still run without it.
try:
    import google.generativeai as genai  # type: ignore
except ModuleNotFoundError:
    genai = None

from dashboard_modules import (
    additional_feature_runs_per_wicket_top_bowlers,
    clean_matches_deliveries,
    dismissal_types_plot,
    get_kpis,
    head_to_head_plot,
    over_summary_plot,
    player_of_match_plot,
    predict_win_probability,
    season_matches_plot,
    team_vs_team_heatmap,
    toss_decision_plots,
    toss_impact_plot,
    top_batsmen_strike_rate,
    top_batsmen_total_runs,
    top_bowlers_wickets_excluding_run_out,
    top_cities_plots,
)


st.set_page_config(page_title="IPL Analytics Pro", page_icon="🏏", layout="wide")

# Injecting Custom CSS for a beautiful, modern UI
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

/* Modern KPI Cards - Enterprise Style */
div[data-testid="stMetric"], div[data-testid="metric-container"] {
    background-color: #1F2937;
    border-radius: 10px;
    padding: 20px;
    border-left: 5px solid #3B82F6;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease-in-out;
}
div[data-testid="stMetric"]:hover, div[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    border-left: 5px solid #22C55E;
    box-shadow: 0px 8px 15px rgba(59, 130, 246, 0.2);
}
/* Make headers pop with primary blue */
h2, h3 {
    color: #3B82F6 !important;
    font-weight: 600;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("🏏 IPL Data Analysis & Insights Dashboard")
st.markdown("**Comprehensive Cricket Analytics and Performance Intelligence Platform**")
st.divider()

# --- Normal Q&A Chatbot (NO AI / NO external APIs) ---
# Put on main page (NOT in sidebar) to save space.
st.subheader("💬 Quick Q&A")
st.caption("Ask by choosing a question (no AI needed).")

qa_bank = [
    (
        "What is Toss Decision?",
        "Toss Decision shows whether the team that wins the coin toss chose to Bat or Field first.",
    ),
    (
        "How are Top Batsmen calculated?",
        "Top Batsmen are ranked by total runs scored from `deliveries.csv` using `batter` + `batsman_runs`.",
    ),
    (
        "How are Top Batsmen strike rate calculated?",
        "Strike rate (approx.) is computed as: (runs scored / balls faced) * 100 from `deliveries.csv` for each batter.",
    ),
    (
        "How are Top Bowlers calculated?",
        "Top Bowlers are wicket-takers from `deliveries.csv`, excluding run-outs (dismissal_kind == 'run out' / 'run out').",
    ),
    (
        "What is Dismissal Types?",
        "Dismissal Types shows the distribution of `dismissal_kind` values in `deliveries.csv`.",
    ),
    (
        "What is Over Summary?",
        "Over Summary aggregates per over: runs, wickets, extras, and batsman runs using `over` from `deliveries.csv`.",
    ),
    (
        "What does 'Toss Impact on Win' mean?",
        "It compares win outcomes relative to the toss decision (bat/field) to see if tossing correlates with winning.",
    ),
    (
        "What are 'Top Cities'?",
        "Top Cities counts matches by the `city` column in `matches.csv` and returns the top N.",
    ),
    (
        "What is Player of the Match?",
        "Player of the Match is derived from the `player_of_match` field in `matches.csv`, aggregated to show top performers.",
    ),
    (
        "What is the ML Win Probability?",
        "The ML module forecasts win probability between two teams using features like toss winner and venue from the uploaded data.",
    ),
]


q = st.selectbox("Select a question:", [x[0] for x in qa_bank], index=0)
answer = next(a for (qq, a) in qa_bank if qq == q)
st.info(f"Q: {q}")
st.success(f"A: {answer}")

with st.sidebar:
    st.header("🧭 Main Navigation")
    app_mode = st.radio("Select Tool", ["🏏 IPL Dashboard", "📂 Custom Data Explorer"])
    st.divider()

    if app_mode == "🏏 IPL Dashboard":
        st.header("📂 IPL Data Setup")
        matches_file = st.file_uploader("Upload Match Data (matches.csv)", type=["csv"])
        deliveries_file = st.file_uploader("Upload Ball Data (deliveries.csv)", type=["csv"])
        st.divider()

        menu_options = ["Overview & KPIs"]
        if matches_file is not None:
            menu_options.extend(
                [
                    "📊 Team Analytics (Heatmap)",
                    "⚔️ Head-to-Head Analysis",
                    "📈 Season Trends",
                    "Toss Decision",
                    "Toss Impact on Win",
                    "Top Cities",
                    "Match Winners (Player of the Match)",
                ]
            )
        if deliveries_file is not None:
            menu_options.extend(
                [
                    "Top Batsmen (Total Runs)",
                    "Top Batsmen (Strike Rate)",
                    "Top Bowlers (Wickets Excluding Run Outs)",
                    "Dismissal Types",
                    "Over Summary",
                ]
            )

        # Optional feature appears only when both are uploaded/cleaned.
        if matches_file is not None and deliveries_file is not None:
            menu_options.extend(["📄 Reports & Downloads"])

        section = st.selectbox("📊 Select Analysis View", menu_options, index=0)
    else:
        matches_file = None
        deliveries_file = None
        section = app_mode


@st.cache_data
def _read_uploaded_csv(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(file_bytes))


@st.cache_data
def _clean_data(matches_df: pd.DataFrame, deliveries_df: pd.DataFrame):
    return clean_matches_deliveries(matches_df, deliveries_df)


matches = None
deliveries = None

if app_mode == "🏏 IPL Dashboard":
    if matches_file is None and deliveries_file is None:
        st.info("Please upload at least one dataset (matches.csv or deliveries.csv) to begin IPL analysis.")
        st.stop()

    with st.spinner("Crunching the numbers... 🏏"):
        try:
            if matches_file:
                matches = _read_uploaded_csv(matches_file.getvalue())
            if deliveries_file:
                deliveries = _read_uploaded_csv(deliveries_file.getvalue())
        except Exception as e:
            st.error(f"Failed to read CSV files: {e}")
            st.stop()

        # Clean only when both datasets are present (dashboard plots need both schema parts).
        if matches is not None and deliveries is not None:
            try:
                matches, deliveries = _clean_data(matches, deliveries)
            except Exception as e:
                st.error(f"Cleaning failed: {e}")
                st.stop()

    # Render High-Level KPIs at the top (always visible for IPL)
    if matches is not None or deliveries is not None:
        # get_kpis expects matches['venue'] and deliveries totals; ensure required columns exist.
        try:
            total_matches, total_runs, total_wickets, total_venues = get_kpis(matches, deliveries)
        except Exception as e:
            st.error(f"KPI calculation failed: {e}")
            st.stop()

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.metric(
                label="🏟️ Total Matches Played",
                value=f"{total_matches:,}" if matches_file else "N/A",
                help="Total number of matches recorded in the uploaded dataset.",
            )
        with kpi2:
            st.metric(
                label="🏏 Total Runs Scored",
                value=f"{total_runs:,}" if deliveries_file else "N/A",
                help="Cumulative runs scored across all matches by all teams.",
            )
        with kpi3:
            st.metric(
                label="🎯 Total Wickets Taken",
                value=f"{total_wickets:,}" if deliveries_file else "N/A",
                help="Total wickets fallen.",
            )
        with kpi4:
            st.metric(
                label="📍 Venues Hosted",
                value=f"{total_venues}" if matches_file else "N/A",
                help="Number of unique venues/cities that have hosted an IPL match.",
            )

    st.divider()

try:
    if section == "Overview & KPIs":
        st.subheader("Welcome to the IPL Analytics Pro Dashboard")
        st.write(
            "Use the sidebar on the left to navigate through different analytical views. "
            "This dashboard provides a comprehensive look into player performances, venue statistics, and historical trends."
        )
        st.info("💡 Hint: Try 'Toss Impact on Win' or 'Match Winners' sections.")

        if matches_file and not deliveries_file:
            st.warning(
                "⚠️ **Observation:** Only Match Data is uploaded. Upload `deliveries.csv` to unlock player-level stats."
            )
        elif deliveries_file and not matches_file:
            st.warning(
                "⚠️ **Observation:** Only Ball Data is uploaded. Upload `matches.csv` to unlock venue/toss stats."
            )
        else:
            st.success("✅ **Observation:** Full dataset uploaded (or available). All visualizations are ready.")

    elif section == "📊 Team Analytics (Heatmap)":
        st.plotly_chart(team_vs_team_heatmap(matches), use_container_width=True)

    elif section == "⚔️ Head-to-Head Analysis":
        st.subheader("⚔️ Head-to-Head Team Comparison")
        teams = sorted(
            list(set(matches["team1"].dropna().unique()) | set(matches["team2"].dropna().unique()))
        )
        col1, col2 = st.columns(2)
        with col1:
            team1 = st.selectbox("Select Team 1", teams, index=0)
        with col2:
            team2 = st.selectbox("Select Team 2", teams, index=1 if len(teams) > 1 else 0)

        if team1 == team2:
            st.warning("⚠️ Please select two different teams to compare.")
        else:
            fig = head_to_head_plot(matches, team1, team2)
            if fig is None:
                st.info(f"No match data found between {team1} and {team2}.")
            else:
                st.plotly_chart(fig, use_container_width=True)

    elif section == "📈 Season Trends":
        st.plotly_chart(season_matches_plot(matches), use_container_width=True)

    elif section == "Toss Decision":
        fig1, fig2 = toss_decision_plots(matches)
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(fig1, use_container_width=True)
        with col2:
            st.pyplot(fig2, use_container_width=True)

    elif section == "Toss Impact on Win":
        st.plotly_chart(toss_impact_plot(matches), use_container_width=True)

    elif section == "Top Cities":
        fig_bar, fig_pie = top_cities_plots(matches, top_n=10)
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(fig_bar, use_container_width=True)
        with col2:
            st.pyplot(fig_pie, use_container_width=True)

    elif section == "Top Batsmen (Total Runs)":
        st.pyplot(top_batsmen_total_runs(deliveries, top_n=10), use_container_width=True)

    elif section == "Top Batsmen (Strike Rate)":
        st.pyplot(top_batsmen_strike_rate(deliveries, top_n=10), use_container_width=True)

    elif section == "Top Bowlers (Wickets Excluding Run Outs)":
        st.pyplot(top_bowlers_wickets_excluding_run_out(deliveries, top_n=10), use_container_width=True)

    elif section == "Dismissal Types":
        st.pyplot(dismissal_types_plot(deliveries), use_container_width=True)

    elif section == "Over Summary":
        st.pyplot(over_summary_plot(deliveries), use_container_width=True)

    elif section == "Match Winners (Player of the Match)":
        st.plotly_chart(player_of_match_plot(matches, top_n=10), use_container_width=True)

    elif section == "📄 Reports & Downloads":
        st.header("📄 Executive Reports & Data Export")
        st.markdown("Download the cleaned, normalized datasets.")
        st.download_button(
            "📥 Download Cleaned Match Data (CSV)",
            data=matches.to_csv(index=False),
            file_name="cleaned_matches.csv",
            mime="text/csv",
        )
        st.download_button(
            "📥 Download Cleaned Ball-by-Ball Data (CSV)",
            data=deliveries.to_csv(index=False),
            file_name="cleaned_deliveries.csv",
            mime="text/csv",
        )

    elif section == "📂 Custom Data Explorer":
        st.header("📂 Auto Data Explorer")
        st.markdown(
            "Upload **any generic CSV dataset**. The app will show stats and charts automatically."
        )
        custom_file = st.file_uploader("Upload Custom Dataset (CSV)", type=["csv"], key="custom_file")
        if custom_file is not None:
            custom_df = pd.read_csv(custom_file)
            st.success(f"✅ Successfully loaded `{custom_file.name}`")
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Rows", f"{custom_df.shape[0]:,}")
            c2.metric("Total Columns", f"{custom_df.shape[1]:,}")
            c3.metric("Missing Values", f"{custom_df.isna().sum().sum():,}")

            st.divider()
            st.subheader("🔍 Data Preview")
            st.dataframe(custom_df.head(), use_container_width=True)
            st.divider()
            st.subheader("📊 Statistical Summary")
            st.dataframe(custom_df.describe(include="all"), use_container_width=True)

            numeric_cols = custom_df.select_dtypes(include=["float64", "int64"]).columns.tolist()
            if numeric_cols:
                sel_num = st.selectbox("Select a numeric column:", numeric_cols)
                if sel_num:
                    fig = px.histogram(
                        custom_df,
                        x=sel_num,
                        marginal="box",
                        title=f"Distribution of {sel_num}",
                        color_discrete_sequence=["#ff7f0e"],
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No numeric columns found in this dataset for visualization.")

    else:
        st.warning("Unknown section selected.")

except KeyError as e:
    st.error(
        "Column missing in your uploaded CSV. "
        f"Missing key: {e}. Please ensure CSV columns match expected schema."
    )
except Exception as e:
    st.error(f"Failed to render section due to error: {e}")

