import streamlit as st
import requests

# Function to call an example API
def call_example_api():
    url = "https://api.example.com/data"
    headers = {
        "Authorization": f"Bearer {st.secrets['auth_token']}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from API")
        return None

# Streamlit app
def main():
    st.title("API Call Page")

    if "auth_token" in st.secrets:
        data = call_example_api()
        if data:
            st.write("API Data:", data)
    else:
        st.warning("Please authenticate first")

if __name__ == "__main__":
    main()