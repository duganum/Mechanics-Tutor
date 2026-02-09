import streamlit as st
import json
import re
import numpy as np
import matplotlib.pyplot as plt
# FIXED: Added logic imports to prevent "load_problems not defined"

# 1. Page Configuration
st.set_page_config(page_title="FE Exam: Strength of Materials Tutor", layout="wide")

# 2. CSS for UI consistency
st.markdown("""
    <style>
    div.stButton > button {
        height: 60px;
        padding: 5px 10px;
        font-size: 14px;
        white-space: normal;
        word-wrap: break-word;
        line-height: 1.2;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
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

# Load problems
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

# --- Page 2: Problem Chat (Omitted for brevity, logic remains same) ---
elif st.session_state.page == "chat":
    # (Same logic as your original chat page)
    pass

# --- Page 3: Interactive Lecture (REVISED) ---
elif st.session_state.page == "lecture":
    topic = st.session_state.lecture_topic
    st.title(f"🎓 Lab: {topic}")
    col_sim, col_chat = st.columns([1, 1])
    
    with col_sim:
        params = {}
        if "Stress" in topic or "Properties" in topic:
            p_val = st.slider("Force (kN)", 1, 100, 22)
            a_val = st.slider("Area (mm²)", 100, 1000, 817)
            # Calculate stress: MPa = N/mm^2 = (kN * 1000) / mm^2
            params = {'P': p_val, 'A': a_val, 'stress': round((p_val * 1000) / a_val, 2)}
        
        st.image(render_lecture_visual(topic, params))
        
        if 'stress' in params:
            st.metric("Current Stress (σ)", f"{params['stress']} MPa")
        
        if st.button("🏠 Exit to Menu", use_container_width=True):
            st.session_state.lecture_session = None
            st.session_state.page = "landing"
            st.rerun()

    with col_chat:
        st.subheader("💬 Socratic Discussion")
        
        prompts = {
            "Design Properties of Materials": "Looking at the curve, what happens to the stress-strain relationship after the strain reaches $\epsilon = 0.1$?",
            "Direct Stress, Deformation, and Design": "If the load $P$ is constant but we double the area $A$, how does the internal stress change?",
            "Torsional Shear Stress and Torsional Deformation": "Why is the shear stress $\tau$ always zero at the neutral axis of a circular shaft?",
            "Combined Load": "What physical scenario causes Mohr's Circle to intersect the horizontal stress axis?"
        }
        initial_question = prompts.get(topic, "How would you define the physical relationship shown here?")
        st.info(f"**Professor's Challenge:** {initial_question}")

        if st.session_state.lecture_session is None:
            sys_msg = (f"You are Dr. Dugan Um, a Professor at TAMUCC teaching {topic}. "
                       "Use LaTeX and Socratic methods. You will receive live slider data in brackets. "
                       "Verify student math and guide them based on those specific numbers.")
            model = get_gemini_model(sys_msg)
            st.session_state.lecture_session = model.start_chat(history=[])

        for msg in st.session_state.lecture_session.history:
            # Clean technical data from student view
            clean_text = re.sub(r"\[Live Lab Data:.*?\]", "", msg.parts[0].text).strip()
            if clean_text:
                with st.chat_message("assistant" if msg.role == "model" else "user"):
                    st.markdown(clean_text)

        if lecture_input := st.chat_input("Analyze..."):
            # Inject live data so AI sees the same stress as the student
            context = f"[Live Lab Data: P={params.get('P')}kN, A={params.get('A')}mm², Stress={params.get('stress')}MPa] "
            st.session_state.lecture_session.send_message(context + lecture_input)
            st.rerun()

# --- Page 4: Report View ---
elif st.session_state.page == "report_view":
    st.title("📊 Performance Summary")
    st.markdown(st.session_state.get("last_report", "No report available."))
    if st.button("Return to Main Menu"):
        st.session_state.page = "landing"; st.rerun()


