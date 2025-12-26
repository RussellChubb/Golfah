# Golfah Utils: Data Loader

# Imports
import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_data():
    summary = pd.read_excel("data/Summary_Data.xlsx", sheet_name="Summary", parse_dates=["Date"])
    rounds = pd.read_excel("data/Rounds_Data.xlsx", sheet_name="Rounds", parse_dates=["Date"])
    course = pd.read_excel("data/Course_Data.xlsx", sheet_name="Course")

    for df in [summary, rounds, course]:
        df.columns = df.columns.str.strip().str.replace(" ", "_")

    if "Plus_/_Minus" in summary.columns:
        summary["ScoreDiff"] = summary["Plus_/_Minus"]
    elif "ScoreDiff" not in summary.columns:
        summary["ScoreDiff"] = summary["Score"] - summary["Par_for_Course"]

    return summary, rounds, course

def save_data(summary_df, rounds_df, course_df, path="data"):
    os.makedirs(path, exist_ok=True)
    summary_df.to_csv(f"{path}/course_summary.csv", index=False)
    rounds_df.to_csv(f"{path}/rounds_data.csv", index=False)
    course_df.to_csv(f"{path}/course_data.csv", index=False)