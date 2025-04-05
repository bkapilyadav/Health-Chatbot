import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app
st.title("Health Chatbot")

# Guardrails: Define system instructions
SYSTEM_PROMPT = (
    "You are a helpful health assistant. "
    "You must not provide medical diagnoses, prescriptions, or treatment plans. "
    "Only provide general wellness advice and suggest consulting a licensed medical professional. "
    "Avoid suggesting specific medications or medical procedures. "
    "Always include a disclaimer that this is not a substitute for professional medical advice."
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Display chat history
for message in st.session_state.messages[1:]:  # skip system prompt from UI
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Collect user input for symptoms
user_input = st.chat_input("Describe your symptoms here...")

# Function to get a response from OpenAI with health-safe guardrails
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages + [{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Process and display response if there's input
if user_input:
    # Append user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Create the assistant prompt with a subtle framing
    assistant_prompt = (
        f"A user has described their symptoms as: {user_input}. "
        "Provide general wellness suggestions only, based on common health knowledge. "
        "Do not diagnose or offer treatment. Suggest visiting a doctor."
    )

    assistant_response = get_response(assistant_prompt)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
