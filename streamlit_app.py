import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Health Chatbot 🤖")

# System prompt to keep the assistant focused on health advice
SYSTEM_PROMPT = (
    "You are a helpful and responsible health assistant. You only answer questions related to health, "
    "wellness, or medical topics. If a question is outside of this domain, politely refuse."
)

# Initialize session history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Display conversation history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Function to check if prompt is medical using GPT
def is_medical_query(prompt):
    check_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a classifier that answers only YES or NO."},
            {"role": "user", "content": f"Is this input related to health, medicine or wellness? '{prompt}' Just answer YES or NO."}
        ]
    )
    answer = check_response.choices[0].message.content.strip().upper()
    return answer.startswith("YES")

# Get assistant's response
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages + [{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Chat input
user_input = st.chat_input("Describe your symptoms here...")

# Handle input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if is_medical_query(user_input):
        assistant_prompt = f"The user has described: {user_input}. Provide general health advice (not a diagnosis)."
        reply = get_response(assistant_prompt)
    else:
        reply = (
            "⚠️ I'm only able to assist with medical, wellness, or health-related topics. "
            "Please ask a health-related question."
        )

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

# Disclaimer
st.markdown("---")
st.markdown(
    "🛑 **Disclaimer:** This assistant provides general health-related guidance. "
    "Always consult a certified medical professional for diagnosis and treatment."
)
