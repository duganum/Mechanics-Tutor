import matplotlib.pyplot as plt
import numpy as np
import io

def render_lecture_visual(topic, params=None):
    if params is None: params = {}
    
    # Matching the Beam Lab Title
    if "Shearing Forces" in topic or "Beams" in topic:
        p_val = params.get('P', 22) 
        pos = np.clip(params.get('L_pos', 500) / 1000, 0.05, 0.95)
        L = 1.0 
        x = np.linspace(0, L, 500)
        
        r1 = p_val * (1 - pos) # Reaction Left
        r2 = p_val * pos       # Reaction Right
        
        # 3-Tier Diagram Setup
        fig, (ax_beam, ax_shear, ax_moment) = plt.subplots(3, 1, figsize=(4, 6), dpi=150, sharex=True)
        
        # ax_beam: Physical Beam
        ax_beam.axhline(0, color='grey', lw=6)
        ax_beam.plot([0, L], [0, 0], marker='^', color='green', ms=10, ls='')
        ax_beam.annotate('', xy=(pos, 0), xytext=(pos, 0.5), arrowprops=dict(arrowstyle='->', color='red', lw=2))
        ax_beam.set_title("Beam Loading & Support", fontsize=9)
        ax_beam.axis('off')

        # ax_shear: SFD
        v_x = np.where(x < pos, r1, -r2)
        ax_shear.fill_between(x, v_x, color='blue', alpha=0.15)
        ax_shear.plot(x, v_x, color='blue', lw=1.5)
        ax_shear.set_ylabel("Shear (V)", fontsize=8)

        # ax_moment: BMD
        m_x = np.where(x < pos, r1 * x, r1 * x - p_val * (x - pos))
        ax_moment.fill_between(x, m_x, color='red', alpha=0.15)
        ax_moment.plot(x, m_x, color='red', lw=1.5)
        ax_moment.set_ylabel("Moment (M)", fontsize=8)
        ax_moment.set_xlabel("Beam Length", fontsize=8)

        plt.tight_layout()
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return buf

    # Standard Fallback
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.text(0.5, 0.5, f"Visualizing: {topic}", ha='center')
    ax.axis('off')
    buf = io.BytesIO(); fig.savefig(buf, format='png'); plt.close(fig); buf.seek(0)
    return buf

def render_problem_diagram(prob):
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.text(0.5, 0.5, f"ID: {prob.get('id', 'N/A')}", ha='center', weight='bold')
    ax.axis('off')
    buf = io.BytesIO(); fig.savefig(buf, format='png'); plt.close(fig); buf.seek(0)
    return buf
