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

# 2. UI Styling
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 1.1rem; }
    .stChatMessage { font-size: 1.1rem !important; }
    div.stButton > button {
        height: 65px; 
        padding: 5px 10px;
        font-size: 1.2rem !important; 
        font-weight: 700 !important; 
        transition: all 0.3s ease;
    }
    .stSlider label { font-size: 1.1rem !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. Initialize Session State
if "page" not in st.session_state: st.session_state.page = "landing"
if "chat_sessions" not in st.session_state: st.session_state.chat_sessions = {}
if "grading_data" not in st.session_state: st.session_state.grading_data = {}
if "user_name" not in st.session_state: st.session_state.user_name = None
if "lecture_topic" not in st.session_state: st.session_state.lecture_topic = None
if "lecture_session" not in st.session_state: st.session_state.lecture_session = None

PROBLEMS = load_problems()

# --- Page 0: Name Entry ---
if st.session_state.user_name is None:
    st.title("🛡️ Engineering Mechanics Portal")
    with st.form("name_form"):
        name_input = st.text_input("Enter your Full Name to begin")
        if st.form_submit_button("Access Tutor"):
            if name_input.strip():
                st.session_state.user_name = name_input.strip()
                st.rerun()
    st.stop()

# --- Page 1: Main Menu ---
if st.session_state.page == "landing":
    st.title(f"🚀 Welcome, {st.session_state.user_name}!")
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

# --- Page 2: Practice Problem Chat (Existing Logic) ---
elif st.session_state.page == "chat":
    # ... (Rest of existing practice problem code)
    pass

# --- Page 3: Lecture Simulation & Socratic Discussion ---
elif st.session_state.page == "lecture":
    topic = st.session_state.lecture_topic
    st.title(f"🎓 Lab: {topic}")
    col_sim, col_chat = st.columns([1, 1])
    
    with col_sim:
        params = {}
        # Specialized Sliders for Beam Bending Labs
        if "Shearing Forces" in topic or "Beams" in topic or "Bending" in topic:
            # Slider 1: Magnitude
            p_val = st.slider("Force Magnitude (P) [kN]", 1, 100, 22) 
            # Slider 2: Location
            l_pos = st.slider("Force Location (L_pos)", 0, 1000, 500) 
            # Slider 3: Section Modulus
            s_val = st.slider("Section Modulus (S) [10³ mm³]", 10, 500, 150)
            
            # Physics Calculations
            pos_ratio = l_pos / 1000
            m_max_kNm = p_val * pos_ratio * (1 - pos_ratio)
            # sigma = M/S (Convert kNm to N-mm and S to mm^3)
            bending_stress = (m_max_kNm * 1e6) / (s_val * 1e3) 
            
            params = {'P': p_val, 'L_pos': l_pos, 'S': s_val, 'sigma_b': bending_stress}
            
            # Live Metrics
            st.metric("Max Bending Moment", f"{m_max_kNm:.2f} kNm")
            st.metric("Max Bending Stress (σ)", f"{bending_stress:.2f} MPa")

        elif "Torsional" in topic:
            p_val = st.slider("Torque (T) [kN-m]", 1, 100, 22)
            a_val = st.slider("Shaft Area (A) [mm²]", 100, 1000, 817)
            params = {'P': p_val, 'A': a_val}

        elif "Stress" in topic or "Properties" in topic:
            p_val = st.slider("Force (P) [kN]", 1, 100, 22)
            a_val = st.slider("Area (A) [mm²]", 100, 1000, 817)
            params = {'P': p_val, 'A': a_val, 'stress': round((p_val * 1000) / a_val, 2)}
            st.metric("Live Calculated Stress (σ)", f"{params['stress']} MPa")

        # Render the visual
        st.image(render_lecture_visual(topic, params))

    with col_chat:
        st.subheader("💬 Socratic Discussion")
        if st.session_state.lecture_session is None:
            sys_msg = f"You are Professor Dugan Um teaching {topic}. Use LaTeX and Socratic method."
            st.session_state.lecture_session = get_gemini_model(sys_msg).start_chat(history=[
                {"role": "user", "parts": ["Hi Professor."]},
                {"role": "model", "parts": ["How would you describe the relationship shown?"]}
            ])
        
        for msg in st.session_state.lecture_session.history:
            if msg.parts[0].text == "Hi Professor.": continue
            with st.chat_message("assistant" if msg.role == "model" else "user"):
                st.markdown(re.sub(r"\[Live Lab Data:.*?\]", "", msg.parts[0].text).strip())

        if lecture_input := st.chat_input("Discuss..."):
            context = f"[Live Lab Data: P={params.get('P')}, Loc={params.get('L_pos')}] "
            st.session_state.lecture_session.send_message(context + lecture_input)
            st.rerun()

# --- Page 4: Report View ---
elif st.session_state.page == "report_view":
    st.title("📊 Performance Summary")
    if st.button("Return to Main Menu"):
        st.session_state.page = "landing"
        st.rerun()
