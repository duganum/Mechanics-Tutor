import matplotlib.pyplot as plt
import numpy as np
import io

def render_lecture_visual(topic, params):
    """
    Renders dynamic engineering diagrams based on the lecture topic and slider parameters.
    Returns a BytesIO buffer containing the PNG image.
    """
    # Use a clean, professional style
    plt.style.use('fast')
    fig, ax = plt.subplots(figsize=(7, 4))
    
    # Topic 1: Direct Stress, Deformation, and Design
    if "Direct Stress" in topic:
        # Create specimen block
        rect = plt.Rectangle((0.2, 0.3), 0.5, 0.4, linewidth=2, edgecolor='black', facecolor='#f0f0f0')
        ax.add_patch(rect)
        
        # Pull values from params
        p_val = params.get('P', 'P')
        a_val = params.get('A', 'A')
        stress_val = params.get('stress', 'P/A')

        # Add Tension Arrows
        ax.annotate('', xy=(0.85, 0.5), xytext=(0.7, 0.5),
                    arrowprops=dict(arrowstyle='->', color='red', lw=3))
        ax.text(0.88, 0.5, f"P = {p_val} kN", color='red', fontweight='bold', va='center')
        
        # Display the live Formula and Value inside the block
        display_text = f"$\\sigma = P/A$\n\n$\\sigma = {stress_val}$ MPa"
        ax.text(0.45, 0.5, display_text, fontsize=14, ha='center', va='center', fontweight='bold')
        
        # Labels for dimensions
        ax.text(0.45, 0.25, f"Area = {a_val} $mm^2$", ha='center', fontsize=10, style='italic')

        ax.set_xlim(0, 1.1)
        ax.set_ylim(0, 1)
        ax.axis('off')

    # Topic 2: Design Properties of Materials (Stress-Strain Curve)
    elif "Properties" in topic:
        # Generate a standard ductile material curve (like steel)
        strain = np.linspace(0, 0.6, 200)
        # Simplified Hooke's Law + Plastic flow curve
        stress = 250 * (1 - np.exp(-10 * strain)) 
        
        ax.plot(strain, stress, color='#1f77b4', lw=3, label="Material Response")
        
        # Dynamic Point based on slider (if P is used as a proxy for load/stress)
        current_p = params.get('P', 50)
        current_strain = -np.log(1 - (current_p*2 / 250)) / 10 if current_p*2 < 250 else 0.5
        
        ax.scatter([current_strain], [current_p*2], color='red', s=100, zorder=5)
        ax.annotate(f"Current State", xy=(current_strain, current_p*2), xytext=(10, 10), 
                    textcoords='offset points', color='red', fontweight='bold')

        ax.set_xlabel("Strain (in/in or mm/mm)", fontsize=10)
        ax.set_ylabel("Stress (ksi or MPa)", fontsize=10)
        ax.set_title("Stress-Strain Relationship", fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_xlim(0, 0.6)
        ax.set_ylim(0, 300)

    # Topic 3: Torsional Shear Stress
    elif "Torsional" in topic:
        # Draw a cross-section of a shaft
        circle = plt.Circle((0.5, 0.5), 0.35, color='lightgrey', ec='black', lw=2)
        ax.add_patch(circle)
        ax.plot([0.5, 0.5], [0.5, 0.85], color='black', ls='--') # Radius line
        
        # Center point
        ax.scatter([0.5], [0.5], color='black', s=50)
        ax.text(0.5, 0.45, "Neutral Axis ($\\tau=0$)", ha='center', fontsize=9)

        # Torque Arrow
        ax.annotate('', xy=(0.8, 0.8), xytext=(0.6, 0.9),
                    arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.5", lw=2, color='blue'))
        ax.text(0.75, 0.9, "Torque (T)", color='blue', fontweight='bold')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title("Shaft Cross-Sectional Shear", fontsize=12)

    # Generic Fallback
    else:
        ax.text(0.5, 0.5, f"Visual for:\n{topic}", ha='center', va='center', fontsize=14)
        ax.axis('off')

    # Final layout adjustments
    plt.tight_layout()
    
    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    plt.close(fig)
    buf.seek(0)
    return buf
