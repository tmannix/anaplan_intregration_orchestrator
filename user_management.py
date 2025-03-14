import streamlit as st
import requests
import pandas as pd
from datetime import datetime


def fetch_users(auth_token):
    anaplan_users_url = "https://us1a.app.anaplan.com/2/0/users"
    headers = {
        "Authorization": f"AnaplanAuthToken {auth_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(anaplan_users_url, headers=headers, verify=False)
    if response.status_code == 200:
        users = response.json()
        users_df = pd.DataFrame(users['users'])
        users_df['lastLoginDate'] = pd.to_datetime(users_df['lastLoginDate'], format='ISO8601')
        if users_df['lastLoginDate'].dt.tz is None:
            users_df['lastLoginDate'] = users_df['lastLoginDate'].dt.tz_localize('UTC')
        else:
            users_df['lastLoginDate'] = users_df['lastLoginDate'].dt.tz_convert('UTC')
        return users_df
    else:
        st.error(f"Failed to retrieve users: {response.status_code} - {response.text}")
        return pd.DataFrame()

def update_user_status(auth_token, user_id, active_status):
    url = f'https://api.anaplan.com/scim/1/0/v2/Users/{user_id}'
    data = {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
        "Operations": [{
            "op": "replace",
            "path": "active",
            "value": active_status
        }]
    }
    headers = {
        "Authorization": f"AnaplanAuthToken {auth_token}",
        "Content-Type": "application/json"
    }
    response = requests.patch(url, headers=headers, json=data, verify=False)
    if response.status_code == 200:
        return True
    else:
        st.error(f"Failed to update user {user_id}: {response.status_code} - {response.text}")
        return False

def send_teams_webhook(webhook_url, updated_users):
    message = {
        "title": "User Status Update",
        "text": "The following users have been updated:\n\n" + "\n".join([f"{user['email']}: {'Enabled' if user['active'] else 'Disabled'}" for user in updated_users])
    }
    response = requests.post(webhook_url, json=message)
    if response.status_code == 200:
        st.success("Teams notification sent successfully!")
    else:
        st.error(f"Failed to send Teams notification: {response.status_code} - {response.text}")

def main():
    st.title("📊 Anaplan Users Dashboard")
    st.write("Use this dashboard to view and filter Anaplan users.")
    
    auth_token = st.session_state.get("auth_token")
    if not auth_token:
        st.error("Please authenticate first.")
        return
    
    col1, col2, col3 = st.columns([2, 4, 2])
    with col1:
        if st.button("Run API"):
            st.session_state['users_df'] = fetch_users(auth_token)
            st.session_state['data_fetched'] = True
    
    if 'data_fetched' in st.session_state:
        users_df = st.session_state['users_df'].copy()
        
        st.sidebar.header("Filter Options")
        filter_columns = st.sidebar.multiselect("Select columns to filter by", users_df.columns)
        
        for filter_column in filter_columns:
            if filter_column == 'lastLoginDate':
                filter_condition = st.sidebar.selectbox(f"Select filter condition for {filter_column}", ["Greater than", "Less than", "Equal to"], key=f"{filter_column}_condition")
                filter_value = st.sidebar.date_input(f"Select date for {filter_column}", key=f"{filter_column}_value")
                filter_value = pd.to_datetime(filter_value).tz_localize('UTC')
                if filter_condition == "Greater than":
                    users_df = users_df[users_df['lastLoginDate'] > filter_value]
                elif filter_condition == "Less than":
                    users_df = users_df[users_df['lastLoginDate'] < filter_value]
                elif filter_condition == "Equal to":
                    users_df = users_df[users_df['lastLoginDate'] == filter_value]
            else:
                filter_value = st.sidebar.text_input(f"Enter filter value for {filter_column}", key=f"{filter_column}_value")
                if filter_value:
                    users_df = users_df[users_df[filter_column].astype(str).str.contains(filter_value, case=False)]
        
        st.subheader("Update User Status")
        disabled_columns = [col for col in users_df.columns if col != 'active']
        edited_df = st.data_editor(users_df, use_container_width=True, disabled=disabled_columns)
        
        changes_df = edited_df[edited_df.ne(st.session_state['users_df']).any(axis=1)]
        st.session_state['changes_df'] = changes_df
        
        st.subheader("Who has changed?")
        st.dataframe(st.session_state['changes_df'], use_container_width=True)
        
        if st.button("Update User Status"):
            updated_users = []
            for index, row in st.session_state['changes_df'].iterrows():
                user_id = row['id']
                active_status = row['active']
                if update_user_status(auth_token, user_id, active_status):
                    updated_users.append({'email': row['email'], 'active': active_status})
            if updated_users:
                updated_users_df = pd.DataFrame(updated_users)
                st.subheader("Updated Users")
                st.dataframe(updated_users_df, use_container_width=True)
                
                webhook_url = "https://asdauk.webhook.office.com/webhookb2/2391f54e-1b00-465e-a202-d3d121a3adcf@b63ee29f-aaa6-4d4e-8267-1d6dca9c0e43/IncomingWebhook/4d64c54dd84f4e71b9b5f4df03f67e4d/39c87cc3-965e-4fe1-b4b2-d9d6bd260050/V2ypBvmBwlTNY4DStecCpqIe6nECNAqxCK7zJ3c5evDCo1"
                send_teams_webhook(webhook_url, updated_users)

if __name__ == "__main__":
    main()
