import streamlit as st
from openai import OpenAI
import re

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Health Chatbot 🤖💬")

# System prompt to keep it focused
SYSTEM_PROMPT = (
    "You are a health assistant. Only provide advice for medical, health, or wellness-related issues. "
    "Do not answer anything unrelated. If asked non-health questions, politely decline."
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Display chat history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Describe your symptoms here...")

# Keyword-based health check (improved)
def is_health_related(prompt):
    HEALTH_TERMS = [
        "pain", "fever", "gas", "bloating", "tightness", "headache", "dizzy",
        "sick", "ill", "vomit", "diarrhea", "symptom", "nausea", "cramp", "burn",
        "chest", "stomach", "cough", "flu", "infection", "allergy", "rash", "pressure",
        "mental", "anxiety", "stress", "tired", "exhausted", "cold", "constipation",
        "digestion", "digestive", "relieve", "relief", "breathing", "fatigue"
    ]
    prompt = prompt.lower()
    return any(word in prompt for word in HEALTH_TERMS)

# Function to get assistant response
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages + [{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Process input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if is_health_related(user_input):
        assistant_prompt = (
            f"The user has described the following issue: {user_input}. "
            f"Please provide general health guidance or remedies. Avoid any diagnosis."
        )
        reply = get_response(assistant_prompt)
    else:
        reply = (
            "⚠️ I'm here to assist only with health and wellness-related questions. "
            "Please rephrase your query to describe a medical concern."
        )

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

# Footer disclaimer
st.markdown("---")
st.markdown(
    "🛑 **Disclaimer:** This chatbot is for informational purposes only and does not replace professional medical advice. "
    "Please consult a healthcare provider for diagnosis and treatment."
)
