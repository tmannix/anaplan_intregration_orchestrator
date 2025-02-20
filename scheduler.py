import streamlit as st
import requests
import time
import json
import os
import threading
from datetime import datetime

# Function to call the Anaplan API
def call_anaplan_api(api_type, model_id=None, action_id=None):
    headers = {
        "Authorization": f"Bearer {st.session_state.auth_token}",
        "Content-Type": "application/json"
    }

    if api_type == "Import":
        api_url = f"https://api.anaplan.com/2/0/models/{model_id}/imports/{action_id}/tasks"
    elif api_type == "Export":
        api_url = f"https://api.anaplan.com/2/0/models/{model_id}/exports/{action_id}/tasks"
    elif api_type == "Process":
        api_url = f"https://api.anaplan.com/2/0/models/{model_id}/processes/{action_id}/tasks"
    elif api_type == "Delete":
        api_url = f"https://api.anaplan.com/2/0/models/{model_id}/deletes/{action_id}/tasks"
    else:
        st.error("Invalid API type selected")
        return None

    response = requests.post(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data from API: {response.status_code}")
        st.error(response.text)
        return None

# Function to save tasks to a JSON file
def save_tasks_to_file(tasks, filename="tasks.json"):
    with open(filename, "w") as file:
        json.dump(tasks, file)

# Function to load tasks from a JSON file
def load_tasks_from_file(filename="tasks.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return []

# Function to save logs to a JSON file
def save_logs_to_file(logs, filename="logs.json"):
    with open(filename, "w") as file:
        json.dump(logs, file)

# Function to load logs from a JSON file
def load_logs_from_file(filename="logs.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return []

# Function to run the scheduler in the background
def run_scheduler():
    while True:
        for task in st.session_state.tasks:
            if task["active"]:
                st.write(f"Running task: {task['task_name']}")
                call_anaplan_api(task["api_type"], task["model_id"], task["action_id"])
                task["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = {
                    "task_name": task["task_name"],
                    "api_type": task["api_type"],
                    "model_name": task["model_name"],
                    "model_id": task["model_id"],
                    "action_id": task["action_id"],
                    "run_time": task["last_run"]
                }
                st.session_state.logs.append(log_entry)
                save_tasks_to_file(st.session_state.tasks)
                save_logs_to_file(st.session_state.logs)
                time.sleep(task["frequency"])

# Function to schedule API calls
def schedule_api_calls():
    if "tasks" not in st.session_state:
        st.session_state.tasks = load_tasks_from_file()
    if "logs" not in st.session_state:
        st.session_state.logs = load_logs_from_file()

    st.title("API Scheduler")

    task_name = st.text_input("Task Name")
    model_name = st.text_input("Model Name")
    model_id = st.text_input("Model ID")
    api_type = st.selectbox("Type of API Call", ["Import", "Export", "Process", "Delete"])
    action_id = st.text_input("Action ID")
    frequency = st.number_input("Frequency (in seconds)", min_value=1)
    active = st.checkbox("Active?", value=True)

    if st.button("Add Task"):
        task = {
            "task_name": task_name,
            "model_name": model_name,
            "model_id": model_id,
            "api_type": api_type,
            "action_id": action_id,
            "frequency": frequency,
            "active": active,
            "last_run": "Never"
        }
        st.session_state.tasks.append(task)
        save_tasks_to_file(st.session_state.tasks)
        st.success("Task added successfully!")

    st.write("Scheduled Tasks:")
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([2, 2, 2, 2, 2, 1, 1, 2, 2])
    with col1:
        st.write("**Task Name**")
    with col2:
        st.write("**Model Name**")
    with col3:
        st.write("**Model ID**")
    with col4:
        st.write("**Type of API Call**")
    with col5:
        st.write("**Action ID**")
    with col6:
        st.write("**Frequency (seconds)**")
    with col7:
        st.write("**Active**")
    with col8:
        st.write("**Toggle Active**")
    with col9:
        st.write("**Last Run**")

    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([2, 2, 2, 2, 2, 1, 1, 2, 2])
        with col1:
            st.write(task["task_name"])
        with col2:
            st.write(task["model_name"])
        with col3:
            st.write(task["model_id"])
        with col4:
            st.write(task["api_type"])
        with col5:
            st.write(task["action_id"])
        with col6:
            st.write(task["frequency"])
        with col7:
            st.write("Active" if task["active"] else "Inactive")
        with col8:
            if st.button("Toggle Active", key=f"toggle_{i}_{task['task_name']}"):
                st.session_state.tasks[i]["active"] = not st.session_state.tasks[i]["active"]
                save_tasks_to_file(st.session_state.tasks)
                st.query_params.update()
        with col9:
            st.write(task["last_run"])

    # Start the scheduler thread if not already running
    if "scheduler_thread" not in st.session_state:
        st.session_state.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        st.session_state.scheduler_thread.start()

    # Display logs
    st.write("Run Logs:")
    for log in st.session_state.logs:
        st.write(log)

def main():
    schedule_api_calls()

if __name__ == "__main__":
    main()