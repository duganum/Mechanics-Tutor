import matplotlib.pyplot as plt
import numpy as np
import io

def render_lecture_visual(topic, params=None):
    """
    Core rendering engine for interactive labs. 
    Handles Axial, Torsional, and Beam Bending visualizations.
    """
    if params is None: params = {}
    
    # --- 1. Topic: Shearing Forces, Bending Moments, and Stress Due to Bending ---
    if any(kw in topic for kw in ["Shearing Forces", "Beams", "Bending"]):
        p_val = params.get('P', 22) 
        # Normalize L_pos slider (0-1000) to beam length (0-1)
        pos = np.clip(params.get('L_pos', 500) / 1000, 0.05, 0.95)
        sigma_b = params.get('sigma_b', 0.0)
        L, x = 1.0, np.linspace(0, 1.0, 500)
        
        # Calculate Reactions for Simple Support
        r1, r2 = p_val * (1 - pos), p_val * pos
        
        # Create 3-Tier stacked subplots
        fig, (ax_beam, ax_shear, ax_moment) = plt.subplots(3, 1, figsize=(4, 6), dpi=150, sharex=True)
        
        # ax_beam: Physical Beam with Shortened Force Vector
        ax_beam.axhline(0, color='grey', lw=6)
        ax_beam.plot([0, L], [0, 0], marker='^', color='green', ms=10, ls='') 
        
        # Shortened arrow logic: xytext height reduced to 0.1
        ax_beam.annotate('', xy=(pos, 0), xytext=(pos, 0.1), 
                        arrowprops=dict(arrowstyle='->', color='red', lw=2))
        
        ax_beam.set_title(f"Bending Stress (σ): {sigma_b:.2f} MPa", fontsize=9)
        ax_beam.set_ylim(-0.05, 0.2) # Adjusted window height for the shorter arrow
        ax_beam.axis('off')

        # ax_shear: Shear Force Diagram (SFD)
        v_x = np.where(x < pos, r1, -r2)
        ax_shear.fill_between(x, v_x, color='blue', alpha=0.15)
        ax_shear.plot(x, v_x, color='blue', lw=1.5)
        ax_shear.axhline(0, color='black', lw=0.5)
        ax_shear.set_ylabel("Shear (V)", fontsize=8)

        # ax_moment: Bending Moment Diagram (BMD)
        m_x = np.where(x < pos, r1 * x, r1 * x - p_val * (x - pos))
        ax_moment.fill_between(x, m_x, color='red', alpha=0.15)
        ax_moment.plot(x, m_x, color='red', lw=1.5)
        ax_moment.axhline(0, color='black', lw=0.5)
        ax_moment.set_ylabel("Moment (M)", fontsize=8)
        ax_moment.set_xlabel("Normalized Beam Length", fontsize=8)

        plt.tight_layout()
        return save_to_buffer(fig)

    # --- 2. Topic: Torsional Shear Stress ---
    elif "Torsional" in topic:
        fig, ax = plt.subplots(figsize=(3, 3), dpi=150)
        t_val = params.get('P', 22) # Magnitude slider
        circle = plt.Circle((0.5, 0.5), 0.35, color='lightgray', ec='black', lw=2)
        ax.add_patch(circle)
        
        # Draw shear stress vectors around the perimeter
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            dx, dy = 0.25 * np.cos(angle), 0.25 * np.sin(angle)
            ax.arrow(0.5 + dx, 0.5 + dy, -0.1*np.sin(angle), 0.1*np.cos(angle), 
                     head_width=0.03, color='red')
        
        ax.set_title(f"Torsion: {t_val} kN-m", fontsize=9)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
        return save_to_buffer(fig)

    # --- 3. Topic: Design Properties / Direct Stress ---
    elif "Stress" in topic or "Properties" in topic:
        fig, ax = plt.subplots(figsize=(3, 3), dpi=150)
        p_val, a_val = params.get('P', 22), params.get('A', 817)
        stress = params.get('stress', 0.0)
        
        ax.add_patch(plt.Rectangle((0.35, 0.2), 0.3, 0.6, color='skyblue', alpha=0.6, ec='black'))
        ax.annotate('', xy=(0.5, 0.95), xytext=(0.5, 0.8), arrowprops=dict(arrowstyle='->', lw=2, color='red'))
        ax.text(0.5, 0.5, f"σ = {stress} MPa", ha='center', va='center', fontsize=8, weight='bold')
        
        ax.set_xlim(0, 1); ax.set_ylim(0, 1.1); ax.axis('off')
        return save_to_buffer(fig)

    # --- 4. Fallback: Default Visual ---
    else:
        fig, ax = plt.subplots(figsize=(3, 3))
        ax.text(0.5, 0.5, f"Visualizing:\n{topic}", ha='center', fontsize=8)
        ax.axis('off')
        return save_to_buffer(fig)

def render_problem_diagram(prob):
    """Renders basic diagrams for practice problems."""
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.text(0.5, 0.5, f"Diagram ID:\n{prob.get('id', 'N/A')}", ha='center', weight='bold')
    ax.axis('off')
    return save_to_buffer(fig)

def save_to_buffer(fig):
    """Helper to convert matplotlib figures to an image buffer."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf
