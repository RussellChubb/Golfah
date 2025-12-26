# Golfah: Hole Analysis Page
# The purpose of this page is to show hole-by-hole analysis of the user's golf rounds.

# TODO:
# Add in donut chart of shot distribution over round (i.e. % of boogeys, pars, birdies, eagles, etc.)

# Imports
import streamlit as st
import matplotlib.pyplot as plt
from utils.Data_Loader import load_data
import plotly.express as px

# Show function (paradigm used for page-switching)
def show():
    
    # Title
    st.title("🕳️ Hole Analysis")

    # Data Loading
    summary_df, rounds_df, course_df = load_data()

    course_list = rounds_df["Course"].unique()
    selected_course = st.selectbox("Select Course", course_list)

    merged = rounds_df.merge(course_df, on=["Course", "Hole"], how="left")
    merged["Diff"] = merged["Score"] - merged["Par"]

    course_summary = (
        merged[merged["Course"] == selected_course]
        .groupby("Hole")
        .agg(Avg_Score=("Score", "mean"), Par=("Par", "first"), Avg_Diff=("Diff", "mean"))
        .reset_index()
    )

    # This dataframe shows average score vs par for each hole
    fakecol1, dataframecol, fakecol2 = st.columns([1, 3, 1])
    with dataframecol:
        st.dataframe(course_summary, width=700)

    # Plot Average Score Difference per Hole
    fig = px.bar(
        course_summary,
        x="Hole",
        y="Avg_Diff",
        color="Avg_Diff",
        color_continuous_scale="RdYlGn_r",
        labels={
            "Avg_Diff": "Average vs Par",
            "Hole": "Hole"
        },
        title=f"Average Score Difference per Hole — {selected_course}",
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray",
        annotation_text="Par",
        annotation_position="top left",
    )

    fig.update_layout(
        height=450,
        xaxis=dict(tickmode="linear"),
        coloraxis_showscale=False,
        margin=dict(l=40, r=40, t=60, b=40),
    )

    st.plotly_chart(fig, use_container_width=True)