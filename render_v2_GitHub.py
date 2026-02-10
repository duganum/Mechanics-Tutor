import matplotlib.pyplot as plt
import numpy as np
import io

def render_lecture_visual(topic, params=None):
    """
    Core rendering engine for interactive engineering labs.
    Handles Material Properties, Axial Stress, and Beam Bending.
    """
    if params is None: params = {}
    
    # 1. Topic: Design Properties of Materials (RESTORED)
    if "Design Properties" in topic:
        fig, ax = plt.subplots(figsize=(4, 3), dpi=150)
        # Generate a standard stress-strain curve for visualization
        strain = np.linspace(0, 0.5, 100)
        # Simplified elastic-plastic model
        stress_curve = np.where(strain < 0.1, strain * 10, 1.0 + (strain - 0.1) * 0.5)
        ax.plot(strain, stress_curve, color='blue', lw=2)
        ax.set_title("Stress-Strain Behavior", fontsize=9)
        ax.set_xlabel("Strain (ε)", fontsize=8)
        ax.set_ylabel("Stress (σ)", fontsize=8)
        ax.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        return save_to_buffer(fig)

    # 2. Topics: Beams, Shearing Forces, and Bending
    elif any(kw in topic for kw in ["Shearing Forces", "Beams", "Bending"]):
        p_val = params.get('P', 22) 
        # Normalize L_pos slider (0-1000) to beam length (0-1)
        pos = np.clip(params.get('L_pos', 500) / 1000, 0.05, 0.95)
        sigma_b = params.get('sigma_b') 
        L, x = 1.0, np.linspace(0, 1.0, 500)
        
        # Static equilibrium reactions
        r1, r2 = p_val * (1 - pos), p_val * pos
        
        fig, (ax_beam, ax_shear, ax_moment) = plt.subplots(3, 1, figsize=(4, 6), dpi=150, sharex=True)
        
        # --- ax_beam: Loading Diagram with Shortened Arrow ---
        ax_beam.axhline(0, color='grey', lw=6)
        ax_beam.plot([0, L], [0, 0], marker='^', color='green', ms=10, ls='') 
        
        # Force arrow: xytext=0.1 creates the requested short vector
        ax_beam.annotate('', xy=(pos, 0), xytext=(pos, 0.1), 
                        arrowprops=dict(arrowstyle='->', color='red', lw=2))
        
        # Conditional Title: Only show stress for the specific Bending Lab
        if "Stress Due to Bending" in topic and sigma_b is not None:
            title_text = f"Bending Stress (σ): {sigma_b:.2f} MPa"
        else:
            title_text = "Beam Loading & Support"
            
        ax_beam.set_title(title_text, fontsize=9)
        ax_beam.set_ylim(-0.05, 0.2) 
        ax_beam.axis('off')

        # --- ax_shear: SFD ---
        v_x = np.where(x < pos, r1, -r2)
        ax_shear.fill_between(x, v_x, color='blue', alpha=0.15)
        ax_shear.plot(x, v_x, color='blue', lw=1.5)
        ax_shear.axhline(0, color='black', lw=0.5)
        ax_shear.set_ylabel("Shear (V)", fontsize=8)

        # --- ax_moment: BMD ---
        m_x = np.where(x < pos, r1 * x, r1 * x - p_val * (x - pos))
        ax_moment.fill_between(x, m_x, color='red', alpha=0.15)
        ax_moment.plot(x, m_x, color='red', lw=1.5)
        ax_moment.axhline(0, color='black', lw=0.5)
        ax_moment.set_ylabel("Moment (M)", fontsize=8)
        ax_moment.set_xlabel("Normalized Beam Length", fontsize=8)

        plt.tight_layout()
        return save_to_buffer(fig)

    # 3. Fallback: Generic display for other topics
    else:
        fig, ax = plt.subplots(figsize=(3, 3))
        ax.text(0.5, 0.5, f"Visualizing:\n{topic}", ha='center', fontsize=8)
        ax.axis('off')
        return save_to_buffer(fig)

def save_to_buffer(fig):
    """Utility to convert Matplotlib figures to Streamlit buffers."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf

def render_problem_diagram(prob):
    """Renders basic ID-based diagrams for review problems."""
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.text(0.5, 0.5, f"Diagram ID: {prob.get('id', 'N/A')}", ha='center', weight='bold')
    ax.axis('off')
    return save_to_buffer(fig)
