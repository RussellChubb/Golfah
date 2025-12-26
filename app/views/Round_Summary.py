# Golfah: Interactive Round Summary + Hole Analysis with RoundID
import streamlit as st
import pandas as pd
import matplotlib.colors as mcolors
import plotly.express as px
from utils.Data_Loader import load_data

def show():

    # Title
    st.title("📊 Golf Rounds Overview")

    # Load Data
    summary_df, rounds_df, course_df = load_data()

    # Create Synthetic Unique ID for Each Round
    summary_df["RoundID"] = (
        summary_df["Date"].astype(str) + "_" +
        summary_df["Player"].astype(str) + "_" +
        summary_df["Course"].astype(str)
    )
    rounds_df["RoundID"] = (
        rounds_df["Date"].astype(str) + "_" +
        rounds_df["Player"].astype(str) + "_" +
        rounds_df["Course"].astype(str)
    )

    # Header
    st.header("🏌️ Round Summary + Filters")
    
    # Filters
    col_round, col_course, col_player, col_type = st.columns(4)

    round_options = sorted(summary_df["Round"].dropna().unique().tolist())
    with col_round:
        selected_rounds = st.multiselect(
            "Round type",
            options=round_options,
            default=["Full-18"] if "Full-18" in round_options else [],
        )

    course_options = sorted(summary_df["Course"].dropna().unique().tolist())
    with col_course:
        selected_courses = st.multiselect("Course", options=course_options, default=[])

    player_options = sorted(summary_df["Player"].dropna().unique().tolist())
    default_players = ["Russell"] if "Russell" in player_options else []
    with col_player:
        selected_players = st.multiselect("Player", options=player_options, default=default_players)

    with col_type:
        selected_types = st.multiselect("Type", options=summary_df["Type"].dropna().unique().tolist(), default=["Solo"])

    # Apply Filters
    filtered_summary = summary_df.copy()
    if selected_rounds:
        filtered_summary = filtered_summary[filtered_summary["Round"].isin(selected_rounds)]
    if selected_courses:
        filtered_summary = filtered_summary[filtered_summary["Course"].isin(selected_courses)]
    if selected_players:
        filtered_summary = filtered_summary[filtered_summary["Player"].isin(selected_players)]
    if selected_types:
        filtered_summary = filtered_summary[filtered_summary["Type"].isin(selected_types)]

    st.caption(f"📊 {len(filtered_summary)} rounds selected")
    if filtered_summary.empty:
        st.info("No rounds match the selected filters.")
        st.stop()

    # Style function for gradient
    def rgba_gradient(series, cmap="RdYlGn_r", alpha=0.35):
        import matplotlib.pyplot as plt
        norm = mcolors.Normalize(vmin=series.min(), vmax=series.max())
        cmap = plt.get_cmap(cmap)
        def color(val):
            r, g, b, _ = cmap(norm(val))
            return f"background-color: rgba({int(r*255)}, {int(g*255)}, {int(b*255)}, {alpha})"
        return [color(v) for v in series]

    # Display Summary Table
    display_df = filtered_summary.copy()
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
    display_df["📅 Date"] = pd.to_datetime(display_df["📅 Date"]).dt.strftime("%d %b %Y")
    display_df = display_df.drop(columns=["ScoreDiff"], errors="ignore")

    # Apply color gradient
    styled_df = display_df.style.apply(rgba_gradient, subset=["➕ / ➖ vs Par"], alpha=0.45)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    # Select Round for Hole Analysis
    # Header
    st.header("🕳️ Hole Analysis") 

    filtered_summary["Label"] = (
        pd.to_datetime(filtered_summary["Date"]).dt.strftime("%d %b %Y") +
        " — " + filtered_summary["Player"] + " @ " + filtered_summary["Course"]
    )

    round_options = filtered_summary[["RoundID", "Label"]].to_dict(orient="records")
    selected_label = st.selectbox(
        "Select a round to view hole analysis",
        options=[r["Label"] for r in round_options]
    )

    selected_round_id = next(r["RoundID"] for r in round_options if r["Label"] == selected_label)

    # Filter hole data
    round_holes = rounds_df[rounds_df["RoundID"] == selected_round_id]
    merged = round_holes.merge(course_df, on=["Course", "Hole"], how="left")
    merged["Diff"] = merged["Score"] - merged["Par"]

    st.subheader(f"Round: {selected_label}")

    dataframe_col, chart_col = st.columns(2)
    with dataframe_col:
        st.dataframe(
            merged[["Hole", "Par", "Score", "Diff"]],
            use_container_width=True, hide_index=True
        )
    # Categorize Shots for Donut
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
            return "Blow-up"

    merged["Shot"] = merged["Diff"].apply(categorize_shot)

    # Shot Distribution Donut Chart
    with chart_col:
        shot_counts = merged["Shot"].value_counts().reset_index()
        shot_counts.columns = ["Shot", "Count"]

        fig = px.pie(
            shot_counts,
            names="Shot",
            values="Count",
            color="Shot",
            hole=0.5,
            color_discrete_map={
                "Birdie": "#a8e6a2",   # soft green
                "Par": "#d0f2b2",      # very light green
                "Bogey": "#ffe29a",    # pastel yellow
                "Double": "#ffb285",   # soft orange
                "Triple": "#ff7f7f",   # pastel red
                "Blow-up": "#d8a8ff"   # soft purple for dramatic effect
            },
        )

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
