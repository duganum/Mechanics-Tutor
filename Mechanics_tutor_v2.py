import streamlit as st
import json
import re
import numpy as np
import matplotlib.pyplot as plt

# Import custom tools - Ensure these files are in the same folder
from logic_v2_GitHub import get_gemini_model, load_problems, check_numeric_match, analyze_and_send_report
from render_v2_GitHub import render_problem_diagram, render_lecture_visual

# 1. Page Configuration
st.set_page_config(page_title="FE Exam: Strength of Materials Tutor", layout="wide")

# 2. UI Styling: Matched with Dynamics Tutor with Enhanced Button Fonts
st.markdown("""
    <style>
    /* Global font size increase */
    html, body, [class*="st-"] {
        font-size: 1.1rem;
    }
    
    /* Specific styling for Chat Messages */
    .stChatMessage {
        font-size: 1.1rem !important;
    }

    /* Enhanced Button Styling: 1.2rem Bold */
    div.stButton > button {
        height: 65px; 
        padding: 5px 10px;
        font-size: 1.2rem !important; 
        font-weight: 700 !important; 
        white-space: normal;
        word-wrap: break-word;
        line-height: 1.2;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        transition: all 0.3s ease;
    }

    /* Button Hover Effect */
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* Label font size for sliders and inputs */
    .stSlider label, .stTextArea label {
        font-size: 1.1rem !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Initialize Session State
if "page" not in st.session_state: st.session_state.page = "landing"
if "chat_sessions" not in st.session_state: st.session_state.chat_sessions = {}
if "grading_data" not in st.session_state: st.session_state.grading_data = {}
if "user_name" not in st.session_state: st.session_state.user_name = None
if "lecture_topic" not in st.session_state: st.session_state.lecture_topic = None
if "lecture_session" not in st.session_state: st.session_state.lecture_session = None

# Load Problems from logic module
PROBLEMS = load_problems()

# --- Page 0: Name Entry ---
if st.session_state.user_name is None:
    st.title("🛡️ Engineering Mechanics Portal")
    st.markdown("### Texas A&M University - Corpus Christi")
    with st.form("name_form"):
        name_input = st.text_input("Enter your Full Name to begin")
        if st.form_submit_button("Access Tutor"):
            if name_input.strip():
                st.session_state.user_name = name_input.strip()
                st.rerun()
            else:
                st.warning("Identification is required for academic reporting.")
    st.stop()

# --- Page 1: Main Menu ---
if st.session_state.page == "landing":
    st.title(f"🚀 Welcome, {st.session_state.user_name}!")
    st.info("FE Exam Prep: Strength of Materials | Dr. Dugan Um")
    
    st.markdown("---")
    st.subheader("💡 Interactive Learning Agents")
    col_l1, col_l2, col_l3, col_l4 = st.columns(4)
    lectures = [
        ("Design Properties of Materials", "SM_1"), 
        ("Direct Stress, Deformation, and Design", "SM_2"), 
        ("Torsional Shear Stress and Torsional Deformation", "SM_3"),
        ("Shearing Forces and Bending Moments in Beams", "SM_4"),
        ("Stress Due to Bending", "SM_5"),
        ("Shearing Stresses in Beams", "SM_6"),
        ("Deflection of Beams", "SM_7"),
        ("Combined Load", "SM_8")
    ]
    for i, (name, pref) in enumerate(lectures):
        with [col_l1, col_l2, col_l3, col_l4][i % 4]:
            if st.button(f"🎓 {name}", key=f"lec_{pref}", use_container_width=True):
                st.session_state.lecture_topic = name
                st.session_state.page = "lecture"
                st.session_state.lecture_session = None 
                st.rerun()

    st.markdown("---")
    st.subheader("📝 FE Exam Review Problems")
    categories = {}
    for p in PROBLEMS:
        cat_main = p.get('category', 'General Review').split(":")[0].strip()
        if cat_main not in categories: categories[cat_main] = []
        categories[cat_main].append(p)

    for cat_name, probs in categories.items():
        st.markdown(f"#### {cat_name}")
        for i in range(0, len(probs), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(probs):
                    prob = probs[i + j]
                    sub_label = prob.get("hw_subtitle", prob.get('id', 'Prob'))
                    with cols[j]:
                        if st.button(f"**{sub_label}**\n({prob['id']})", key=f"btn_{prob['id']}", use_container_width=True):
                            st.session_state.current_prob = prob
                            st.session_state.page = "chat"
                            st.rerun()

# --- Page 2: Practice Problem Chat ---
elif st.session_state.page == "chat":
    prob = st.session_state.current_prob
    p_id = prob['id']
    if p_id not in st.session_state.grading_data: st.session_state.grading_data[p_id] = {'solved': set()}
    solved = st.session_state.grading_data[p_id]['solved']
    
    cols = st.columns([2, 1])
    with cols[0]:
        st.subheader(f"📌 {prob['category']}")
        st.info(prob['statement'])
        try:
            st.image(render_problem_diagram(prob), width=400)
        except Exception:
            st.error("Diagram unavailable.")
    
    with cols[1]:
        st.markdown("### 📝 Session Analysis")
        st.write("Work through the derivation with the tutor below.")
        feedback = st.text_area("Notes for Dr. Um:", placeholder="Please provide a feedback to your professor.")
        if st.button("⬅️ Submit Session", use_container_width=True):
            history_text = ""
            if p_id in st.session_state.chat_sessions:
                for msg in st.session_state.chat_sessions[p_id].history:
                    role = "Tutor" if msg.role == "model" else "Student"
                    history_text += f"{role}: {msg.parts[0].text}\n"
            
            with st.spinner("Generating academic report..."):
                report = analyze_and_send_report(st.session_state.user_name, prob['category'], history_text + feedback)
                st.session_state.last_report = report
                st.session_state.page = "report_view"
                st.rerun()

    if p_id not in st.session_state.chat_sessions:
        sys_prompt = f"You are a Strength of Materials Tutor. Problem: {prob['statement']}. Use Socratic method and LaTeX."
        model = get_gemini_model(sys_prompt)
        # Initialize history to prevent double-chat
        st.session_state.chat_sessions[p_id] = model.start_chat(history=[
            {"role": "user", "parts": ["Hi Tutor."]},
            {"role": "model", "parts": ["👋 Ready. Please describe your first step or the governing equations you intend to use."]}
        ])

    for message in st.session_state.chat_sessions[p_id].history:
        if message.parts[0].text == "Hi Tutor.": continue
        with st.chat_message("assistant" if message.role == "model" else "user"):
            st.markdown(message.parts[0].text)

    if user_input := st.chat_input("Your analysis..."):
        for target, val in prob['targets'].items():
            if target not in solved and check_numeric_match(user_input, val):
                st.session_state.grading_data[p_id]['solved'].add(target)
        try:
            st.session_state.chat_sessions[p_id].send_message(user_input)
            st.rerun()
        except Exception:
            st.warning("⚠️ The professor is a little busy right now. Please try again in a minute.")

# --- Page 3: Lecture Simulation & Socratic Discussion ---
elif st.session_state.page == "lecture":
    topic = st.session_state.lecture_topic
    st.title(f"🎓 Lab: {topic}")
    col_sim, col_chat = st.columns([1, 1])
    
    with col_sim:
        params = {}
        if "Stress" in topic or "Properties" in topic:
            p_val = st.slider("Force (kN)", 1, 100, 22)
            a_val = st.slider("Area (mm²)", 100, 1000, 817)
            params = {'P': p_val, 'A': a_val, 'stress': round((p_val * 1000) / a_val, 2)}
        
        st.image(render_lecture_visual(topic, params))
        if 'stress' in params:
            st.metric("Live Calculated Stress (σ)", f"{params['stress']} MPa")

    with col_chat:
        st.subheader("📊 Session Completion")
        lecture_feedback = st.text_area("Notes for Dr. Um:", placeholder="Please provide a feedback to your professor.", key="lec_feedback")
        if st.button("⬅️ Submit Session", use_container_width=True):
            history_text = ""
            if st.session_state.lecture_session:
                for msg in st.session_state.lecture_session.history:
                    role = "Professor" if msg.role == "model" else "Student"
                    history_text += f"{role}: {msg.parts[0].text}\n"
            with st.spinner("Analyzing mastery..."):
                report = analyze_and_send_report(st.session_state.user_name, f"LECTURE: {topic}", history_text + lecture_feedback)
                st.session_state.last_report = report
                st.session_state.page = "report_view"
                st.rerun()
        
        if st.button("🏠 Exit to Menu", use_container_width=True):
            st.session_state.lecture_session = None
            st.session_state.page = "landing"
            st.rerun()

        st.markdown("---")

        st.subheader("💬 Socratic Discussion")
        if st.session_state.lecture_session is None:
            prompts = {"Design Properties of Materials": "Looking at the curve, what happens after the yield point?"}
            initial_question = prompts.get(topic, "How would you describe the relationship shown?")
            sys_msg = f"You are Professor Dugan Um teaching {topic}. Use LaTeX and Socratic method."
            model = get_gemini_model(sys_msg)
            
            # Use history to inject greeting without double-AI call
            initial_history = [
                {"role": "user", "parts": ["Hi Professor."]},
                {"role": "model", "parts": [initial_question]}
            ]
            st.session_state.lecture_session = model.start_chat(history=initial_history)
        
        chat_container = st.container(height=400)
        with chat_container:
            for msg in st.session_state.lecture_session.history:
                if msg.parts[0].text == "Hi Professor.": continue
                clean_text = re.sub(r"\[Live Lab Data:.*?\]", "", msg.parts[0].text).strip()
                if clean_text:
                    with st.chat_message("assistant" if msg.role == "model" else "user"):
                        st.markdown(clean_text)
        
        if lecture_input := st.chat_input("Discuss..."):
            context = f"[Live Lab Data: P={params.get('P', 'N/A')}kN, A={params.get('A', 'N/A')}mm²] "
            try:
                st.session_state.lecture_session.send_message(context + lecture_input)
                st.rerun()
            except Exception:
                st.warning("⚠️ The professor is a little busy right now. Please try again in a minute.")

# --- Page 4: Report View ---
elif st.session_state.page == "report_view":
    st.title("📊 Performance Summary")
    st.markdown(st.session_state.get("last_report", "No report available."))
    if st.button("Return to Main Menu"):
        st.session_state.page = "landing"
        st.rerun()
