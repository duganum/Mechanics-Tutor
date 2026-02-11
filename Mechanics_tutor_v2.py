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
    
    # Filter for specifically the 3 generated problems for Chapter 1
    # SM_1_2: Axial Elongation | SM_1_3: Thermal Stress | SM_1_4: Poisson's Ratio
    chapter_1_ids = ["SM_1_2", "SM_1_3", "SM_1_4"]
    ch1_probs = [p for p in PROBLEMS if p['id'] in chapter_1_ids]
    
    st.markdown("#### Design Properties of Materials")
    cols = st.columns(3)
    for idx, prob in enumerate(ch1_probs):
        with cols[idx]:
            if st.button(f"**{prob.get('hw_subtitle', 'FE Prob')}**\n({prob['id']})", key=f"btn_{prob['id']}", use_container_width=True):
                # Redirect to 'lecture' mode to ensure Socratic Discussion is available
                st.session_state.lecture_topic = f"Problem {prob['id']}: {prob['hw_subtitle']}"
                st.session_state.lecture_id = prob['id']
                st.session_state.current_prob = prob # Store problem context
                st.session_state.page = "lecture"
                st.session_state.lecture_session = None
                st.rerun()

# --- Page 3: Full Socratic Lecture & Problem Flow ---
elif st.session_state.page == "lecture":
    topic = st.session_state.lecture_topic
    lec_id = st.session_state.lecture_id
    st.title(f"🎓 Lab/Problem: {topic}")
    
    col_sim, col_side = st.columns([1, 1])
    
    with col_sim:
        params = {'lec_id': lec_id}
        
        # Check if we are in one of the 3 specific FE problems
        if lec_id in ["SM_1_2", "SM_1_3", "SM_1_4"]:
            st.info(st.session_state.current_prob['statement'])
            # Render a generic diagram for these problems
            st.image(render_problem_diagram(st.session_state.current_prob))
        
        # Standard Simulation Logic for Lecture IDs
        elif lec_id in ["SM_4", "SM_5", "SM_6", "SM_7"]:
            p_val = st.slider("Force Magnitude (P) [kN]", 1, 100, 22)
            l_pos = st.slider("Force Location (L_pos)", 0, 1000, 500)
            if lec_id == "SM_5":
                s_val = st.slider("Section Modulus (S) [10³ mm³]", 10, 500, 301)
                m_max = p_val * (l_pos/1000) * (1 - l_pos/1000)
                sigma_b = (m_max * 1e6) / (s_val * 1e3)
                params.update({'P': p_val, 'L_pos': l_pos, 'S': s_val, 'sigma_b': sigma_b})
                st.metric("Max Bending Stress (σ)", f"{sigma_b:.2f} MPa")
            else:
                params.update({'P': p_val, 'L_pos': l_pos})
                st.metric("Applied Load (P)", f"{p_val} kN")
            st.image(render_lecture_visual(topic, params))

        elif lec_id == "SM_8":
            sig_x = st.slider("Normal Stress (σx) [MPa]", -500, 500, 100)
            sig_y = st.slider("Normal Stress (σy) [MPa]", -500, 500, 50)
            tau_xy = st.slider("Shear Stress (τxy) [MPa] (CCW is '-')", -100, 100, 40)
            center = (sig_x + sig_y) / 2
            radius = np.sqrt(((sig_x - sig_y)/2)**2 + tau_xy**2)
            params.update({'P': sig_x, 'sigma_y': sig_y, 'tau_val': tau_xy}) 
            m1, m2, m3 = st.columns(3)
            m1.metric("Principal σ₁", f"{(center+radius):.1f} MPa")
            m2.metric("Principal σ₂", f"{(center-radius):.1f} MPa")
            m3.metric("Max Shear τ", f"{radius:.1f} MPa")
            st.image(render_lecture_visual(topic, params))

        else:
            # Fallback for SM_1, SM_2, SM_3
            p_val = st.slider("Magnitude / Force (P) [kN]", 1, 100, 22)
            a_val = st.slider("Area / Geometry (A) [mm²]", 100, 2000, 817)
            stress = (p_val * 1000) / a_val
            params.update({'P': p_val, 'A': a_val, 'stress': stress})
            st.metric("Calculated Stress", f"{stress:.2f} MPa")
            st.image(render_lecture_visual(topic, params))

    with col_side:
        st.subheader("💬 Socratic Discussion")
        if st.session_state.lecture_session is None:
            sys_msg = f"You are Professor Dugan Um. Guide the student through: {topic}."
            initial_greeting = f"Hello! Let's analyze {topic}. Based on the parameters provided, how would you start the derivation?"
            st.session_state.lecture_session = get_gemini_model(sys_msg).start_chat(history=[
                {"role": "model", "parts": [initial_greeting]}
            ])
        
        chat_container = st.container(height=450)
        with chat_container:
            for msg in st.session_state.lecture_session.history:
                with st.chat_message("assistant" if msg.role == "model" else "user"):
                    st.markdown(msg.parts[0].text)

        with st.form("lecture_chat_form", clear_on_submit=True):
            lecture_input = st.text_input("Discuss results...", placeholder="Type here...")
            if st.form_submit_button("Submit Message") and lecture_input:
                st.session_state.lecture_session.send_message(lecture_input)
                st.rerun()

    st.markdown("---")
    st.subheader("📝 Session Analysis")
    st.info("Ensure you have discussed the physical principles before submitting.")
    user_feedback = st.text_area("Notes for Dr. Um:", placeholder="Provide feedback...", height=150)
    
    col_submit, col_exit = st.columns(2)
    with col_submit:
        if st.button("⬅️ Submit Session", use_container_width=True):
            if st.session_state.lecture_session:
                history_text = "\n".join([f"{m.role}: {m.parts[0].text}" for m in st.session_state.lecture_session.history])
                full_history = f"{history_text}\n\n--- STUDENT FEEDBACK ---\n{user_feedback}"
                with st.spinner("Analyzing..."):
                    try:
                        analyze_and_send_report(
                            user_name=str(st.session_state.user_name),
                            topic_title=str(topic),
                            chat_history=full_history
                        )
                        st.success("Analysis emailed to Dr. Um!")
                        st.session_state.page = "landing"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

    with col_exit:
        if st.button("🏠 Exit to Menu", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()
