import matplotlib.pyplot as plt
import numpy as np
import io

def render_problem_diagram(prob):
    """Renders a simple placeholder for practice problems."""
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.text(0.5, 0.5, f"Problem: {prob.get('id', 'FE Exam')}", ha='center', va='center', fontsize=12)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf

def render_lecture_visual(topic, params):
    """Renders the interactive lab simulation."""
    plt.style.use('fast')
    fig, ax = plt.subplots(figsize=(7, 4))
    
    if "Direct Stress" in topic or "Properties" in topic:
        # Specimen Block
        rect = plt.Rectangle((0.2, 0.3), 0.5, 0.4, linewidth=2, edgecolor='black', facecolor='#d3d3d3')
        ax.add_patch(rect)
        
        # Get live data
        p_val = params.get('P', 0)
        a_val = params.get('A', 0)
        stress_val = params.get('stress', 'P/A')

        # Stress Arrow
        ax.annotate('', xy=(0.85, 0.5), xytext=(0.7, 0.5),
                    arrowprops=dict(arrowstyle='->', color='red', lw=3))
        
        # Math Text
        display_text = f"$\\sigma = P/A$\n\n$\\sigma = {stress_val}$ MPa"
        ax.text(0.45, 0.5, display_text, fontsize=16, ha='center', va='center', fontweight='bold')
        
        # Labels
        ax.text(0.85, 0.55, f"P = {p_val} kN", color='red')
        ax.text(0.45, 0.22, f"A = {a_val} $mm^2$", ha='center')

    elif "Torsional" in topic:
        circle = plt.Circle((0.5, 0.5), 0.35, color='#ecf0f1', ec='black', lw=2)
        ax.add_patch(circle)
        ax.set_title("Shaft Cross-Section")
    else:
        ax.text(0.5, 0.5, f"Lab: {topic}", ha='center')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf
