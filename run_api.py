import streamlit as st
import requests
import pandas as pd
import json

def main():
    st.title("Run API Page")
    st.write("Use this page to run the API and retrieve data based on your selection.")
    
    if "auth_token" not in st.session_state:
        st.error("Please authenticate first on the Authentication page.")
        return

    auth_token = st.session_state["auth_token"]

    # Fetch workspaces
    workspaces = fetch_workspaces(auth_token)
    if workspaces is not None:
        workspace = st.selectbox("Select Workspace", workspaces, format_func=lambda x: x['name'])
        workspace_id = workspace['id']

        # Fetch models for the selected workspace
        models = fetch_models(auth_token, workspace_id)
        if models is not None:
            model = st.selectbox("Select Model", models, format_func=lambda x: x['name'])
            model_id = model['id']

            operation = st.selectbox("Select Operation", ["Process", "Import", "Export", "Action"])
            operation_id_label = f"{operation} ID"
            operation_id = st.text_input(operation_id_label)

            if st.button("Run API"):
                if not operation_id:
                    st.error("Please enter the Operation ID.")
                else:
                    if operation == "Export":
                        data = run_export(auth_token, workspace_id, model_id, operation_id)
                        if data is not None:
                            st.success(f"{operation} completed successfully!")
                            st.dataframe(data)
                            st.download_button(
                                label="Download data as CSV",
                                data=data.to_csv(index=False).encode('utf-8'),
                                file_name='export_data.csv',
                                mime='text/csv',
                            )
                    else:
                        success = run_anaplan_operation(auth_token, workspace_id, model_id, operation, operation_id)
                        if success:
                            st.success(f"{operation} completed successfully!")

def fetch_workspaces(auth_token):
    url = "https://api.anaplan.com/2/0/workspaces"
    headers = {
        "Authorization": f"AnaplanAuthToken {auth_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['workspaces']
    else:
        st.error(f"Failed to retrieve workspaces: {response.status_code} - {response.text}")
        return None

def fetch_models(auth_token, workspace_id):
    url = f"https://api.anaplan.com/2/0/workspaces/{workspace_id}/models"
    headers = {
        "Authorization": f"AnaplanAuthToken {auth_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['models']
    else:
        st.error(f"Failed to retrieve models: {response.status_code} - {response.text}")
        return None

def run_anaplan_operation(auth_token, workspace_id, model_id, operation, operation_id):
    url = f"https://api.anaplan.com/2/0/workspaces/{workspace_id}/models/{model_id}/{operation}s/{operation_id}/tasks"
    headers = {
        "Authorization": f"AnaplanAuthToken {auth_token}",
        "Content-Type": "application/json"
    }
    data = {
        "localeName": "en_US"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return True
    else:
        st.error(f"Failed to run {operation}: {response.status_code} - {response.text}")
        return False

def run_export(auth_token, workspace_id, model_id, export_id):
    url = f"https://api.anaplan.com/2/0/workspaces/{workspace_id}/models/{model_id}/exports/{export_id}/tasks"
    headers = {
        "Authorization": f"AnaplanAuthToken {auth_token}",
        "Content-Type": "application/json"
    }
    data = {
        "localeName": "en_US"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        task_id = response.json()["task"]["id"]
        return get_export_data(auth_token, workspace_id, model_id, export_id, task_id)
    else:
        st.error(f"Failed to run export: {response.status_code} - {response.text}")
        return None

def get_export_data(auth_token, workspace_id, model_id, export_id, task_id):
    url = f"https://api.anaplan.com/2/0/workspaces/{workspace_id}/models/{model_id}/exports/{export_id}/tasks/{task_id}/dump"
    headers = {
        "Authorization": f"AnaplanAuthToken {auth_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        df = pd.read_csv(response.content.decode('utf-8'))
        df = df.drop(columns=['lastlogindate'], errors='ignore')  # Exclude lastlogindate from the dataframe
        # Perform comparison excluding 'lastlogindate'
        columns_to_compare = [col for col in df.columns if col != 'lastlogindate']
        # Add your comparison logic here using columns_to_compare
        return df[columns_to_compare]
    else:
        st.error(f"Failed to get export data: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    main()
