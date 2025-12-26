# Golfah: Home Page

# Imports
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import os
from utils.Navbar import navbar
from utils.Data_Loader import load_data

# Page Configuration
st.set_page_config(page_title="Golfah", page_icon="⛳", layout="wide")

# Show function (paradigm used for page-switching)
def show():

    # Metric Style
    metric_style = (
        "background-color: rgba(38,39,48,0.7); "
        "border: 2px solid rgba(46,204,113,0.7); "
        "border-radius: 10px; "
        "padding: 1.5em 1em; "
        "text-align: center; "
        "margin-bottom: 0.5em; "
        "color: #ffffff;"
    )

    # Load fonts
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Martian+Mono:wght@400;700&family=Space+Grotesk:wght@400;700&display=swap" rel="stylesheet">
        """,
        unsafe_allow_html=True,
    )

    # Page Title & Sub Title
    st.markdown(
        """
        <div style='text-align: center; margin-top: 1rem;'>
            <h1 style='
                font-family: "Space Grotesk", sans-serif; 
                font-weight: 700; 
                font-size: 5rem;   /* much bigger title */
                margin: 0;
                color: #ffffff;
            '>
                Golfah ⛳
            </h1>
            <h2 style='
                font-family: "Martian Mono", monospace; 
                font-weight: 400; 
                font-size: 1.2rem; 
                margin: 0;
                color: #cccccc;
            '>
                Using Data to Improve your golf game!
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Data Loading
    summary_df, rounds_df, course_df = load_data()

    # Visual divider
    st.divider()

    # # Summary cards with custom styling
    # col1, col2, col3 = st.columns(3)


    # # Helper function to format values safely
    # def safe_format(value, default="N/A"):
    #     """Format value, returning default if None or NaN."""
    #     if value is None or (isinstance(value, float) and pd.isna(value)):
    #         return default
    #     return value

    # # Pulling Summary Stats
    # def get_summary_stats(summary_df: pd.DataFrame):
    #     """Compute high-level summary metrics."""
    #     best_row = summary_df.loc[summary_df["Score"].idxmin()]
    #     avg_score = summary_df["Score"].mean()
    #     avg_diff = summary_df["ScoreDiff"].mean()

    #     return {
    #         "best_score": int(best_row["Score"]),
    #         "best_course": best_row["Course"],
    #         "avg_score": round(avg_score, 1),
    #         "avg_diff": round(avg_diff, 1),
    #     }

    # col1.markdown(
    #     f"<div style='{metric_style}'>"
    #     f"<div style='font-size:0.9rem; color:#cccccc; margin-bottom:0.5em'><b>Best Score 🏆</b></div>"
    #     f"<div style='font-size:1.8rem; color:rgba(46,204,113,1); font-weight:700'>{safe_format(stats['best_score'])}</div>"
    #     f"<div style='font-size:0.75rem; color:#aaaaaa; margin-top:0.3em'>{safe_format(stats['best_course'])}</div>"
    #     f"<hr style='margin:0.8em 0; border:0; border-top:1px solid rgba(46,204,113,0.3)'>"
    #     f"<div style='font-size:0.9rem; color:#cccccc; margin-bottom:0.5em'><b>Best Score 18 🏆</b></div>"
    #     f"<div style='font-size:1.8rem; color:rgba(46,204,113,1); font-weight:700'>{safe_format(stats['best_score'])}</div>"
    #     f"<div style='font-size:0.75rem; color:#aaaaaa; margin-top:0.3em'>{safe_format(stats['best_course'])}</div>"
    #     "</div>",
    #     unsafe_allow_html=True,
    # )

    # col2.markdown(
    #     f"<div style='{metric_style}'>"
    #     f"<div style='font-size:0.9rem; color:#cccccc; margin-bottom:0.5em'><b>Average Score (9 Holes) 📊</b></div>"
    #     f"<div style='font-size:1.8rem; color:rgba(46,204,113,1); font-weight:700'>{safe_format(stats['avg_score'])}</div>"
    #     f"<hr style='margin:0.8em 0; border:0; border-top:1px solid rgba(46,204,113,0.3)'>"
    #     f"<div style='font-size:0.9rem; color:#cccccc; margin-bottom:0.5em'><b>Average Score (18 Holes) 📊</b></div>"
    #     f"<div style='font-size:1.8rem; color:rgba(46,204,113,1); font-weight:700'>{safe_format(stats['avg_score'])}</div>"
    #     "</div>",
    #     unsafe_allow_html=True,
    # )

    # avg_diff_9 = (
    #     f"{stats['avg_diff']:+}"
    #     if stats["avg_diff"] is not None and not pd.isna(stats["avg_diff"])
    #     else "N/A"
    # )
    # avg_diff_18 = (
    #     f"{stats['avg_diff']:+}"
    #     if stats["avg_diff"] is not None and not pd.isna(stats["avg_diff"])
    #     else "N/A"
    # )

    # col3.markdown(
    #     f"<div style='{metric_style}'>"
    #     f"<div style='font-size:0.9rem; color:#cccccc; margin-bottom:0.5em'><b>Avg vs Par (9 Holes) ⛳</b></div>"
    #     f"<div style='font-size:1.8rem; color:rgba(46,204,113,1); font-weight:700'>{avg_diff_9}</div>"
    #     f"<hr style='margin:0.8em 0; border:0; border-top:1px solid rgba(46,204,113,0.3)'>"
    #     f"<div style='font-size:0.9rem; color:#cccccc; margin-bottom:0.5em'><b>Avg vs Par (18 Holes) ⛳</b></div>"
    #     f"<div style='font-size:1.8rem; color:rgba(46,204,113,1); font-weight:700'>{avg_diff_18}</div>"
    #     "</div>",
    #     unsafe_allow_html=True,
    # )

    # # Visual Divider
    # st.divider()

    # st.subheader("📈 Score Trend Over Time")
    # round_types = ["All"] + list(summary_df["Type"].unique())
    # selected_type = st.selectbox("Select Round Type:", round_types)

    # # Filter data based on selection
    # if selected_type != "All":
    #     fig = plot_score_trend(summary_df, selected_type)
    # else:
    #     fig = plot_score_trend(summary_df)

    # st.plotly_chart(fig, use_container_width=True)

    # st.subheader("🏌️ Recent Rounds")
    # st.dataframe(summary_df.sort_values("Date", ascending=False).head(5))
