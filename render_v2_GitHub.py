import matplotlib.pyplot as plt
import numpy as np
import io

def render_problem_diagram(prob):
    """
    Renders a standard placeholder or logic-based diagram for FE Review problems.
    """
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.text(0.5, 0.5, f"Problem ID: {prob.get('id', 'N/A')}\n{prob.get('category', 'Statics')}", 
            ha='center', va='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf

def render_lecture_visual(topic, params):
    """
    Renders dynamic engineering diagrams based on the lecture topic and slider parameters.
    Returns a BytesIO buffer containing the PNG image.
    """
    plt.style.use('fast')
    fig, ax = plt.subplots(figsize=(7, 4))
    
    # Topic 1 & 2: Direct Stress / Design Properties
    if "Direct Stress" in topic or "Properties" in topic:
        # Create specimen block (The "Box" in your simulation)
        rect = plt.Rectangle((0.2, 0.3), 0.5, 0.4, linewidth=2, edgecolor='black', facecolor='#d3d3d3')
        ax.add_patch(rect)
        
        # Pull live values
        p_val = params.get('P', 0)
        a_val = params.get('A', 0)
        stress_val = params.get('stress', 'P/A')

        # Tension Arrow (Dynamic color based on stress intensity if desired)
        ax.annotate('', xy=(0.85, 0.5), xytext=(0.7, 0.5),
                    arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=4))
        
        # Internal Formula Text
        display_text = f"$\\sigma = P/A$\n\n$\\sigma = {stress_val}$ MPa"
        ax.text(0.45, 0.5, display_text, fontsize=16, ha='center', va='center', fontweight='bold', color='#2c3e50')
        
        # Metadata labels
        ax.text(0.85, 0.55, f"P = {p_val} kN", color='#e74c3c', fontweight='bold', ha='left')
        ax.text(0.45, 0.22, f"Area (A) = {a_val} $mm^2$", ha='center', fontsize=11, color='#34495e')

        ax.set_xlim(0, 1.1)
        ax.set_ylim(0, 1)
        ax.axis('off')

    # Topic 3: Torsional Shear Stress
    elif "Torsional" in topic:
        circle = plt.Circle((0.5, 0.5), 0.35, color='#ecf0f1', ec='#2c3e50', lw=3)
        ax.add_patch(circle)
        ax.plot([0.5, 0.5], [0.5, 0.85], color='#2c3e50', ls='--') 
        
        ax.scatter([0.5], [0.5], color='#c0392b', s=80, zorder=5)
        ax.text(0.5, 0.42, "Neutral Axis\n$\\tau=0$", ha='center', fontsize=10, color='#c0392b')

        # Torque rotation arrow
        ax.annotate('', xy=(0.8, 0.7), xytext=(0.7, 0.85),
                    arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.5", lw=3, color='#3498db'))
        ax.text(0.8, 0.85, "Torque (T)", color='#3498db', fontweight='bold')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title("Shaft Cross-Section", fontsize=14, fontweight='bold')

    else:
        ax.text(0.5, 0.5, f"Visualizing:\n{topic}", ha='center', va='center', fontsize=14, style='italic')
        ax.axis('off')

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    plt.close(fig)
    buf.seek(0)
    return buf
