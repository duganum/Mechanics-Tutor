# --- Page 3: Lecture Simulation & Discussion Flow Revised ---
elif st.session_state.page == "lecture":
    topic = st.session_state.lecture_topic
    lec_id = st.session_state.lecture_id
    st.title(f"🎓 Lab: {topic}")
    
    col_sim, col_side = st.columns([1, 1])
    
    # Left Column: Simulation Parameters and Visuals
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
        else:
            p_val = st.slider("Magnitude / Force (P) [kN]", 1, 100, 22)
            a_val = st.slider("Area / Geometry (A) [mm²]", 100, 2000, 817)
            stress = (p_val * 1000) / a_val
            params.update({'P': p_val, 'A': a_val, 'stress': stress})
            st.metric("Calculated Stress", f"{stress:.2f} MPa")

        st.image(render_lecture_visual(topic, params))

    # Right Column: Socratic Discussion (Switched to side)
    with col_side:
        if st.button("🏠 Exit to Menu", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

        st.subheader("💬 Socratic Discussion")
        
        if st.session_state.lecture_session is None:
            sys_msg = f"You are Professor Dugan Um teaching {topic} (ID: {lec_id})."
            initial_greeting = f"Welcome to the lab on {topic}. I have initialized the simulation. What observations can you make from the current data?"
            st.session_state.lecture_session = get_gemini_model(sys_msg).start_chat(history=[
                {"role": "model", "parts": [initial_greeting]}
            ])
        
        # Chat container for history in side column
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

    # Bottom Full Width: Session Analysis (Switched to bottom)
    st.markdown("---")
    st.subheader("📝 Session Analysis")
    st.info("Work through the derivation with the tutor above. Focus on using correct LaTeX notation and physical principles.")
    
    user_feedback = st.text_area("Notes for Dr. Um:", placeholder="Please provide feedback to your professor...", height=150)
    
    if st.button("⬅️ Submit Session", use_container_width=True):
        if st.session_state.lecture_session:
            history_text = "\n".join([f"{m.role}: {m.parts[0].text}" for m in st.session_state.lecture_session.history])
            full_history_with_feedback = f"{history_text}\n\n--- STUDENT FEEDBACK ---\n{user_feedback}"
            
            with st.spinner("Analyzing session and sending report..."):
                try:
                    report = analyze_and_send_report(
                        user_name=str(st.session_state.user_name),
                        topic_title=str(topic),
                        chat_history=full_history_with_feedback
                    )
                    st.success("Session Analysis complete and emailed to Dr. Um!")
                    st.session_state.page = "landing"
                    st.rerun()
                except Exception as e:
                    st.error(f"Submission Error: {e}")
