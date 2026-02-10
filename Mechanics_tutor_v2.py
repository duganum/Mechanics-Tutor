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
    div.stButton > button {
        height: 65px; 
        font-size: 1.2rem !important; 
        font-weight: 700 !important; 
        transition: all 0.3s ease;
    }
    .stSlider label { font-size: 1.1rem !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. Initialize Session State
if "page" not in st.session_state: st.session_state.page = "landing"
if "user_name" not in st.session_state: st.session_state.user_name = None
if "lecture_topic" not in st.session_state: st.session_state.lecture_topic = None
if "lecture_id" not in st.session_state: st.session_state.lecture_id = None
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
                st.session_state.lecture_id = pref 
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
                    with cols[j]:
                        if st.button(f"**{prob.get('hw_subtitle', 'Prob')}**\n({prob['id']})", key=f"btn_{prob['id']}", use_container_width=True):
                            st.session_state.current_prob = prob
                            st.session_state.page = "chat"
                            st.rerun()

# --- Page 3: Lecture Simulation & Socratic Discussion ---
elif st.session_state.page == "lecture":
    topic = st.session_state.lecture_topic
    lec_id = st.session_state.lecture_id
    st.title(f"🎓 Lab: {topic}")
    
    col_sim, col_chat = st.columns([1, 1])
    
    with col_sim:
        params = {'lec_id': lec_id}
        
        if lec_id in ["SM_4", "SM_5", "SM_6"]:
            p_val = st.slider("Force Magnitude (P) [kN]", 1, 100, 22)
            l_pos = st.slider("Force Location (L_pos)", 0, 1000, 500)
            
            if lec_id == "SM_5":
                s_val = st.slider("Section Modulus (S) [10³ mm³]", 10, 500, 301)
                m_max = p_val * (l_pos/1000) * (1 - l_pos/1000)
                sigma_b = (m_max * 1e6) / (s_val * 1e3)
                params.update({'P': p_val, 'L_pos': l_pos, 'S': s_val, 'sigma_b': sigma_b})
                st.metric("Max Bending Stress (σ)", f"{sigma_b:.2f} MPa")
            else:
                a_val = st.slider("Beam Area (A) [mm²]", 100, 2000, 817)
                params.update({'P': p_val, 'L_pos': l_pos, 'A': a_val})

        else: # SM_1, SM_2, SM_3
            p_val = st.slider("Magnitude / Force (P) [kN]", 1, 100, 22)
            a_val = st.slider("Area / Geometry (A) [mm²]", 100, 2000, 817)
            stress = (p_val * 1000) / a_val
            params.update({'P': p_val, 'A': a_val, 'stress': stress})
            st.metric("Calculated Stress", f"{stress:.2f} MPa")

        st.image(render_lecture_visual(topic, params))

    with col_chat:
        if st.button("🏠 Exit to Menu", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()
        st.subheader("💬 Socratic Discussion")
        if st.session_state.lecture_session is None:
            sys_msg = f"You are Professor Dugan Um teaching {topic}."
            st.session_state.lecture_session = get_gemini_model(sys_msg).start_chat(history=[])
        
        for msg in st.session_state.lecture_session.history:
            with st.chat_message(msg.role):
                st.markdown(msg.parts[0].text)

        if lecture_input := st.chat_input("Discuss the results..."):
            st.session_state.lecture_session.send_message(lecture_input)
            st.rerun()
