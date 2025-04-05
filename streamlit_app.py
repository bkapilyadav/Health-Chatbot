import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title
st.title("Health Chatbot 🤖🩺")

# System guardrail: Medically-focused, general advice only
system_message = {
    "role": "system",
    "content": (
        "You are a friendly and helpful virtual health assistant. "
        "You provide general health advice based on symptoms the user reports. "
        "You do not provide diagnoses or prescriptions. "
        "You do not answer non-medical questions. "
        "Encourage users to consult healthcare professionals for any serious or persistent issues."
    )
}

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [system_message]

# Display existing chat messages
for msg in st.session_state.chat_history[1:]:  # skip system message in UI
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Collect user input
user_input = st.chat_input("Describe your symptoms or ask a health-related question...")

# Send full chat history to OpenAI and get response
def get_chat_response():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.chat_history
    )
    return response.choices[0].message.content

# Process user input
if user_input:
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get assistant response
    response = get_chat_response()
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)


# Disclaimer
st.markdown("---")
st.markdown(
    "🛑 **Disclaimer:** This assistant provides general health-related guidance. "
    "Always consult a certified medical professional for diagnosis and treatment."
)
