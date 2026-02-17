# Golfah: Play Page

# Imports
import os
import streamlit as st
import pandas as pd
from datetime import date
from utils.Data_Loader import load_data
from pathlib import Path

# TODO
# Actually get this page working

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

    # Load in Data
    summary_df, rounds_df, course_df = load_data()

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
                ⛳ Add New Round
            </h1>
            <h2 style='
                font-family: "Martian Mono", monospace; 
                font-weight: 400; 
                font-size: 1.2rem; 
                margin: 0;
                color: #cccccc;
            '>
                Log your latest golf round and track your progress!
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Visual divider
    st.divider()

    # New Round Form
    with st.form("new_round_form"):
        st.subheader("Round Summary Info")
        col1, col2, col3 = st.columns(3)
        course = col1.selectbox("Course", course_df["Course"].unique())
        player = col2.text_input("Player Name", "Russell")
        round_date = col3.date_input("Date", date.today())
        round_type = col1.selectbox(
            "Round Type", ["Front-9", "Back-9", "Full", "Practice"]
        )
        comment = st.text_input("Comment", "")

        st.subheader("Enter Scores")
        holes = course_df[course_df["Course"] == course][
            ["Hole", "Par", "Distance"]
        ].copy()
        holes["Score"] = holes["Hole"].apply(
            lambda h: st.number_input(
                f"Hole {h} Score", min_value=1, max_value=15, value=4, step=1
            )
        )

        submitted = st.form_submit_button("Add Round")

    if submitted:
        total_score = holes["Score"].sum()
        total_par = holes["Par"].sum()
        diff = total_score - total_par

        # Append to summary table
        new_summary = pd.DataFrame(
            [
                {
                    "Date": round_date,
                    "Course": course,
                    "Player": player,
                    "RoundType": round_type,
                    "Score": total_score,
                    "ParTotal": total_par,
                    "ScoreDiff": diff,
                    "Comment": comment,
                }
            ]
        )
        summary_df = pd.concat([summary_df, new_summary], ignore_index=True)

        # TODO: Need to redo this func, doesn't work rn
        # # Append to rounds data
        # new_rounds = holes.assign(
        #     Course=course,
        #     Player=player,
        #     Date=round_date,
        # )[["Course", "Hole", "Player", "Score", "Date"]]
        # rounds_df = pd.concat([rounds_df, new_rounds], ignore_index=True)

        # save_data(summary_df, rounds_df, course_df)

        # st.success(f"New round added for {player} at {course} ({round_type})!")
