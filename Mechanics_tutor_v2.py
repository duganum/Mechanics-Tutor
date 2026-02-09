import streamlit as st
import json
import re
import numpy as np
import matplotlib.pyplot as plt

from logic_v2_GitHub import get_gemini_model, load_problems, check_numeric_match, analyze_and_send_report
from render_v2_GitHub import render_problem_diagram, render_lecture_visual
