import matplotlib.pyplot as plt
import numpy as np
import io

def render_lecture_visual(topic, params=None):
    """
    Generates 3-tier engineering diagrams for Beam labs.
    Synchronized with Main Code to handle Magnitude, Location, and Section Modulus.
    """
    if params is None: params = {}
    
    # Matching the specific lab topics for Beams and Bending
    if any(keyword in topic for keyword in ["Shearing Forces", "Beams", "Bending"]):
        p_val = params.get('P', 22) 
        # Normalize 0-1000 input to 0-1 beam length
        pos = np.clip(params.get('L_pos', 500) / 1000, 0.05, 0.95)
        sigma_b = params.get('sigma_b', 0.0)
        L, x = 1.0, np.linspace(0, 1.0, 500)
        
        # Static Equilibrium Reactions
        r1, r2 = p_val * (1 - pos), p_val * pos
        
        # Setup 3-Tier aligned diagrams
        fig, (ax_beam, ax_shear, ax_moment) = plt.subplots(3, 1, figsize=(4, 6), dpi=150, sharex=True)
        
        # --- 1. Beam Diagram: Shortened Force Vector ---
        ax_beam.axhline(0, color='grey', lw=6)
        ax_beam.plot([0, L], [0, 0], marker='^', color='green', ms=10, ls='') # Supports
        
        # xytext determines arrow length; 0.1 creates the requested short vector
        ax_beam.annotate('', xy=(pos, 0), xytext=(pos, 0.1), 
                        arrowprops=dict(arrowstyle='->', color='red', lw=2))
        
        ax_beam.set_title(f"Bending Stress (σ): {sigma_b:.2f} MPa", fontsize=9)
        ax_beam.set_ylim(-0.05, 0.2) # Tightened window to frame the short arrow
        ax_beam.axis('off')

        # --- 2. Shear Force Diagram (SFD) ---
        v_x = np.where(x < pos, r1, -r2)
        ax_shear.fill_between(x, v_x, color='blue', alpha=0.15)
        ax_shear.plot(x, v_x, color='blue', lw=1.5)
        ax_shear.axhline(0, color='black', lw=0.5)
        ax_shear.set_ylabel("Shear (V)", fontsize=8)

        # --- 3. Bending Moment Diagram (BMD) ---
        m_x = np.where(x < pos, r1 * x, r1 * x - p_val * (x - pos))
        ax_moment.fill_between(x, m_x, color='red', alpha=0.15)
        ax_moment.plot(x, m_x, color='red', lw=1.5)
        ax_moment.axhline(0, color='black', lw=0.5)
        ax_moment.set_ylabel("Moment (M)", fontsize=8)
        ax_moment.set_xlabel("Normalized Beam Length", fontsize=8)

        plt.tight_layout()
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return buf

    # Standard Fallback for other lecture topics
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.text(0.5, 0.5, f"Visualizing:\n{topic}", ha='center', fontsize=8)
    ax.axis('off')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf

def render_problem_diagram(prob):
    """Generates standard problem diagrams based on Problem ID."""
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.text(0.5, 0.5, f"ID: {prob.get('id', 'N/A')}", ha='center', weight='bold')
    ax.axis('off')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf
