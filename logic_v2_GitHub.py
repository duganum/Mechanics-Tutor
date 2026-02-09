import streamlit as st
import google.generativeai as genai
import json
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_gemini_model(system_instruction):
    """Initializes the Gemini 2.0 Flash model using the faculty API key."""
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
    """Loads the FE Exam problem set from the specific GitHub JSON file."""
    try:
        # Explicitly targeting the filename shown in your repository
        with open('problems_v2_GitHub.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"problems_v2_GitHub.json Load Error: {e}")
        return []

def check_numeric_match(user_val, correct_val, tolerance=0.05):
    """Extracts numbers and checks if the student's answer is within 5%."""
    try:
        u_match = re.search(r"[-+]?\d*\.\d+|\d+", str(user_val))
        if not u_match: return False
        u = float(u_match.group())
        c = float(correct_val)
        if c == 0: return abs(u) < tolerance
        return abs(u - c) <= abs(tolerance * c)
    except:
        return False

def evaluate_understanding_score(chat_history):
    """Strict evaluation of mechanics mastery using LaTeX and Handbook formulas."""
    eval_instruction = (
        "You are a strict Engineering Professor. Evaluate the student (0-10).\n"
        "STRICT RULE: If the student did not derive or use specific governing equations "
        "like $Mc/I$ or $PL/AE$ in LaTeX, do NOT exceed a score of 5.\n"
        "Output ONLY the integer."
    )
    model = get_gemini_model(eval_instruction)
    if not model: return 0
    try:
        response = model.generate_content(f"History:\n{chat_history}")
        score_match = re.search(r"\d+", response.text)
        return int(score_match.group()) if score_match else 0
    except:
        return 0

def analyze_and_send_report(user_name, topic_title, chat_history):
    """Generates a pedagogical report and emails it to Dr. Dugan Um."""
    score = evaluate_understanding_score(chat_history)
    report_instruction = f"Academic report for Dr. Dugan Um. Score: {score}/10. Use LaTeX."
    model = get_gemini_model(report_instruction)
    if not model: return "AI Analysis Unavailable"
    try:
        report_text = model.generate_content(chat_history).text
        sender = st.secrets["EMAIL_SENDER"]
        receiver = "dugan.um@gmail.com" 
        msg = MIMEMultipart()
        msg['From'], msg['To'] = sender, receiver
        msg['Subject'] = f"Mech Tutor: {user_name} - {topic_title} [{score}/10]"
        msg.attach(MIMEText(report_text, 'plain'))
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender, st.secrets["EMAIL_PASSWORD"])
        server.send_message(msg)
        server.quit()
        return report_text
    except:
        return "Report Generated (Email delivery skipped)."
