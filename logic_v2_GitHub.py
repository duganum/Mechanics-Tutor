with col_chat:
    st.subheader("💬 Socratic Discussion")
    
    # 1. Define topic-specific leading questions
    prompts = {
        "Design Properties of Materials": "Looking at the curve, what happens to the stress-strain relationship after the strain reaches $\epsilon = 0.1$?",
        "Direct Stress, Deformation, and Design": "If we double the area $A$ but keep load $P$ constant, how does the stress change?",
        "Combined Load": "What physical scenario causes Mohr's Circle to intersect the horizontal axis?"
    }
    initial_question = prompts.get(topic, "How would you describe the relationship shown here?")

    # 2. Display the leading question as a static instruction box (not a chat bubble)
    st.info(f"**Professor's Challenge:** {initial_question}")

    # 3. Initialize the session ONLY once without sending an initial message
    if "lecture_session" not in st.session_state or st.session_state.lecture_session is None:
        sys_msg = (
            f"You are a Professor at TAMUCC teaching {topic}. "
            "STRICT RULES: 1. You are a Socratic tutor. 2. Do NOT answer questions yourself. "
            "3. Wait for the student to provide an analysis. 4. Use LaTeX for math. "
            f"The student is currently responding to this prompt: {initial_question}"
        )
        model = get_gemini_model(sys_msg)
        st.session_state.lecture_session = model.start_chat(history=[])

    # 4. Display ONLY actual chat history
    for msg in st.session_state.lecture_session.history:
        with st.chat_message("assistant" if msg.role == "model" else "user"):
            st.markdown(msg.parts[0].text)

    # 5. Handle student input
    if lecture_input := st.chat_input("Discuss the mechanics..."):
        # The AI now only speaks AFTER this input is sent
        st.session_state.lecture_session.send_message(lecture_input)
        st.rerun()
