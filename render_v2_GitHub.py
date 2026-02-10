import matplotlib.pyplot as plt
import numpy as np
import io

def render_lecture_visual(topic, params=None):
    """Visualizes derivation components with dynamic updates. Reduced size by 50%."""
    # Reduced figsize from (6, 6) to (3, 3) for a 50% smaller footprint
    fig, ax = plt.subplots(figsize=(3, 3), dpi=150)
    if params is None: params = {}
    
    # --- Topic 1: Design Properties of Materials ---
    if topic == "Design Properties of Materials":
        strain_elastic = np.linspace(0, 0.05, 50)
        stress_elastic = 4000 * strain_elastic 
        strain_plastic = np.linspace(0.05, 0.5, 100)
        stress_plastic = 200 + 100 * np.sqrt(strain_plastic - 0.05)
        
        strain = np.concatenate([strain_elastic, strain_plastic])
        stress = np.concatenate([stress_elastic, stress_plastic])
        ax.plot(strain, stress, 'b-', lw=1.5)
        
        p_val = params.get('P', 22)
        a_val = params.get('A', 817)
        curr_stress = (p_val * 1000) / a_val # MPa
        
        curr_strain = curr_stress / 4000 if curr_stress <= 200 else 0.05 + ((curr_stress - 200) / 100)**2
        ax.scatter(curr_strain, curr_stress, color='red', s=50, zorder=5)
        ax.set_title("Stress-Strain Curve", fontsize=9)
        ax.set_xlim(0, 0.6); ax.set_ylim(0, 400)
        ax.grid(True, linestyle=':', alpha=0.6)

    # --- Topic 2: Direct Stress, Deformation, and Design ---
    elif topic == "Direct Stress, Deformation, and Design":
        p_val = params.get('P', 22)
        a_val = params.get('A', 817)
        stress = params.get('stress', round((p_val * 1000) / a_val, 2))

        ax.add_patch(plt.Rectangle((0.35, 0.2), 0.3, 0.6, color='skyblue', alpha=0.6, ec='black', lw=1))
        ax.annotate('', xy=(0.5, 0.95), xytext=(0.5, 0.8), arrowprops=dict(arrowstyle='->', lw=2, color='red'))
        ax.annotate('', xy=(0.5, 0.05), xytext=(0.5, 0.2), arrowprops=dict(arrowstyle='->', lw=2, color='red'))
        ax.text(0.5, 0.98, f'P = {p_val} kN', ha='center', color='red', fontsize=8, weight='bold')
        ax.text(0.5, 0.5, f'σ = {stress} MPa\nA = {a_val} mm²', ha='center', va='center', 
                fontsize=8, bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
        ax.set_xlim(0, 1); ax.set_ylim(0, 1.1); ax.axis('off')

    # --- Topic 3: Torsional Shear Stress and Torsional Deformation ---
    elif "Torsional" in topic:
        t_val = params.get('P', 22)
        radius = np.sqrt(params.get('A', 817) / np.pi)
        circle = plt.Circle((0.5, 0.5), 0.35, color='lightgray', ec='black', lw=2, alpha=0.7)
        ax.add_patch(circle)
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            dx, dy = 0.25 * np.cos(angle), 0.25 * np.sin(angle)
            ax.arrow(0.5 + dx, 0.5 + dy, -0.1*np.sin(angle), 0.1*np.cos(angle), head_width=0.03, color='red')
        ax.text(0.5, 0.5, f"T = {t_val} kN-m\nr ≈ {radius:.1f} mm", ha='center', va='center', fontsize=7)
        ax.set_title("Torsional Shear Analysis", fontsize=9)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

    # --- Topic 4: Shearing Forces and Bending Moments in Beams ---
    elif "Shearing Forces" in topic:
        p_val = params.get('P', 22)
        # Use A slider to control position of load (normalized 0.1 to 0.9)
        raw_a = params.get('A', 400)
        pos = 0.1 + (raw_a / 1000) * 0.8 
        
        x = np.linspace(0, 1, 500)
        # Reactions for simple support
        r_right = p_val * pos
        r_left = p_val * (1 - pos)
        
        # Shear Force V(x)
        v_x = np.where(x < pos, r_left, -r_right)
        ax.fill_between(x, v_x, color='teal', alpha=0.3)
        ax.plot(x, v_x, color='teal', lw=1.5, label='Shear (V)')
        
        # Draw the beam and point load
        ax.axhline(0, color='black', lw=2)
        ax.annotate('', xy=(pos, 0), xytext=(pos, p_val*0.4), 
                    arrowprops=dict(arrowstyle='->', color='red', lw=2))
        
        ax.set_title("Shear Force Diagram", fontsize=9)
        ax.set_ylabel("V (kN)", fontsize=8)
        ax.set_xlim(0, 1)
        ax.grid(True, linestyle=':', alpha=0.5)

    # --- Default Fallback ---
    else:
        ax.text(0.5, 0.5, f"Visualizing:\n{topic}", ha='center', va='center', fontsize=8)
        ax.axis('off')

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf

def render_problem_diagram(prob):
    """Generates diagrams for specific practice problems."""
    fig, ax = plt.subplots(figsize=(3, 3), dpi=150)
    ax.text(0.5, 0.5, f"Problem Diagram\nID: {prob.get('id', 'Unknown')}", 
            ha='center', va='center', weight='bold', fontsize=9)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf
