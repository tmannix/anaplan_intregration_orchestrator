import streamlit as st
import requests

# Function to call the Anaplan API with pagination support
def call_anaplan_api(api_type, model_id=None, import_id=None, export_id=None):
    headers = {
        "Authorization": f"Bearer {st.session_state.auth_token}",
        "Content-Type": "application/json"
    }

    def fetch_all_pages(api_url, key):
        all_data = []
        offset = 0
        while True:
            response = requests.get(f"{api_url}?offset={offset}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                all_data.extend(data.get(key, []))
                if len(data.get(key, [])) < 100:
                    break
                offset += 100
            else:
                st.error(f"Failed to fetch data from API: {response.status_code}")
                st.error(response.text)
                return None
        return all_data

    if api_type == "Get Model IDs":
        api_url = "https://api.anaplan.com/2/0/models"
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            models = response.json().get('models', [])
            filtered_models = [model for model in models if model.get('activeState') == 'PRODUCTION']
            return filtered_models
        else:
            st.error(f"Failed to fetch data from API: {response.status_code}")
            st.error(response.text)
            return None
    elif api_type == "Get Process ID":
        api_url = f"https://api.anaplan.com/2/0/models/{model_id}/processes"
        return fetch_all_pages(api_url, 'processes')
    elif api_type == "Get Action ID":
        api_url = f"https://api.anaplan.com/2/0/models/{model_id}/actions"
        return fetch_all_pages(api_url, 'actions')
    elif api_type == "Get Import ID":
        api_url = f"https://api.anaplan.com/2/0/models/{model_id}/imports"
        return fetch_all_pages(api_url, 'imports')
    elif api_type == "Get Export ID":
        api_url = f"https://api.anaplan.com/2/0/models/{model_id}/exports"
        return fetch_all_pages(api_url, 'exports')
    elif api_type == "Get Export Metadata":
        api_url = f"https://api.anaplan.com/2/0/models/{model_id}/exports/{export_id}"
        response = requests.get(api_url, headers=headers)
    elif api_type == "Get Import Metadata":
        api_url = f"https://api.anaplan.com/2/0/models/{model_id}/imports/{import_id}"
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

        if api_type == "Get Import ID":
            if model_id and st.button("Fetch Import IDs"):
                imports = call_anaplan_api(api_type, model_id)
                if imports:
                    st.session_state.imports = imports
                    st.write("Fetched Imports:", imports)

        if "imports" in st.session_state:
            import_names = [imp['name'] for imp in st.session_state.imports]
            selected_import_name = st.selectbox("Select Import Name", import_names)
            selected_import = next((imp for imp in st.session_state.imports if imp['name'] == selected_import_name), None)
            if selected_import:
                import_id = selected_import['id']

        if api_type == "Get Export ID":
            if model_id and st.button("Fetch Export IDs"):
                exports = call_anaplan_api(api_type, model_id)
                if exports:
                    st.session_state.exports = exports
                    st.write("Fetched Exports:", exports)

        if "exports" in st.session_state:
            export_names = [exp['name'] for exp in st.session_state.exports]
            selected_export_name = st.selectbox("Select Export Name", export_names)
            selected_export = next((exp for exp in st.session_state.exports if exp['name'] == selected_export_name), None)
            if selected_export:
                export_id = selected_export['id']

        if api_type in ["Get Import Metadata"]:
            if not import_id:
                import_id = st.text_input("Enter Import ID")

        if api_type in ["Get Export Metadata"]:
            if not export_id:
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