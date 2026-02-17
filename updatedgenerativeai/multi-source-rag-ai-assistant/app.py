# app.py
import streamlit as st
from datetime import datetime

# ────────────────────────────────────────────────
# Page config
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="Chat • Test",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Very basic dark mode look (optional — you can remove or move to .streamlit/config.toml)
st.markdown(
    """
    <style>
        .stApp {
            background-color: #0e1117;
            color: #e0e0e0;
        }
        .stChatMessage.user {
            background-color: #1e3a5f !important;
        }
        .stChatMessage.assistant {
            background-color: #2d1e4a !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ────────────────────────────────────────────────
# Session state for messages
# ────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ────────────────────────────────────────────────
# Sidebar
# ────────────────────────────────────────────────
with st.sidebar:
    st.header("Chat controls")
    
    if st.button("Clear conversation", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.caption(f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    st.caption("Minimal chat UI — Feb 2026")

# ────────────────────────────────────────────────
# Main area — title + chat history + input
# ────────────────────────────────────────────────
st.title("💬 Simple Streamlit Chat")
st.caption("Just the UI part — no backend yet")

# Show all previous messages
for message in st.session_state.messages:
    role = message["role"]
    avatar = "👤" if role == "user" else "🤖"
    
    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])

# Chat input at the bottom
if prompt := st.chat_input("Type your message here…"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Fake assistant reply (placeholder — replace later with real call)
    fake_reply = (
        f"You wrote: **{prompt}**\n\n"
        "This is a placeholder response.\n\n"
        "Later this will be replaced with your real RAG / LLM answer."
    )
    
    st.session_state.messages.append({"role": "assistant", "content": fake_reply})
    
    # Re-run to show the new messages immediately
    st.rerun()