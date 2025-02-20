
import streamlit as st
from streamlit_option_menu import option_menu

st.title("Home Page")
st.write("Welcome to the Home Page!")

selected = option_menu(
    menu_title=None,
    options=["Home", "Call API", "Authentication"],
    icons=["house", "cloud-upload", "key"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected == "Home":
    st.write("Welcome to the Home Page!")
elif selected == "Call API":
    import call_api
elif selected == "Authentication":
    import authentication