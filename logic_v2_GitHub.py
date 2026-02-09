import streamlit as st
import json
import re
import numpy as np
import matplotlib.pyplot as plt
from logic_v2_GitHub import get_gemini_model, load_problems, check_numeric_match, analyze_and_send_report
from render_v2_GitHub import render_problem_diagram, render_lecture_visual

# 1. Page Configuration
st.set_page_config(page_title="FE Exam: Strength of Materials Tutor", layout="wide")

# 2. CSS for UI consistency and button sizing
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

# Load problems from the specific GitHub JSON file
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
    
    # Section A: Interactive Lectures (Revised Syllabus Order)
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
                # Reset lecture session to ensure fresh start
                st.session_state.lecture_session = None
                st.rerun()

    # Section B: Practice Problems
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

# --- Page 2: Problem Chat ---
elif st.session_state.page == "chat":
    prob = st.session_state.current_prob
    p_id = prob['id']
    if p_id not in st.session_state.grading_data: st.session_state.grading_data[p_id] = {'solved': set()}
    solved = st.session_state.grading_data[p_id]['solved']
    
    cols = st.columns([2, 1])
    with cols[0]:
        st.subheader(f"📌 {prob['category']}")
        st.info(prob['statement'])
        st.image(render_problem_diagram(prob), width=400)
    
    with cols[1]:
        st.metric("Variables Found", f"{len(solved)} / {len(prob['targets'])}")
        st.progress(len(solved) / len(prob['targets']) if len(prob['targets']) > 0 else 0)
        feedback = st.text_area("Notes for Dr. Um:", placeholder="Hardest part?")
        if st.button("⬅️ Submit Session", use_container_width=True):
            history_text = ""
            if p_id in st.session_state.chat_sessions:
                for msg in st.session_state.chat_sessions[p_id].history:
                    role = "Tutor" if msg.role == "model" else "Student"
                    history_text += f"{role}: {msg.parts[0].text}\n"
            report = analyze_and_send_report(st.session_state.user_name, prob['category'], history_text + feedback)
            st.session_state.last_report = report
            st.session_state.page = "report_view"; st.rerun()

    if p_id not in st.session_state.chat_sessions:
        sys_prompt = f"You are a Socratic Tutor for Strength of Materials. Use LaTeX. Do NOT solve the problem for the student."
        model = get_gemini_model(sys_prompt)
        st.session_state.chat_sessions[p_id] = model.start_chat(history=[])

    for message in st.session_state.chat_sessions[p_id].history:
        with st.chat_message("assistant" if message.role == "model" else "user"):
            st.markdown(message.parts[0].text)

    if user_input := st.chat_input("Analyze..."):
        for target, val in prob['targets'].items():
            if target not in solved and check_numeric_match(user_input, val):
                st.session_state.grading_data[p_id]['solved'].add(target)
        st.session_state.chat_sessions[p_id].send_message(user_input); st.rerun()

# --- Page 3: Interactive Lecture ---
elif st.session_state.page == "lecture":
    topic = st.session_state.lecture_topic
    st.title(f"🎓 Lab: {topic}")
    col_sim, col_chat = st.columns([1, 1])
    
    with col_sim:
        params = {}
        if "Properties" in topic or "Direct" in topic:
            params['P'] = st.slider("Force (kN)", 1, 100, 50)
            params['A'] = st.slider("Area (mm²)", 100, 1000, 500)
        st.image(render_lecture_visual(topic, params))
        if st.button("🏠 Exit to Menu", use_container_width=True):
            st.session_state.lecture_session = None; st.session_state.page = "landing"; st.rerun()

    with col_chat:
        st.subheader("💬 Socratic Discussion")
        
        # 1. Define topic-specific leading questions
        prompts = {
            "Design Properties of Materials": "Looking at the curve, what happens to the stress-strain relationship after the strain reaches $\epsilon = 0.1$?",
            "Direct Stress, Deformation, and Design": "If the load $P$ is constant but we double the area $A$, how does the internal stress change?",
            "Torsional Shear Stress and Torsional Deformation": "Why is the shear stress $\tau$ always zero at the neutral axis of a circular shaft?",
            "Combined Load": "What physical scenario causes Mohr's Circle to intersect the horizontal stress axis?"
        }
        initial_question = prompts.get(topic, "How would you define the physical relationship shown here?")

        # 2. Display the Challenge as a static INFO box (NOT a chat turn)
        st.info(f"**Professor's Challenge:** {initial_question}")

        # 3. Initialize the AI with STRICT instructions to wait
        if "lecture_session" not in st.session_state or st.session_state.lecture_session is None:
            sys_msg = (
                f"You are a Professor at TAMUCC teaching {topic}. "
                "STRICT RULES: 1. You are a Socratic tutor. 2. NEVER answer your own questions. "
                "3. Wait for the student's FIRST input. 4. Use LaTeX for math. "
                f"The student is responding to this prompt: {initial_question}. "
                "Do NOT repeat the prompt. Silently wait for the student to start the analysis."
            )
            model = get_gemini_model(sys_msg)
            st.session_state.lecture_session = model.start_chat(history=[])

        # 4. Display ONLY actual conversation history (starts empty)
        for msg in st.session_state.lecture_session.history:
            with st.chat_message("assistant" if msg.role == "model" else "user"):
                st.markdown(msg.parts[0].text)

        # 5. Conversations only begin here
        if lecture_input := st.chat_input("Discuss the mechanics..."):
            st.session_state.lecture_session.send_message(lecture_input)
            st.rerun()

# --- Page 4: Report View ---
elif st.session_state.page == "report_view":
    st.title("📊 Performance Summary")
    st.markdown(st.session_state.get("last_report", "No report available."))
    if st.button("Return to Main Menu"):
        st.session_state.page = "landing"; st.rerun()
