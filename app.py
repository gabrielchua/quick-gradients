import os
import json
import streamlit as st
from groq import Groq
from st_keyup import st_keyup

API_KEY = os.environ.get("GROQ_API_KEY")
if API_KEY is None:
    try:
        API_KEY = st.secrets["GROQ_API_KEY"]
    except KeyError:
        # Handle the case where GROQ_API_KEY is neither in the environment variables nor in Streamlit secrets
        st.error("API key not found.")
        st.stop()

client = Groq(api_key=API_KEY)

SYSTEM_MESSAGE = """
Given a description of a theme, come up with two hex color codes that would be used for a gradient to represent the theme.
These colours must be aesthetically pleasing and complement each other.
Also provide ONLY ONE emoji that represents the theme.

Reply in JSON.

For example
{
    "color_1": "FF5733",
    "color_2": "FFC300",
    "emoji": "🔥"
}
"""
def generate_colors(theme):
    """
    Given a theme, generate two hex color codes that would represent the theme.
    """
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "system", "content": SYSTEM_MESSAGE},
                  {"role": "user", "content": theme}],
        stream=False,
        response_format={"type": "json_object"}
    )

    results = response.choices[0].message.content
    results = json.loads(results)

    return results["color_1"], results["color_2"], results["emoji"]

def is_dark_color(color):
    """
    Check if a color is dark.
    """
    # Implement the logic to determine if the color is dark
    # For example, you can check if the sum of the RGB values is below a certain threshold
    # Return True if the color is dark, False otherwise
    
    # Convert the color from hex to RGB
    r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
    
    # Calculate the luminance of the color
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    
    # Check if the luminance is below a certain threshold (e.g., 0.5)
    if luminance < 0.5:
        return True
    else:
        return False


def update_ui():
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden}
    #header {visibility: hidden}
    #footer {visibility: hidden}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        }
        
    .stApp a:first-child {
        display: none;
    }
    .css-15zrgzn {display: none}
    .css-eczf16 {display: none}
    .css-jn99sy {display: none}
    </style>
    """, unsafe_allow_html=True)

    if st.session_state["theme"] != "":
        color_1, color_2, emoji = generate_colors(st.session_state["theme"])
        is_dark_centre= is_dark_color(color_1)
        text_color = "#ffffff" if is_dark_centre else "#000000"
        st.markdown(f"""
        <div style="background: radial-gradient(circle, #{color_1}, #{color_2}); border-radius: 10px; padding: 20px; text-align: center;">
            <h2 style="text-align: center; color: {text_color};">{st.session_state["theme"]} {emoji}</h2>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden}
    #header {visibility: hidden}
    #footer {visibility: hidden}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        }
        
    .stApp a:first-child {
        display: none;
    }
    .css-15zrgzn {display: none}
    .css-eczf16 {display: none}
    .css-jn99sy {display: none}
    </style>
    """, unsafe_allow_html=True)
    
st_keyup('Enter your text, and an image is dynamically generated',
         max_chars=280,
         key="theme",
         on_change=update_ui)
