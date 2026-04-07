# Golfah: Entry Point
# This is the main entry point for the Golfah Streamlit application.

# Imports
import streamlit as st
from utils.Navbar import navbar
import sys  # Needed for deployment
from pathlib import Path  # Needed for deployment

# Needed for deployment to ensure the app can find the views and utils modules
sys.path.insert(0, str(Path(__file__).parent))

# Page Setup
st.set_page_config(page_title="Golfah", page_icon="⛳", layout="wide")

# Render Navbar + Get to Selected Page
page = navbar()

# Page Routing (match the option_menu labels)
if page == "Home":
    from views import Home

    Home.show()

elif page == "Play":
    from views import Play

    Play.show()

elif page == "Round Summary":
    from views import Round_Summary

    Round_Summary.show()
