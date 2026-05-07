import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=api_key)

# Streamlit page settings
st.set_page_config(
    page_title="Groq Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Simple GenAI Chatbot")
st.write("Powered by Groq + Streamlit")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask something...")

if prompt:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        full_response = ""

        # Stream response from Groq
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=1024,
            stream=True
        )

        for chunk in completion:

            content = chunk.choices[0].delta.content

            if content:

                full_response += content

                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )