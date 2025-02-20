import streamlit as st
import requests
import base64
from datetime import datetime, timedelta
import threading
import time

# Function to generate authentication token
def generate_auth_token(username, password):
    user_pw = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8')
    auth_headers = {
        'Authorization': f'Basic {user_pw}',
        'Content-Type': 'application/json'
    }
    auth_url = 'https://us1a.app.anaplan.com/token/authenticate'
    response = requests.post(auth_url, headers=auth_headers, verify=False)
    if str(response.status_code).startswith('2'):
        auth_json = response.json()
        return auth_json['tokenInfo']['tokenValue']
    else:
        st.error(f"Failed to authenticate: {response.status_code}")
        st.error(response.text)
        return None

# Function to refresh the authentication token in the background
def refresh_token():
    while True:
        if "auth_token" in st.session_state:
            token = generate_auth_token(st.session_state.username, st.session_state.password)
            if token:
                st.session_state.auth_token = token
                st.session_state.last_refreshed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(900)  # Refresh every 15 minutes

# Streamlit app
def main():
    st.title("Authentication Page")

    username = st.text_input("Username")
    
    # Password input with show/hide functionality
    show_password = st.checkbox("Show Password")
    password = st.text_input("Password", type="default" if show_password else "password")

    if st.button("Login"):
        token = generate_auth_token(username, password)
        if token:
            st.success("Authentication successful!")
            st.write(f"Your token: {token}")
            st.session_state.auth_token = token
            st.session_state.username = username
            st.session_state.password = password
            st.session_state.last_refreshed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Start the token refresh thread if not already running
            if "refresh_thread" not in st.session_state:
                st.session_state.refresh_thread = threading.Thread(target=refresh_token, daemon=True)
                st.session_state.refresh_thread.start()

    if "auth_token" in st.session_state:
        st.write(f"Logged in as: {st.session_state.username}")
        
        # Password display with show/hide functionality
        show_password_bottom = st.checkbox("Show Password", key="show_password_bottom")
        st.write(f"Password: {'*' * len(st.session_state.password) if not show_password_bottom else st.session_state.password}")
        
        st.write(f"Auth token last refreshed: {st.session_state.last_refreshed}")

if __name__ == "__main__":
    main()