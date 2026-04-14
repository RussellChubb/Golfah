# Golfah: Entry Point

# Deployment
import sys
from pathlib import Path

# Needed for deployment to ensure the app can find the views and utils modules
sys.path.insert(0, str(Path(__file__).parent))

# Imports
import streamlit as st
from utils.Navbar import navbar

# Page Setup
st.set_page_config(page_title="Golfah", page_icon="⛳", layout="wide")

# Render Navbar + Get to Selected Page
page = navbar()

# Page Routingh
if page == "Home":
    from views import Home

    Home.show()

elif page == "Play":
    from views import Play

    Play.show()

elif page == "Round Summary":
    from views import Round_Summary

    Round_Summary.show()
