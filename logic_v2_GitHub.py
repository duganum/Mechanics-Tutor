import json
import re
import google.generativeai as genai
import streamlit as st

# --- 1. AI Configuration ---
def get_gemini_model(sys_prompt):
    """
    Initializes the Gemini model with a specific system instruction.
    Uses st.secrets for the API key to ensure security on Streamlit Cloud.
    """
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=sys_prompt
    )
    return model

# --- 2. Data Loading ---
def load_problems():
    """
    Loads the FE Exam problems from the local JSON file.
    This function is defined here but called by the Main app.
    """
    try:
        # Ensure the filename matches your actual JSON file name
        with open('problems_v2.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback if file is missing
        return []
    except Exception as e:
        print(f"Error loading problems: {e}")
        return []

# --- 3. Numeric Evaluation Logic ---
def check_numeric_match(user_input, target_val, tolerance=0.05):
    """
    Extracts numbers from student input and compares them to the target.
    Allows for a 5% margin of error for rounding.
    """
    # Find all numbers (including decimals) in the user's string
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", user_input)
    if not numbers:
        return False
    
    try:
        # Check the last number mentioned against the target
        last_num = float(numbers[-1])
        target = float(target_val)
        
        # Calculate percent difference
        diff = abs(last_num - target) / abs(target) if target != 0 else abs(last_num)
        return diff <= tolerance
    except:
        return False

# --- 4. Reporting Logic ---
def analyze_and_send_report(user_name, category, history):
    """
    Summarizes the session performance. 
    In a full production version, this could send an email or save to a DB.
    """
    report = f"### 📊 Session Report for {user_name}\n"
    report += f"**Topic:** {category}\n\n"
    
    # Simple logic to determine if they struggled or succeeded
    if "I don't know" in history or "help" in history:
        report += "📝 **Observation:** Student requested significant guidance on this topic."
    else:
        report += "✅ **Observation:** Student demonstrated strong independent derivation."
    
    return report

# --- IMPORTANT: DO NOT CALL FUNCTIONS OR DEFINE VARIABLES HERE ---
# No "PROBLEMS = load_problems()" here. 
# The Main app (Mechanics_tutor_v2.py) will handle those calls.
