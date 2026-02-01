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

    # Visual divider
    st.divider()

    # About Section
    st.markdown(
        """
        <div style='padding: 2em 0;'>
            <div style='
                background-color: rgba(38,39,48,0.5); 
                border-left: 4px solid rgba(46,204,113,0.7); 
                border-radius: 8px; 
                padding: 2em;
            '>
                <h3 style='
                    font-family: "Space Grotesk", sans-serif; 
                    color: rgba(46,204,113,1); 
                    margin-top: 0;
                '>
                    About Golfah ⛳
                </h3>
                <p style='
                    font-family: "Martian Mono", monospace; 
                    font-size: 1rem; 
                    line-height: 1.6; 
                    color: #cccccc;
                    margin-bottom: 1em;
                '>
                    Golfah is your personal golf analytics platform designed to help you track, analyze, and improve your game. 
                    By logging every round you play, you can identify patterns in your performance, understand your strengths and 
                    weaknesses, and make data-driven decisions to lower your scores.
                </p>
                <p style='
                    font-family: "Martian Mono", monospace; 
                    font-size: 1rem; 
                    line-height: 1.6; 
                    color: #cccccc;
                    margin-bottom: 1em;
                '>
                    Whether you're tracking solo rounds or playing with friends, Golfah provides detailed insights into your 
                    shot distribution, course performance, and scoring trends over time. Use the navigation menu to explore 
                    your round summaries, add new rounds, or dive deep into your statistics.
                </p>
                <p style='
                    font-family: "Martian Mono", monospace; 
                    font-size: 1rem; 
                    line-height: 1.6; 
                    color: #cccccc;
                    margin-bottom: 0;
                '>
                    <strong>Remember:</strong> The key to improvement is consistent tracking and honest analysis. Every round is 
                    a learning opportunity! 🏌️
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Load Data
    summary_df, rounds_df, course_df = load_data()

    # Helper function to format values safely
    def safe_format(value, default="N/A"):
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return default
        return value

    # Filter for Russell's solo rounds
    russell_solo = summary_df[(summary_df["Player"] == "Russell") & (summary_df["Type"] == "Solo")]

    # Get best scores
    russell_18 = russell_solo[russell_solo["Round"] == "Full-18"]
    russell_9 = russell_solo[russell_solo["Round"].isin(["Front-9", "Back-9"])]

    # Calculate stats
    best_score_18 = russell_18["Score"].min() if not russell_18.empty else None
    best_course_18 = russell_18.loc[russell_18["Score"].idxmin(), "Course"] if not russell_18.empty else None
    
    best_score_9 = russell_9["Score"].min() if not russell_9.empty else None
    best_course_9 = russell_9.loc[russell_9["Score"].idxmin(), "Course"] if not russell_9.empty else None
    
    # Total rounds for Russell
    total_rounds = len(summary_df[summary_df["Player"] == "Russell"])

    # Summary cards with custom styling
    col1, col2, col3 = st.columns(3)

    col1.markdown(
        f"<div style='{metric_style}'>"
        f"<div style='font-size:0.9rem; color:#cccccc; margin-bottom:0.5em'><b>Best Score (18 Holes) 🏆</b></div>"
        f"<div style='font-size:1.8rem; color:rgba(46,204,113,1); font-weight:700'>{safe_format(int(best_score_18) if best_score_18 else None)}</div>"
        f"<div style='font-size:0.75rem; color:#aaaaaa; margin-top:0.3em'>{safe_format(best_course_18)}</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    col2.markdown(
        f"<div style='{metric_style}'>"
        f"<div style='font-size:0.9rem; color:#cccccc; margin-bottom:0.5em'><b>Best Score (9 Holes) 🏆</b></div>"
        f"<div style='font-size:1.8rem; color:rgba(46,204,113,1); font-weight:700'>{safe_format(int(best_score_9) if best_score_9 else None)}</div>"
        f"<div style='font-size:0.75rem; color:#aaaaaa; margin-top:0.3em'>{safe_format(best_course_9)}</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    col3.markdown(
        f"<div style='{metric_style}'>"
        f"<div style='font-size:0.9rem; color:#cccccc; margin-bottom:0.5em'><b>Total Rounds Played 📊</b></div>"
        f"<div style='font-size:1.8rem; color:rgba(46,204,113,1); font-weight:700'>{total_rounds}</div>"
        "</div>",
        unsafe_allow_html=True,
    )
