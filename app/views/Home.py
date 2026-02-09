# Golfah: Home Page

# Imports
import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from pathlib import Path
import pydeck as pdk

# TODO
# Have some kind of check to see whether or not the data files exist, if they don't perhaps we can raise something for users to chuck their own .csvs in

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
        "min-height: 150px;"
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

    # Divider
    st.divider()

    # Page Title & Sub Title
    st.markdown(
        """
        <div style='text-align: center; margin-top: 1rem;'>
            <h1 style='
                font-family: "Space Grotesk", sans-serif; 
                font-weight: 700; 
                font-size: 3rem;
                margin: 0;
                color: #ffffff;
            '>
                High Level Metrics 📊  
            </h1>
            <h2 style='
                font-family: "Martian Mono", monospace; 
                font-weight: 400; 
                font-size: 1.2rem; 
                margin: 0;
                color: #cccccc;
            '>
                My High Level Golf Stats at a Glance!
            </h2>
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
    russell_solo = summary_df[
        (summary_df["Player"] == "Russell") & (summary_df["Type"] == "Solo")
    ]

    # Get best scores
    russell_18 = russell_solo[russell_solo["Round"] == "Full-18"]
    russell_9 = russell_solo[russell_solo["Round"].isin(["Front-9", "Back-9"])]

    # Calculate stats
    best_score_18 = russell_18["Score"].min() if not russell_18.empty else None
    best_course_18 = (
        russell_18.loc[russell_18["Score"].idxmin(), "Course"]
        if not russell_18.empty
        else None
    )

    best_score_9 = russell_9["Score"].min() if not russell_9.empty else None
    best_course_9 = (
        russell_9.loc[russell_9["Score"].idxmin(), "Course"]
        if not russell_9.empty
        else None
    )

    # Total rounds for Russell
    total_rounds = len(summary_df[summary_df["Player"] == "Russell"])

    # # Estiated Handicap (simple formula)
    # estimated_handicap = (russell_solo["Score"] - russell_solo["Par"]).mean() if not russell_solo.empty else None

    # Summary cards with custom styling
    col1, col2, col3, col4 = st.columns(4)

    # Best Score 18 Holes
    col1.markdown(
        f"<div style='{metric_style}'>"
        f"<div style='font-size:0.9rem; color:#cccccc; margin-bottom:0.5em'><b>Best Score (18 Holes) 🏆</b></div>"
        f"<div style='font-size:1.8rem; color:rgba(46,204,113,1); font-weight:700'>{safe_format(int(best_score_18) if best_score_18 else None)}</div>"
        f"<div style='font-size:0.75rem; color:#aaaaaa; margin-top:0.3em'>{safe_format(best_course_18)}</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Best Score 9 Holes
    col2.markdown(
        f"<div style='{metric_style}'>"
        f"<div style='font-size:0.9rem; color:#cccccc; margin-bottom:0.5em'><b>Best Score (9 Holes) 🏆</b></div>"
        f"<div style='font-size:1.8rem; color:rgba(46,204,113,1); font-weight:700'>{safe_format(int(best_score_9) if best_score_9 else None)}</div>"
        f"<div style='font-size:0.75rem; color:#aaaaaa; margin-top:0.3em'>{safe_format(best_course_9)}</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Total Rounds Played
    col3.markdown(
        f"<div style='{metric_style}'>"
        f"<div style='font-size:0.9rem; color:#cccccc; margin-bottom:0.5em'><b>Total Rounds Played 📊</b></div>"
        f"<div style='font-size:1.8rem; color:rgba(46,204,113,1); font-weight:700'>{total_rounds}</div>"
        f"<div style='font-size:0.75rem; color:#aaaaaa; margin-top:0.3em'>Placeholder to say how many in the last 30 days</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # # TODO: Estimated Handicap (simple formula)
    # col4.markdown(
    #     f"<div style='{metric_style}'>"
    #     f"<div style='font-size:0.9rem; color:#cccccc; margin-bottom:0.5em'><b>Estimated Handicap</b></div>"
    #     f"<div style='font-size:1.8rem; color:rgba(46,204,113,1); font-weight:700'>{estimated_handicap}</div>"
    #     "</div>",
    #     unsafe_allow_html=True,
    # )

    # Divider
    st.divider()

    # Heading for Course Map
    # Page Title & Sub Title
    st.markdown(
        """
        <div style='text-align: center; margin-top: 1rem;'>
            <h1 style='
                font-family: "Space Grotesk", sans-serif; 
                font-weight: 700; 
                font-size: 3rem;
                margin: 0;
                color: #ffffff;
            '>
                Course Map 🗺️  
            </h1>
            <h2 style='
                font-family: "Martian Mono", monospace; 
                font-weight: 400; 
                font-size: 1.2rem; 
                margin: 0;
                color: #cccccc;
            '>
                Visualing all the golf courses I've played!
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Divider
    st.divider()

    # Layout for Map and Table
    colmap, coltable = st.columns([2, 1])

    with colmap:
        # Filter courses with coords
        map_df = course_df[["Course", "LAT", "LON"]].dropna()

        # View state (centered roughly on NZ)
        view_state = pdk.ViewState(
            latitude=map_df["LAT"].mean(),
            longitude=map_df["LON"].mean(),
            zoom=4,
            pitch=0,
        )

        # Layer
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position="[LON, LAT]",
            radius_units="pixels",
            get_radius=6,
            radius_min_pixels=4,
            radius_max_pixels=12,
            get_fill_color=[46, 204, 113, 50],
            pickable=True,
            auto_highlight=True,
            highlight_color=[255, 255, 255],
        )

        # Render
        st.pydeck_chart(
            pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip={"text": "{Course}"},
            )
        )

    # Table of Courses
    with coltable:
        course_df = course_df.rename(
            {"Slope_Rating": "Slope Rating", "Course_Rating": "Course Rating"},
        )

        st.dataframe(
            course_df[["Course", "Slope_Rating", "Course_Rating"]]
            .drop_duplicates()
            .reset_index(drop=True),
            hide_index=True,
        )
