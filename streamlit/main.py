import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from dotenv import load_dotenv
from gemini.chat import ChatGemini

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(page_title="Gemini Pro Streamlit Chatbot", layout="centered")

# Dark/Light mode toggle
mode = st.sidebar.selectbox("Theme", ["Light", "Dark"])
background = "#FFFFFF" if mode == "Light" else "#1E1E1E"
text_color = "#000000" if mode == "Light" else "#FFFFFF"
user_bubble = "#DCF8C6" if mode == "Light" else "#2E7D32"
bot_bubble = "#F1F0F0" if mode == "Light" else "#333333"

# Page Title
st.markdown(
    f"<h1 style='color:{text_color}; text-align:center;'>💬 Gemini Pro Streamlit Chatbot</h1>",
    unsafe_allow_html=True
)

# Initialize Gemini
gemini_chat = ChatGemini()

# Image Paths
USER_IMG = "assets/user.jpg"
BOT_IMG = "assets/bot.jpg"

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat Messages Display
for i, (role, message) in enumerate(st.session_state.chat_history):
    col1, col2 = st.columns([1, 9]) if role == "user" else st.columns([9, 1])
    bubble_color = user_bubble if role == "user" else bot_bubble
    image = USER_IMG if role == "user" else BOT_IMG

    with col1 if role == "user" else col2:
        st.image(image, width=60)
    with col2 if role == "user" else col1:
        st.markdown(
            f"""
            <div style='
                background-color:{bubble_color};
                color:{text_color};
                padding: 12px;
                border-radius: 10px;
                margin-bottom: 5px;
                font-family: Arial, sans-serif;
                line-height: 1.5;
            '>{message}</div>
            """,
            unsafe_allow_html=True,
        )

# Scroll to bottom hack
st.markdown("<div id='chat-bottom'></div>", unsafe_allow_html=True)

# Input box
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    try:
        response = gemini_chat.get_gemini_response(user_input)
        st.session_state.chat_history.append(("bot", response))
    except Exception as e:
        st.error(f"Error generating response: {e}")
    # Scroll trigger
    st.markdown(
        "<script>document.getElementById('chat-bottom').scrollIntoView({behavior: 'smooth'});</script>",
        unsafe_allow_html=True
    )
