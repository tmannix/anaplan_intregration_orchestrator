import streamlit as st
from auth_page import main as auth_page_main
from get_anaplan_ids import main as get_anaplan_id_main
from scheduler import main as scheduler_main
from user_management import main as user_management_main
from guide import main as guide_main
from run_api import main as run_api_main

# Set up page configuration
st.set_page_config(
    page_title="Anaplan Integration Helper",
    page_icon=":guardsman:",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Sidebar for navigation
st.sidebar.title("Anaplan Integration Helper")
selected = st.sidebar.radio(
    "Go to",
    ["Home", "Guide", "Authentication", "Get Anaplan IDs", "Run API", "Scheduler", "User Management"],
    index=0
)

# Main app logic
if selected == "Home":
    st.title("Streamline Your Anaplan Integration with Ease")
    st.subheader("Effortlessly manage APIs, schedule processes, and handle user management within your Anaplan Tenant.")
    
    try:
        st.image("https://i.imgur.com/q97MwMQ.jpeg", use_container_width=True)
    except Exception as e:
        st.error(f"Error loading image: {e}")
    
    st.markdown("""
    ### Key Features
    - **API Integration**: Seamlessly connect and manage APIs within your Anaplan Tenant.
    - **Process Scheduling**: Automate and schedule ongoing processes for efficiency.
    - **User Management**: Simplify user management tasks with intuitive tools.
    
    ### Benefits
    - **Increased Efficiency**: Save time by automating repetitive tasks.
    - **Improved Accuracy**: Reduce errors with reliable API integrations.
    - **Enhanced Control**: Easily manage users and processes from a single interface.
    
    ### Testimonials
    > "This app has transformed how we manage our Anaplan processes. It's a game-changer!"
    """)

elif selected == "Guide":
    guide_main()
elif selected == "Authentication":
    auth_page_main()
elif selected == "Get Anaplan IDs":
    get_anaplan_id_main()
elif selected == "Run API":
    run_api_main()
elif selected == "Scheduler":
    scheduler_main()
elif selected == "User Management":
    user_management_main()
