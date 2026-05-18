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

# Page Routing
# If it's the home-page, render the home-page.
if page == "Home":
    from views import home

    # Render the home page.
    home.show()

# If it's the play-page, render the play-page.
elif page == "Play":
    from views import play

    # Render the play page.
    play.show()

# If it's the analysis-page, render the analysis-page.
elif page == "Analysis":
    from views import analysis

    # Render the analysis page.
    analysis.show()

# If it's the achievements-page, render the achievements-page.
elif page == "Achievements":
    from views import achievements

    # Render the achievements page.
    achievements.show()