import matplotlib.pyplot as plt
import numpy as np
import io

def render_lecture_visual(topic, params=None):
    """Revised visualizer for Beam Labs with 3-slider logic."""
    if params is None: params = {}
    
    # 1. Broaden the match condition to catch the exact lab title
    if "Shearing Forces" in topic or "Bending Moments" in topic:
        # 2. Assign Slider Logic
        # P = Magnitude (Force Slider)
        # L_pos = Location (Repurposed from a secondary slider if available)
        # A = Beam Area (Area Slider)
        p_val = params.get('P', 22) 
        a_val = params.get('A', 817)
        # Mapping the location to either a specific 'L_pos' or using 'A' as a fallback
        loc_input = params.get('L_pos', a_val) 
        pos = np.clip(loc_input / 1000, 0.05, 0.95)
        
        L = 1.0
        x = np.linspace(0, L, 500)
        
        # Static Reactions
        r1 = p_val * (1 - pos / L)
        r2 = p_val * (pos / L)
        
        # Stress Calculation
        max_v = max(abs(r1), abs(r2))
        shear_stress = (max_v * 1000) / max(1, a_val) # MPa (N/mm^2)
        
        # Create the 3-tier engineering diagram
        fig, (ax_beam, ax_shear, ax_moment) = plt.subplots(3, 1, figsize=(4, 6), dpi=150, sharex=True)
        
        # Beam Diagram
        ax_beam.axhline(0, color='grey', lw=6)
        ax_beam.plot(0, 0, '^', color='green', ms=10) 
        ax_beam.plot(L, 0, 'o', color='green', ms=8)
        ax_beam.annotate('', xy=(pos, 0), xytext=(pos, 0.5), 
                        arrowprops=dict(arrowstyle='->', color='red', lw=2))
        ax_beam.set_title(f"Force: {p_val}kN | Stress: {shear_stress:.2f}MPa", fontsize=9)
        ax_beam.axis('off')

        # Shear Diagram
        v_x = np.where(x < pos, r1, -r2)
        ax_shear.fill_between(x, v_x, color='blue', alpha=0.15)
        ax_shear.plot(x, v_x, color='blue', lw=1.5)
        ax_shear.set_ylabel("Shear (V)", fontsize=8)

        # Moment Diagram
        m_x = np.where(x < pos, r1 * x, r1 * x - p_val * (x - pos))
        ax_moment.fill_between(x, m_x, color='red', alpha=0.15)
        ax_moment.plot(x, m_x, color='red', lw=1.5)
        ax_moment.set_ylabel("Moment (M)", fontsize=8)
        ax_moment.set_xlabel("Normalized Beam Length", fontsize=8)

        plt.tight_layout()
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return buf

    # Fallback to identify what topic string is actually being passed
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.text(0.5, 0.5, f"No Match Found For:\n{topic}", ha='center', fontsize=8)
    ax.axis('off')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf

def render_problem_diagram(prob):
    """Problem diagram fallback."""
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.text(0.5, 0.5, f"Problem ID: {prob.get('id', 'N/A')}", ha='center')
    ax.axis('off')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf
