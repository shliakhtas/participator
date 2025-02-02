import requests
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = os.environ.get("LANGFLOW_ID")
FLOW_ID = os.environ.get("FLOW_ID")
APPLICATION_TOKEN = os.environ.get("APPLICATION_TOKEN")
ENDPOINT = "participator"  # The endpoint name of the flow

SCENARIOS = {
    "Перегоріла лампочка в під'їзді": ("Я", "Сусід"),
    "Не вивезли вчасно сміття": ("Я", "КП"),
    "Шумить паб після 23:00": ("Я", "Бізнес"),
    "Знайти гранти на освітлення": ("Я", "Організація/Міська влада"),
    "Знайти куди виділити кошти": ("Організація/Міська влада", "Я"),
    "Попереписуватись з Садовим про потреби міста": ("Я", "Організація/Міська влада"),
}

def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    
    # Make the API request to the flow endpoint
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    st.title("Participator Demo")

    # Add secret key authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        secret_key = st.text_input("Enter secret key:", type="password")
        if secret_key == "512":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Please enter the correct secret key to access the chat")
            return

    # Scenario selector
    scenario = st.selectbox("Choose a scenario:", list(SCENARIOS.keys()))
    chat1_name, chat2_name = SCENARIOS[scenario]

    # Manage session state for messages and responses
    if 'messages' not in st.session_state:
        st.session_state.messages = {"chat1": "", "chat2": ""}
        st.session_state.responses = {"chat1": "", "chat2": ""}

    # Create layout for the two chat columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(chat1_name)
        message1 = st.text_area(f"Message ({chat1_name})", value=st.session_state.messages["chat1"], placeholder=f"Write as {chat1_name}...")
        if st.button(f"Send from {chat1_name}"):
            if not message1.strip():
                st.error(f"Please enter a message for {chat1_name}")
            else:
                with st.spinner(f"Processing message from {chat1_name}..."):
                    try:
                        response1 = run_flow(message1)
                        response_text = response1["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                        st.session_state.messages["chat1"] = message1
                        st.session_state.responses["chat1"] = response_text
                        st.markdown(f"**{chat1_name}:** {response_text}")
                    except Exception as e:
                        st.error(str(e))

    with col2:
        st.subheader(chat2_name)
        message2 = st.text_area(f"Message ({chat2_name})", value=st.session_state.messages["chat2"], placeholder=f"Write as {chat2_name}...")
        if st.button(f"Send from {chat2_name}"):
            if not message2.strip():
                st.error(f"Please enter a message for {chat2_name}")
            else:
                with st.spinner(f"Processing message from {chat2_name}..."):
                    st.session_state.messages["chat2"] = message2
                    st.session_state.responses["chat2"] = f"I'm chat {chat2_name}"
                    st.markdown(f"**{chat2_name}:** I'm chat {chat2_name}")
                    
        # Display the stored response for chat 2
        if st.session_state.responses["chat2"]:
            st.markdown(f"**{chat2_name}:** {st.session_state.responses['chat2']}")

if __name__ == "__main__":
    main()
