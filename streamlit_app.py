import streamlit as st
from openai import OpenAI
from datetime import datetime
import pandas as pd
import re

# --- SETUP ---

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.title("Health Chatbot 🤖💊")

# Define health-related keywords
HEALTH_KEYWORDS = [
    "symptom", "pain", "headache", "fever", "cough", "cold", "tired",
    "health", "medicine", "remedy", "treatment", "body", "wellness",
    "injury", "flu", "infection", "sick", "vomit", "dizzy", "nausea",
    "exercise", "nutrition", "mental", "stress", "anxiety", "fatigue",
    "allergy", "diarrhea", "burn", "rash", "cramp"
]

# System prompt enforcing strict behavior
SYSTEM_PROMPT = (
    "You are a health-focused AI assistant. You ONLY respond to questions "
    "about health, wellness, or general well-being. "
    "If a user asks about unrelated topics (like finance, politics, or entertainment), "
    "politely decline to answer. Never provide a diagnosis or prescription."
)

# --- SESSION STATE ---

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
if "log" not in st.session_state:
    st.session_state.log = []

# --- DISPLAY CHAT HISTORY ---

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT INPUT ---

user_input = st.chat_input("Describe your symptoms...")

# --- UTILITY: Check if input is health-related ---

def is_health_related(prompt):
    prompt_lower = prompt.lower()
    return any(re.search(rf"\b{kw}\b", prompt_lower) for kw in HEALTH_KEYWORDS)

# --- RESPONSE FUNCTION ---

def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages + [{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- PROCESS USER INPUT ---

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if is_health_related(user_input):
        assistant_prompt = (
            f"A user has described symptoms or asked a health question: {user_input}. "
            "Provide safe, general wellness suggestions only."
        )
        response = get_response(assistant_prompt)
    else:
        response = (
            "⚠️ I'm designed to assist **only with health and wellness-related questions**. "
            "Please describe symptoms or ask something health-specific."
        )

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

    # Log it
    st.session_state.log.append({
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "response": response,
        "is_health_related": is_health_related(user_input)
    })

# --- LOG DOWNLOAD ---

if st.session_state.log:
    df_log = pd.DataFrame(st.session_state.log)
    csv = df_log.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Chat Log", csv, "chat_log.csv")

# --- FOOTER DISCLAIMER ---

st.markdown("---")
st.markdown(
    "⚠️ **Disclaimer:** This chatbot is for informational purposes only. "
    "It does not provide medical diagnoses or treatments. "
    "Please consult a licensed healthcare provider for medical issues."
)
