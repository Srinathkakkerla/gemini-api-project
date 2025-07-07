import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gemini.chat import ChatGemini

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(page_title="Gemini Pro Streamlit Chatbot", layout="wide")
st.title("💬 Gemini Pro Streamlit Chatbot")

# Initialize chat class
gemini_chat = ChatGemini()

# Chat history session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input at the bottom
user_input = st.chat_input("Type your message here...")

# First handle the response
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    try:
        response = gemini_chat.get_gemini_response(user_input)
        st.session_state.chat_history.append(("bot", response))
    except Exception as e:
        st.error(f"Error generating response: {e}")

# Now display the chat history
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
