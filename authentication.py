import streamlit as st
import requests

def save_credentials(username, password):
    st.session_state["username"] = username
    st.session_state["password"] = password

def get_auth_token():
    auth = (st.session_state.get("username"), st.session_state.get("password"))
    response = requests.get("https://api.anaplan.com/token", auth=auth)
    return response.json().get("token")

st.title("Authentication Page")

username = st.text_input("Username", value=st.session_state.get("username", ""))
password = st.text_input("Password", type="password", value=st.session_state.get("password", ""))

if st.button("Save Credentials"):
    save_credentials(username, password)
    st.success("Credentials saved!")

if st.button("Get Auth Token"):
    if "username" in st.session_state and "password" in st.session_state:
        token = get_auth_token()
        st.text_input("Auth Token", value=token, type="password")
    else:
        st.error("Please save your credentials first.")