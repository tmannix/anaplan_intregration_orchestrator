import streamlit as st

def save_credentials(username, password):
    st.secrets["username"] = username
    st.secrets["password"] = password

def get_auth_token():
    import requests
    auth = (st.secrets["username"], st.secrets["password"])
    response = requests.get("https://api.anaplan.com/token", auth=auth)
    return response.json().get("token")

st.title("Authentication Page")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Save Credentials"):
    save_credentials(username, password)
    st.success("Credentials saved!")

if st.button("Get Auth Token"):
    token = get_auth_token()
    st.text_input("Auth Token", value=token, type="password")