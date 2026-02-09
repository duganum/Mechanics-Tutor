import matplotlib.pyplot as plt
import numpy as np
import io

def render_problem_diagram(prob):
    """
    Renders a standard diagram for FE Review practice problems.
    This ensures the 'chat' page doesn't crash.
    """
    fig, ax = plt.subplots(figsize=(5, 3))
    
    # Generic placeholder logic based on problem data
    p_id = prob.get('id', 'N/A')
    category = prob.get('category', 'Engineering Mechanics')
    
    ax.text(0.5, 0.6, f"Problem: {p_id}", ha='center', fontsize=12, fontweight='bold')
    ax.text(0.5, 0.4, f"Topic: {category}", ha='center', fontsize=10, style='italic')
    
    # Simple border
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    rect = plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, color='gray', ls='--')
    ax.add_patch(rect)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf

def render_lecture_visual(topic, params):
    """
    The main simulation renderer. 
    It uses 'params' passed from the slider in the main app.
    """
    plt.style.use('fast')
    fig, ax = plt.subplots(figsize=(7, 4))
    
    # --- Topic 1 & 2: Direct Stress Simulation ---
    if "Direct Stress" in topic or "Properties" in topic:
        # 1. Specimen Block
        rect = plt.Rectangle((0.2, 0.3), 0.5, 0.4, linewidth=2, edgecolor='#2c3e50', facecolor='#d3d3d3')
        ax.add_patch(rect)
        
        # 2. Extract live slider data
        p_val = params.get('P', 'P')
        a_val = params.get('A', 'A')
        stress_val = params.get('stress', 'P/A')

        # 3. Dynamic Tension Arrow
        ax.annotate('', xy=(0.85, 0.5), xytext=(0.7, 0.5),
                    arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=4))
        
        # 4. Text Overlay: LaTeX Math
        display_text = f"$\\sigma = P/A$\n\n$\\sigma = {stress_val}$ MPa"
        ax.text(0.45, 0.5, display_text, fontsize=16, ha='center', va='center', fontweight='bold')
        
        # 5. Metadata
        ax.text(0.85, 0.55, f"P = {p_val} kN", color='#e74c3c', fontweight='bold')
        ax.text(0.45, 0.22, f"Area (A) = {a_val} $mm^2$", ha='center', fontsize=11)

        ax.set_xlim(0, 1.1)
        ax.set_ylim(0, 1)
        ax.axis('off')

    # --- Topic 3: Torsional Shear ---
    elif "Torsional" in topic:
        circle = plt.Circle((0.5, 0.5), 0.35, color='#ecf0f1', ec='#2c3e50', lw=3)
        ax.add_patch(circle)
        ax.plot([0.5, 0.5], [0.5, 0.85], color='#2c3e50', ls='--') 
        
        ax.scatter([0.5], [0.5], color='#c0392b', s=80, zorder=5)
        ax.text(0.5, 0.42, "Neutral Axis\n$\\tau=0$", ha='center', fontsize=10)

        # Torque Arrow
        ax.annotate('', xy=(0.8, 0.7), xytext=(0.7, 0.85),
                    arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.5", lw=3, color='#3498db'))
        ax.text(0.8, 0.85, "Torque (T)", color='#3498db', fontweight='bold')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

    # --- Fallback ---
    else:
        ax.text(0.5, 0.5, f"Diagram for:\n{topic}", ha='center', va='center', fontsize=12)
        ax.axis('off')

    plt.tight_layout()
    buf = io.BytesIO()
    # DPI 120 keeps the image crisp on Streamlit
    plt.savefig(buf, format='png', dpi=120)
    plt.close(fig)
    buf.seek(0)
    return buf
