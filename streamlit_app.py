import streamlit as st
from openai import OpenAI
from datetime import datetime
import pandas as pd
import os

# --- SETUP ---

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.title("Health Chatbot 🤖💊")

SYSTEM_PROMPT = (
    "You are a helpful health assistant. "
    "Do not provide medical diagnoses, prescriptions, or treatments. "
    "Only give general health and wellness advice. "
    "Always recommend consulting a licensed healthcare professional. "
    "Avoid discussing medications or procedures."
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

# --- RESPONSE FUNCTION WITH LOGGING ---

def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages + [{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- PROCESS INPUT ---

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    assistant_prompt = (
        f"A user has described symptoms as: {user_input}. "
        "Provide safe, general wellness suggestions. Avoid medical advice."
    )
    response = get_response(assistant_prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)

        # Rating + Flagging UI
        col1, col2 = st.columns(2)
        with col1:
            feedback = st.radio("Rate this response", ["👍", "👎"], horizontal=True)
        with col2:
            flag = st.checkbox("🚩 Flag this response")

        # Log entry
        st.session_state.log.append({
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "response": response,
            "feedback": feedback,
            "flagged": flag
        })

# --- DOWNLOADABLE LOG HISTORY ---

if st.session_state.log:
    df_log = pd.DataFrame(st.session_state.log)
    csv_log = df_log.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Chat Log", csv_log, file_name="health_chat_log.csv")

# --- FOOTER DISCLAIMER ---

st.markdown("---")
st.markdown(
    "⚠️ **Disclaimer:** This chatbot does not provide medical advice. "
    "It is intended for general wellness information only. "
    "Always consult with a licensed healthcare professional for medical concerns."
)
