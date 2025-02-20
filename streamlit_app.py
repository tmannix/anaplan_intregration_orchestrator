import streamlit as st
from auth_page import main as auth_page_main
from call_api import main as call_api_main

# Set up page configuration
st.set_page_config(
    page_title="Main App",
    page_icon=":guardsman:",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Sidebar for navigation
st.sidebar.title("Main Menu")
selected = st.sidebar.radio(
    "Go to",
    ["Home", "Authentication", "API Call"],
    index=0
)

# Main app logic
if selected == "Home":
    st.title("Home Page")
    st.write("Welcome to the main app!")
elif selected == "Authentication":
    auth_page_main()
elif selected == "API Call":
    call_api_main()