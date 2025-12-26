# Golfah: Manage Data Page

# Imports
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from utils.Navbar import navbar
from utils.Data_Loader import load_data, save_data
import os

# Show function (paradigm used for page-switching)
def show():

    # Data Loading
    summary_df, rounds_df, course_df = load_data()

    st.title("⚙️ Manage Data")

    tab1, tab2, tab3 = st.tabs(["Course Summary", "Rounds Data", "Course Data"])

    with tab1:
        edited_summary = st.data_editor(summary_df, num_rows="dynamic", key="summary_edit")

    with tab2:
        edited_rounds = st.data_editor(rounds_df, num_rows="dynamic", key="rounds_edit")

    with tab3:
        edited_course = st.data_editor(course_df, num_rows="dynamic", key="course_edit")

    if st.button("💾 Save Changes to CSV"):
        save_data(edited_summary, edited_rounds, edited_course)
        st.success("Data saved successfully!")
