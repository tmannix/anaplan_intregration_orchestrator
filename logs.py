import streamlit as st
import json
import os

# Function to load logs from a JSON file
def load_logs_from_file(filename="logs.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return []

def display_logs():
    st.title("Run Logs")

    logs = load_logs_from_file()

    if logs:
        for log in logs:
            st.write(log)
    else:
        st.write("No logs available.")

def main():
    display_logs()

if __name__ == "__main__":
    main()