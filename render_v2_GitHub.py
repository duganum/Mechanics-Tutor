import matplotlib.pyplot as plt
import numpy as np
import io

def render_lecture_visual(topic, params=None):
    """
    Renders dynamic beam diagrams. 
    Synchronized with Main Code to handle conditional Bending Stress display.
    """
    if params is None: params = {}
    
    # Identify Beam-related labs
    if any(kw in topic for kw in ["Shearing Forces", "Beams", "Bending"]):
        p_val = params.get('P', 22) 
        pos = np.clip(params.get('L_pos', 500) / 1000, 0.05, 0.95)
        sigma_b = params.get('sigma_b') 
        L, x = 1.0, np.linspace(0, 1.0, 500)
        
        # Static equilibrium
        r1, r2 = p_val * (1 - pos), p_val * pos
        
        fig, (ax_beam, ax_shear, ax_moment) = plt.subplots(3, 1, figsize=(4, 6), dpi=150, sharex=True)
        
        # --- 1. Beam Diagram ---
        ax_beam.axhline(0, color='grey', lw=6)
        ax_beam.plot([0, L], [0, 0], marker='^', color='green', ms=10, ls='') 
        
        # SHORTENED ARROW: xytext=0.1 ensures the red arrow is short as requested
        ax_beam.annotate('', xy=(pos, 0), xytext=(pos, 0.1), 
                        arrowprops=dict(arrowstyle='->', color='red', lw=2))
        
        # CONDITIONAL TITLE: Only shows stress if the topic is "Stress Due to Bending"
        if "Stress Due to Bending" in topic and sigma_b is not None:
            title_text = f"Bending Stress (σ): {sigma_b:.2f} MPa"
        else:
            title_text = "Beam Loading & Support"
            
        ax_beam.set_title(title_text, fontsize=9)
        ax_beam.set_ylim(-0.05, 0.2) 
        ax_beam.axis('off')

        # --- 2. Shear Diagram (SFD) ---
        v_x = np.where(x < pos, r1, -r2)
        ax_shear.fill_between(x, v_x, color='blue', alpha=0.15)
        ax_shear.plot(x, v_x, color='blue', lw=1.5)
        ax_shear.set_ylabel("Shear (V)", fontsize=8)

        # --- 3. Bending Moment Diagram (BMD) ---
        m_x = np.where(x < pos, r1 * x, r1 * x - p_val * (x - pos))
        ax_moment.fill_between(x, m_x, color='red', alpha=0.15)
        ax_moment.plot(x, m_x, color='red', lw=1.5)
        ax_moment.set_ylabel("Moment (M)", fontsize=8)
        ax_moment.set_xlabel("Normalized Beam Length", fontsize=8)

        plt.tight_layout()
        return save_to_buffer(fig)

    # Fallback for other topics
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.text(0.5, 0.5, f"Visualizing:\n{topic}", ha='center', fontsize=8)
    ax.axis('off')
    return save_to_buffer(fig)

def render_problem_diagram(prob):
    """Diagram ID fallback for FE review section."""
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.text(0.5, 0.5, f"ID: {prob.get('id', 'N/A')}", ha='center', weight='bold')
    ax.axis('off')
    return save_to_buffer(fig)

def save_to_buffer(fig):
    """Utility to convert plots to Streamlit-compatible buffers."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf
