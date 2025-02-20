import streamlit as st
import requests

# Function to call the Anaplan API
def call_anaplan_api(api_type, model_id=None, import_id=None, export_id=None):
    headers = {
        "Authorization": f"Bearer {st.session_state.auth_token}",
        "Content-Type": "application/json"
    }

    if api_type == "Get Model IDs":
        api_url = "https://api.anaplan.com/2/0/models"
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            models = response.json().get('models', [])
            # Filter models where activeState is PRODUCTION
            filtered_models = [model for model in models if model.get('activeState') == 'PRODUCTION']
            return filtered_models
        else:
            st.error(f"Failed to fetch data from API: {response.status_code}")
            st.error(response.text)
            return None
    elif api_type == "Get Process ID":
        api_url = f"https://api.anaplan.com/2/0/models/{model_id}/processes"
        response = requests.get(api_url, headers=headers)
    elif api_type == "Get Action ID":
        api_url = f"https://api.anaplan.com/2/0/models/{model_id}/actions"
        response = requests.get(api_url, headers=headers)
    elif api_type == "Get Import ID":
        api_url = f"https://api.anaplan.com/2/0/models/{model_id}/imports"
        response = requests.get(api_url, headers=headers)
    elif api_type == "Get Export ID":
        api_url = f"https://api.anaplan.com/2/0/models/{model_id}/exports"
        response = requests.get(api_url, headers=headers)
    elif api_type == "Get Export Metadata":
        api_url = f"https://api.anaplan.com/2/0/models/{model_id}/exports/{export_id}/metadata"
        response = requests.get(api_url, headers=headers)
    elif api_type == "Get Import Metadata":
        api_url = f"https://api.anaplan.com/2/0/models/{model_id}/imports/{import_id}/metadata"
        response = requests.get(api_url, headers=headers)
    else:
        st.error("Invalid API type selected")
        return None

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data from API: {response.status_code}")
        st.error(response.text)
        return None

# Streamlit app
def main():
    st.title("API Call Page")

    if "auth_token" in st.session_state:
        api_type = st.selectbox(
            "Select API Type",
            ["Get Model IDs", "Get Process ID", "Get Action ID", "Get Import ID", "Get Export ID", "Get Export Metadata", "Get Import Metadata"]
        )

        model_id = None
        import_id = None
        export_id = None

        if api_type == "Get Model IDs":
            if st.button("Fetch Model IDs"):
                models = call_anaplan_api(api_type)
                if models:
                    st.session_state.models = models
                    st.write("Fetched Models:", models)

        if "models" in st.session_state:
            model_names = [model['name'] for model in st.session_state.models]
            selected_model_name = st.selectbox("Select Model Name", model_names)
            selected_model = next((model for model in st.session_state.models if model['name'] == selected_model_name), None)
            if selected_model:
                model_id = selected_model['id']

        if api_type in ["Get Process ID", "Get Action ID", "Get Import ID", "Get Export ID", "Get Export Metadata", "Get Import Metadata"]:
            if not model_id:
                model_id = st.text_input("Enter Model ID")

        if api_type in ["Get Import Metadata"]:
            import_id = st.text_input("Enter Import ID")

        if api_type in ["Get Export Metadata"]:
            export_id = st.text_input("Enter Export ID")

        if st.button("Run API"):
            data = call_anaplan_api(api_type, model_id, import_id, export_id)
            if data:
                st.session_state.api_data = data

        if "api_data" in st.session_state:
            search_query = st.text_input("Search API Data")
            if search_query:
                filtered_data = [item for item in st.session_state.api_data if search_query.lower() in str(item).lower()]
                st.write(f"Filtered API Data for {api_type}:", filtered_data)
            else:
                st.write(f"API Data for {api_type}:", st.session_state.api_data)
    else:
        st.warning("Please authenticate first")

if __name__ == "__main__":
    main()