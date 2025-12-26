# Golfah Utils: Navbar

# Imports
import streamlit as st
from streamlit_option_menu import option_menu

# Navbar
def navbar():
    page = option_menu(
        menu_title=None,  # Hide the title
        options=[
            "Home",
            "Hole Analysis",
            "Play",
            "Round Summary",
        ],
        icons=[
            "house-fill",
            "flag-fill",
            "plus-circle-fill",
            "bar-chart-fill"
        ],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "transparent",
                "max-width": "100%",  # Make it full width
            },
            "icon": {"color": "rgba(46,204,113,0.9)", "font-size": "18px"},
            "nav-link": {
                "font-family": "'Space Grotesk', sans-serif",
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "padding": "12px 30px",  # Increased padding for wider buttons
                "background-color": "transparent",
                "border-bottom": "2px solid transparent",
                "color": "#ffffff",
                "flex": "1",  # Makes each button take equal width
            },
            "nav-link-selected": {
                "background-color": "rgba(46,204,113,0.2)",
                "border-bottom": "2px solid rgba(46,204,113,0.9)",
                "color": "#ffffff",
                "font-weight": "600",
            },
            "nav-link:hover": {
                "background-color": "rgba(46,204,113,0.1)",
                "border-bottom": "2px solid rgba(46,204,113,0.5)",
            },
        },
    )
    return page