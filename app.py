import streamlit as st
import os
import uuid
from utils import extract_text_from_pdf
from graph_logic import factory_graph

# 1. Page Config
st.set_page_config(page_title="AI Factory Pro", layout="wide", initial_sidebar_state="expanded")

# 2. THE DESIGNER CSS (The "Secret Sauce" for the look you want)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    
    /* Card Container Logic */
    .content-card {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Glowing Success Message */
    .stAlert {
        background-color: rgba(35, 134, 54, 0.1) !important;
        border: 1px solid #238636 !important;
        color: #3fb950 !important;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px 8px 0 0;
        color: #8b949e;
        padding: 0 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #21262d !important;
        border-bottom: 2px solid #58a6ff !important;
        color: #58a6ff !important;
    }
    
    /* Image Polish */
    img {
        border-radius: 10px;
        border: 1px solid #30363d;
        transition: transform 0.3s ease;
    }
    img:hover {
        transform: scale(1.02);
        border-color: #58a6ff;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. History Logic
if "history" not in st.session_state:
    st.session_state.history = {} 
if "current_thread_id" not in st.session_state:
    st.session_state.current_thread_id = str(uuid.uuid4())

# --- Sidebar History ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>📁 Projects</h2>", unsafe_allow_html=True)
    if st.button("➕ Start New Project"):
        st.session_state.current_thread_id = str(uuid.uuid4())
        st.rerun()
    
    st.markdown("<br><p style='color:#8b949e; font-size:12px;'>SAVED SESSIONS</p>", unsafe_allow_html=True)
    for tid in list(st.session_state.history.keys()):
        if st.button(f"Project {tid[:8]}", key=tid):
            st.session_state.current_thread_id = tid
            st.rerun()

# --- Main Interface ---
current_tid = st.session_state.current_thread_id
st.markdown(f"<h1 style='letter-spacing:-1px;'>🏭 AI Content Factory</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#8b949e;'>Active Thread: <span style='color:#58a6ff;'>{current_tid}</span></p>", unsafe_allow_html=True)

# Main Interaction Logic
if current_tid in st.session_state.history:
    data = st.session_state.history[current_tid]
    st.markdown('<div class="stAlert">✔️ Session successfully loaded from memory.</div>', unsafe_allow_html=True)
else:
    with st.container():
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Source PDF", type="pdf")
        if uploaded_file and st.button("🚀 Execute Production"):
            config = {"configurable": {"thread_id": current_tid}}
            with st.status("⚡ Orchestrating Nodes...", expanded=True) as status:
                text = extract_text_from_pdf(uploaded_file)
                result = factory_graph.invoke({"raw_text": text}, config)
                st.session_state.history[current_tid] = result
                status.update(label="Production Complete!", state="complete")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- Output Display ---
if current_tid in st.session_state.history:
    res = st.session_state.history[current_tid]
    t1, t2, t3 = st.tabs(["🎬 Video Script", "🖼️ Storyboard", "🐦 Twitter"])
    
    with t1:
        st.markdown(f'<div class="content-card">{res.get("video_script", "")}</div>', unsafe_allow_html=True)
    
    with t2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        imgs = res.get("image_prompts", [])
        if imgs:
            cols = st.columns(2)
            for idx, p in enumerate(imgs):
                with cols[idx % 2]:
                    if os.path.exists(p):
                        st.image(p, caption=f"SCENE {idx+1}", width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with t3:
        st.markdown(f'<div class="content-card">{res.get("twitter_thread", "")}</div>', unsafe_allow_html=True)