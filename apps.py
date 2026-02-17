
# app.py
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ✅ import from your backend (bug-fixed backend.py)
from rag_backend import reg_simple, retriever, llm  # change filename if yours isn't backend.py

# ────────────────────────────────────────────────
# Page config
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Source RAG App • Asfand",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(
    """
    <style>
        /* ===== Main Background ===== */
        .stApp {
            background-color: #0b1220;
            color: #ffffff;
        }

        /* ===== Sidebar ===== */
        [data-testid="stSidebar"] {
            background-color: #111827;
        }

        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        /* ===== Headers ===== */
        h1, h2, h3, h4 {
            color: #ffffff !important;
        }

        /* ===== Normal Text ===== */
        p, span, label, div {
            color: #e5e7eb !important;
        }

        /* ===== Buttons ===== */
        .stButton > button {
            width: 100%;
            background-color: #2563eb;
            color: #ffffff;
            border-radius: 10px;
            border: none;
            padding: 0.6rem 1rem;
            font-weight: 600;
        }

        .stButton > button:hover {
            background-color: #1d4ed8;
        }

        /* ===== Chat Bubbles ===== */
        .stChatMessage.user {
            background-color: #1e293b !important;
            color: #ffffff !important;
            border-radius: 12px;
        }

        .stChatMessage.assistant {
            background-color: #f9fafb !important;
            color: #111827 !important;
            border-radius: 12px;
        }

        /* ===== Input Box ===== */
        textarea {
            background-color: #1f2937 !important;
            color: #ffffff !important;
            border-radius: 10px !important;
            border: 1px solid #374151 !important;
        }

        /* ===== Expander ===== */
        .stExpander {
            background-color: #1f2937 !important;
            border-radius: 10px;
        }

    </style>
    """,
    unsafe_allow_html=True
)
# ────────────────────────────────────────────────
# Session state initialization
# ────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vector_store_loaded" not in st.session_state:
    st.session_state.vector_store_loaded = True  # ✅ your backend already indexed at import time

# ────────────────────────────────────────────────
# Sidebar
# ────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Controls")

    # (kept as-is, doesn't affect your current backend)
    source_filter = st.multiselect(
        "Filter sources",
        options=["All", "Papers", "Notes", "Tweets"],
        default=["All"],
        help="Select which sources to query from"
    )

    if st.button("Clear conversation", type="primary"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    if st.button("Run evaluation"):
        with st.spinner("Evaluating..."):
            eval_results = "Placeholder eval: Faithfulness 0.85 | Relevancy 0.92"
        st.info(eval_results)

    st.caption(f"Built by Asfand • {datetime.now().year}")
    st.caption("v1.0 • Feb 2026")

# ────────────────────────────────────────────────
# Main chat area
# ────────────────────────────────────────────────
st.title(" Multi-Source RAG Chat")
st.caption("Ask questions about your papers, notes, and tweets. Sources cited inline.")

# Display chat history
for message in st.session_state.messages:
    role = message["role"]
    avatar = "👨‍💻" if role == "user" else "🤖"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask a question about your documents...")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(prompt)

    # Generate response with spinner
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Retrieving and generating..."):
            # ✅ your backend returns string only
            answer = reg_simple(prompt, retriever, llm, top_k=3)

        st.markdown(answer)

    # Add to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()
