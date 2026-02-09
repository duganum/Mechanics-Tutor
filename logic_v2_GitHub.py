import streamlit as st
import google.generativeai as genai
import json
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_gemini_model(system_instruction):
    """Initializes and returns the Gemini 2.0 Flash model."""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(
            model_name='models/gemini-2.0-flash', 
            system_instruction=system_instruction
        )
    except Exception as e:
        st.error(f"Gemini Initialization Failed: {e}")
        return None

def load_problems():
    """Loads the problem list from the JSON file."""
    try:
        # Updated to the new Mechanics-focused filename
        with open('problems.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"problems.json Load Error: {e}")
        return []

def check_numeric_match(user_val, correct_val, tolerance=0.05):
    """Checks if numeric input matches within a 5% tolerance."""
    try:
        u_match = re.search(r"[-+]?\d*\.\d+|\d+", str(user_val))
        if not u_match: return False
        u = float(u_match.group())
        c = float(correct_val)
        if c == 0: return abs(u) < tolerance
        return abs(u - c) <= abs(tolerance * c)
    except (ValueError, TypeError, AttributeError):
        return False

def evaluate_understanding_score(chat_history):
    """
    Evaluates understanding based on Mechanics of Materials concepts.
    Focuses on internal forces, stress formulas, and LaTeX rigor.
    """
    eval_instruction = (
        "You are a strict Engineering Professor at Texas A&M University - Corpus Christi. "
        "Evaluate the student's understanding (0-10) of Strength of Materials based ONLY on chat history.\n\n"
        "STRICT SCORING RUBRIC:\n"
        "0-3: Irrelevant or non-technical participation.\n"
        "4-5: Conceptual understanding present, but lacks governing formulas (e.g., $Mc/I$, $VQ/Ib$, $PL/AE$).\n"
        "6-8: Correctly identifies internal forces (Shear/Moment) and uses proper mechanics equations in LaTeX.\n"
        "9-10: Complete mastery. Flawless application of FE Reference Handbook formulas and sign conventions.\n\n"
        "CRITICAL RULES:\n"
        "1. If the student fails to use governing MECHANICS equations, do NOT exceed 5.\n"
        "2. Penalize sloppy notation (e.g., 'sigma' or 'P/A') instead of LaTeX ($\sigma$, $\\frac{P}{A}$).\n"
        "3. Output ONLY the integer score."
    )
    
    model = get_gemini_model(eval_instruction)
    if not model: return 0

    try:
        response = model.generate_content(f"Chat history to evaluate:\n{chat_history}")
        score_match = re.search(r"\d+", response.text)
        if score_match:
            score = int(score_match.group())
            return min(max(score, 0), 10)
        return 0
    except Exception:
        return 0

def analyze_and_send_report(user_name, topic_title, chat_history):
    """Analyzes the Mechanics session and emails a report to Dr. Um."""
    
    score = evaluate_understanding_score(chat_history)
    
    report_instruction = (
        "You are an academic evaluator for Engineering Mechanics. Analyze this session.\n"
        "Your report must include:\n"
        "1. Session Overview\n"
        f"2. Mechanics Mastery Score: {score}/10\n"
        "3. FE Exam Readiness: Did the student use proper Handbook formulas and LaTeX?\n"
        "4. Strengths/Gaps: (e.g., struggles with Mohr's Circle or Shear Diagrams).\n"
        "5. EXACT student feedback quote."
    )
    
    model = get_gemini_model(report_instruction)
    if not model: return "AI Analysis Unavailable"

    prompt = (
        f"Student: {user_name}\nTopic: {topic_title}\nAssigned Score: {score}/10\n\n"
        f"DATA:\n{chat_history}\n\n"
        "Format for Dr. Dugan Um. Use LaTeX for all math."
    )
    
    try:
        response = model.generate_content(prompt)
        report_text = response.text
    except Exception as e:
        report_text = f"Analysis failed: {str(e)}"

    # Email Logic
    sender = st.secrets["EMAIL_SENDER"]
    password = st.secrets["EMAIL_PASSWORD"] 
    receiver = "dugan.um@gmail.com" 

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = f"Mech. Tutor ({user_name}): {topic_title} [Score: {score}/10]"
    msg.attach(MIMEText(report_text, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
    except Exception:
        pass # Silent fail for email in local testing
    
    return report_text
