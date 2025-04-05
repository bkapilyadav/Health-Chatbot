import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using API key from secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app
st.title("Health Chatbot 🤖🩺")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are a helpful, medically-aware health assistant. "
            "You provide general advice and suggestions for common health symptoms. "
            "You DO NOT give diagnoses or treatments. "
            "Always encourage users to consult a doctor for any serious or persistent symptoms. "
            "Do not respond to questions unrelated to health or wellness."
        )}
    ]

# Display chat history
for message in st.session_state.messages[1:]:  # skip system prompt
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Collect user input
user_input = st.chat_input("Describe your symptoms or ask a health-related question...")

# Function to check if input is health-related (simple heuristic-based)
def is_health_related(prompt):
    keywords = [
        "pain", "symptom", "stomach", "headache", "fever", "gas", "acidity", "cold", "cough",
        "nausea", "vomit", "diarrhea", "what should I eat", "what to eat", "what can I take",
        "medication", "remedy", "home remedy", "medicine", "bloating", "tired", "weak", "ill", "sick"
    ]
    return any(kw in prompt.lower() for kw in keywords)

# Function to get GPT response
def get_response():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )
    return response.choices[0].message.content

# Main logic for handling input
if user_input:
    # Check if input is health-related
    if is_health_related(user_input):
        # Append user's message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get assistant response
        assistant_response = get_response()
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

        with st.chat_message("assistant"):
            st.markdown(assistant_response)
    else:
        # Reject non-health prompts
        with st.chat_message("assistant"):
            st.warning("⚠️ This chatbot only answers health-related queries. Please enter a valid symptom or health question.")

# Disclaimer
st.markdown("---")
st.markdown(
    "🛑 **Disclaimer:** This assistant provides general health-related guidance. "
    "Always consult a certified medical professional for diagnosis and treatment."
)
