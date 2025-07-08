import os
import sys
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gemini.chat import ChatGemini

# ------------------ Environment Setup ------------------
load_dotenv()

# ------------------ Page Config ------------------
st.set_page_config(page_title="Gemini Pro Streamlit Chatbot", layout="wide")
st.title("💬 Gemini Pro Streamlit Chatbot")

# ------------------ Initialize Gemini Chat Class ------------------
gemini_chat = ChatGemini()

# ------------------ Session Prompt Count ------------------
if "prompt_count" not in st.session_state:
    st.session_state.prompt_count = 0

# ------------------ Hidden Logging Function ------------------
def log_usage(prompt):
    with open("chatbot_logs.txt", "a") as logfile:
        logfile.write(f"[{datetime.now()}] Prompt: {prompt}\n")

# ------------------ Chat History Session State ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------ User Chat Input ------------------
user_input = st.chat_input("Type your message here...")

# ------------------ Handle Chat Response ------------------
if user_input:
    if st.session_state.prompt_count < 5:  # Limit to 5 prompts/session
        st.session_state.prompt_count += 1

        # Log the prompt
        log_usage(user_input)

        # Append user message
        st.session_state.chat_history.append(("user", user_input))
        try:
            # Call Gemini API and append bot response
            response = gemini_chat.get_gemini_response(user_input)
            st.session_state.chat_history.append(("bot", response))
        except Exception as e:
            st.error(f"Error generating response: {e}")
    else:
        st.warning("⚠️ You’ve reached the maximum prompts for this session. Please refresh the page to try again later.")

# ------------------ Chat History Display ------------------
user_image_path = os.path.join(os.path.dirname(__file__), "assets", "user.jpg")
bot_image_path = os.path.join(os.path.dirname(__file__), "assets", "bot.jpg")

for role, message in st.session_state.chat_history:
    with st.container():
        if role == "user":
            col1, col2 = st.columns([1, 9])
            with col1:
                st.image(user_image_path, width=50)
            with col2:
                st.markdown(f"""
                <div style='background-color:#f0f0f5; padding:10px; border-radius:10px;'>
                    <strong>You:</strong> {message}
                </div>
                """, unsafe_allow_html=True)
        else:
            col1, col2 = st.columns([9, 1])
            with col2:
                st.image(bot_image_path, width=50)
            with col1:
                st.markdown(f"""
                <div style='background-color:#e6f2ff; padding:10px; border-radius:10px;'>
                    <strong>Gemini:</strong> {message}
                </div>
                """, unsafe_allow_html=True)

# ------------------ Optional Prompt Usage Counter ------------------
st.caption(f"Prompts used this session: {st.session_state.prompt_count}/5")
