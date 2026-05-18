# Golfah: Home Page

# Imports
import streamlit as st
from pathlib import Path

# TODO
# Create video to embed on this screen
# Add R Logo to top left hand corner
# Create a real about section, with a lot less lorem ipsum


# Show function (paradigm used for page-switching)
def show():

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
                Using Data to improve your golf game!
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
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                </p>
                <p style='
                    font-family: "Martian Mono", monospace; 
                    font-size: 1rem; 
                    line-height: 1.6; 
                    color: #cccccc;
                    margin-bottom: 1em;
                '>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </p>
                <p style='
                    font-family: "Martian Mono", monospace; 
                    font-size: 1rem; 
                    line-height: 1.6; 
                    color: #cccccc;
                    margin-bottom: 0;
                '>
                    <strong>Remember:</strong> Remove the AI slop....
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )