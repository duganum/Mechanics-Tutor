import json
import re
import google.generativeai as genai
import streamlit as st

def get_gemini_model(sys_prompt):
    """Initializes the AI model using Streamlit secrets."""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=sys_prompt
        )
        return model
    except Exception as e:
        st.error(f"AI Configuration Error: {e}")
        return None

def load_problems():
    """Loads problem data from JSON."""
    try:
        with open('problems_v2.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception:
        return []

def check_numeric_match(user_input, target_val, tolerance=0.05):
    """Compares student answer to target with a 5% tolerance."""
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", user_input)
    if not numbers:
        return False
    try:
        user_num = float(numbers[-1])
        target = float(target_val)
        if target == 0: return abs(user_num) < tolerance
        return abs(user_num - target) / abs(target) <= tolerance
    except:
        return False

def analyze_and_send_report(user_name, category, history):
    """Generates a basic session summary."""
    return f"### 📊 Report for {user_name}\n**Topic:** {category}\nSession completed successfully."
