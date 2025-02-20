import streamlit as st
import requests
import base64

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
            # Store the token in Streamlit secrets
            st.secrets["auth_token"] = token

if __name__ == "__main__":
    main()