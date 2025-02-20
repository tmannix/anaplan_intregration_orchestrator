import streamlit as st
import requests
import base64
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# Function to generate authentication token
def generate_auth_token(username, password):
    # Encode the username and password
    user_pw = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')

    # Set up the headers for the request
    auth_headers = {
        'Authorization': f'Basic {user_pw}',
        'Content-Type': 'application/json'
    }

    # URL for authentication
    auth_url = 'https://us1a.app.anaplan.com/token/authenticate'

    # Make the POST request
    response = requests.post(auth_url, headers=auth_headers, verify=False)

    # Check the response
    if str(response.status_code).startswith('2'):
        auth_json = response.json()
        return auth_json['tokenInfo']['tokenValue']
    else:
        st.error(f"Failed to authenticate: {response.status_code}")
        st.error(response.text)
        return None

# Streamlit app
def main():
    st.title("Authentication Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        token = generate_auth_token(username, password)
        if token:
            st.success("Authentication successful!")
            st.write(f"Your token: {token}")
            # Store the token and other details in Streamlit session state
            st.session_state.auth_token = token
            st.session_state.username = username
            st.session_state.password = password
            st.session_state.last_refreshed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Auto-refresh every 15 minutes (900 seconds)
    if "auth_token" in st.session_state:
        st_autorefresh(interval=900 * 1000, key="auth_refresh")
        token = generate_auth_token(st.session_state.username, st.session_state.password)
        if token:
            st.session_state.auth_token = token
            st.session_state.last_refreshed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        st.write(f"Logged in as: {st.session_state.username}")
        st.write(f"Password: {st.session_state.password}")
        st.write(f"Auth token last refreshed: {st.session_state.last_refreshed}")

if __name__ == "__main__":
    main()