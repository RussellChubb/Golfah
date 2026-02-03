# Golfah: Interactive Round Summary
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from pathlib import Path

# TODO
# Have some kind of check to see whether or not the data files exist, if they don't perhaps we can raise something for users to chuck their own .csvs in
# Have Round ID Filter be responsive to other filters.
# Have some kind of thing to bring up pictures of people when their name is in the Player List

# Data Loading
APP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = APP_DIR / "data"


# Data Caching
@st.cache_data
def load_data():
    summary = pd.read_excel(
        DATA_DIR / "Summary_Data.xlsx",
        parse_dates=["Date"],
    )

    rounds = pd.read_excel(
        DATA_DIR / "Rounds_Data.xlsx",
        parse_dates=["Date"],
    )

    courses = pd.read_excel(DATA_DIR / "Course_Data.xlsx")

    return summary, rounds, courses


def show():

    # Page Title & Sub Title
    st.markdown(
        """
        <div style='text-align: center; margin-top: 1rem;'>
            <h1 style='
                font-family: "Space Grotesk", sans-serif; 
                font-weight: 700; 
                font-size: 3rem;   /* much bigger title */
                margin: 0;
                color: #ffffff;
            '>
                📊 Round Summary
            </h1>
            <h2 style='
                font-family: "Martian Mono", monospace; 
                font-weight: 400; 
                font-size: 1.2rem; 
                margin: 0;
                color: #cccccc;
            '>
                Dive deep into your golf rounds and performance trends!
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Visual divider
    st.divider()

    # Load Data
    summary_df, rounds_df, course_df = load_data()

    # Create Synthetic Unique ID for Each Round
    summary_df["RoundID"] = (
        summary_df["Date"].astype(str)
        + "_"
        + summary_df["Player"].astype(str)
        + "_"
        + summary_df["Course"].astype(str)
    )
    rounds_df["RoundID"] = (
        rounds_df["Date"].astype(str)
        + "_"
        + rounds_df["Player"].astype(str)
        + "_"
        + rounds_df["Course"].astype(str)
    )

    # Filters
    col_round, col_course, col_player, col_type, col_roundid = st.columns(5)

    round_options = sorted(summary_df["Round"].dropna().unique().tolist())
    with col_round:
        selected_rounds = st.multiselect(
            "Round type",
            options=round_options,
            default=["Full-18"] if "Full-18" in round_options else [],
        )

    # Course Filter
    course_options = sorted(summary_df["Course"].dropna().unique().tolist())
    with col_course:
        selected_courses = st.multiselect("Course", options=course_options, default=[])

    # Player Filter
    player_options = sorted(summary_df["Player"].dropna().unique().tolist())
    default_players = ["Russell"] if "Russell" in player_options else []
    with col_player:
        selected_players = st.multiselect(
            "Player", options=player_options, default=default_players
        )

    # Round Type Filter
    with col_type:
        selected_types = st.multiselect(
            "Type",
            options=summary_df["Type"].dropna().unique().tolist(),
            default=["Solo"],
        )

    # RoundID Filter
    with col_roundid:
        roundid_options = sorted(summary_df["RoundID"].dropna().unique().tolist())
        selected_roundids = st.multiselect(
            "Round ID", options=roundid_options, default=[]
        )

    # Allow users to Apply Filters
    filtered_summary = summary_df.copy()
    if selected_rounds:
        filtered_summary = filtered_summary[
            filtered_summary["Round"].isin(selected_rounds)
        ]
    if selected_courses:
        filtered_summary = filtered_summary[
            filtered_summary["Course"].isin(selected_courses)
        ]
    if selected_players:
        filtered_summary = filtered_summary[
            filtered_summary["Player"].isin(selected_players)
        ]
    if selected_types:
        filtered_summary = filtered_summary[
            filtered_summary["Type"].isin(selected_types)
        ]
    if selected_roundids:
        filtered_summary = filtered_summary[
            filtered_summary["RoundID"].isin(selected_roundids)
        ]

    # Small Caption to show number of rounds selected
    st.caption(f"📊 {len(filtered_summary)} rounds selected")
    if filtered_summary.empty:
        st.info("No rounds match the selected filters.")
        st.stop()

    # Display Summary Table
    display_df = filtered_summary.copy()

    # Sort by raw Date first (newest at bottom)
    display_df = display_df.sort_values("Date", ascending=True)

    # Rename columns
    display_df = display_df.rename(
        columns={
            "Date": "📅 Date",
            "Course": "⛳ Course",
            "Player": "🏌️ Player",
            "Round": "🕳️ Round",
            "Type": "🎯 Type",
            "Score": "📊 Score",
            "Plus_/_Minus": "➕ / ➖ vs Par",
        }
    )

    # Format date for display only
    display_df["📅 Date"] = pd.to_datetime(display_df["📅 Date"]).dt.strftime(
        "%d %b %Y"
    )

    # Drop internal columns
    display_df = display_df.drop(
        columns=["ScoreDiff", "Par_for_Course", "RoundID", "Comment"], errors="ignore"
    )

    # Rounds DataFrame
    st.dataframe(display_df, width="stretch", hide_index=True)

    # Filter hole data based on RoundID filter (or all filtered rounds if none selected)
    if selected_roundids:
        round_holes = rounds_df[rounds_df["RoundID"].isin(selected_roundids)]
    else:
        round_holes = rounds_df[rounds_df["RoundID"].isin(filtered_summary["RoundID"])]

    merged = round_holes.merge(course_df, on=["Course", "Hole"], how="left")
    merged["Diff"] = merged["Score"] - merged["Par"]

    # Function to categorize shots
    def categorize_shot(diff):
        if diff <= -1:
            return "Birdie"
        elif diff == 0:
            return "Par"
        elif diff == 1:
            return "Bogey"
        elif diff == 2:
            return "Double"
        elif diff == 3:
            return "Triple"
        else:
            return "Blow-up (4+)"

    merged["Shot"] = merged["Diff"].apply(categorize_shot)

    # Layout: Two Columns
    col_scoretrend, col_donut = st.columns(2)

    # Shot Distribution Donut Chart
    with col_donut:
        shot_counts = merged["Shot"].value_counts().reset_index()
        shot_counts.columns = ["Shot", "Count"]

        fig = px.pie(
            shot_counts,
            names="Shot",
            values="Count",
            color="Shot",
            color_discrete_map={
                "Birdie": "#a8e6a2",
                "Par": "#d0f2b2",
                "Bogey": "#ffe29a",
                "Double": "#ffb285",
                "Triple": "#ff7f7f",
                "Blow-up (4+)": "#d8a8ff",
            },
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker_line_color="#ffffff",
            marker_line_width=2,
        )

        st.plotly_chart(fig, width="stretch")

    # Score Trend Over Time 18 vs 9 Holes
    with col_scoretrend:
        plot_df = filtered_summary.copy()

        plot_df["Date"] = pd.to_datetime(plot_df["Date"])

        def group_type(row):
            t = str(row["Round"]).strip()
            if t == "Full-18":
                return "Full 18"
            elif t in ["Front-9", "Back-9"]:
                return "Front/Back 9"
            else:
                return None

        plot_df["TypeGroup"] = plot_df.apply(group_type, axis=1)
        plot_df = plot_df[plot_df["TypeGroup"].notna()]
        plot_df = plot_df.sort_values("Date")

        # Pastel palette (repurposed for players)
        player_palette = [
            "#a8e6a2",
            "#94b7df",
            "#ffe29a",
            "#ffb285",
            "#ff7f7f",
            "#d8a8ff",
        ]

        players = plot_df["Player"].unique()
        color_map = {
            player: player_palette[i % len(player_palette)]
            for i, player in enumerate(players)
        }

        fig = px.line(
            plot_df,
            x="Date",
            y="Score",
            color="Player",
            line_dash="TypeGroup",
            markers=True,
            color_discrete_map=color_map,
        )

        # Fill the area under each line
        fig.update_traces(fill="tozeroy", opacity=0.6)

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Score",
            legend_title="Player / Round Type",
            template="plotly_dark",
            hovermode="x unified",
        )

        st.plotly_chart(fig, width="stretch")
