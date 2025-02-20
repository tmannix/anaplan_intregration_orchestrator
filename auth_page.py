import streamlit as st
import requests
import json

# Function to generate authentication token
def generate_auth_token(username, password):
    url = "https://auth.anaplan.com/token/authenticate"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json().get("tokenInfo", {}).get("tokenValue")
    else:
        st.error("Failed to authenticate")
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
            # Store the token in Streamlit secrets
            st.secrets["auth_token"] = token

if __name__ == "__main__":
    main()