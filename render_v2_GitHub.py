import matplotlib.pyplot as plt
import numpy as np
import io

def render_lecture_visual(topic, params=None):
    """Visualizes derivation components with dynamic updates."""
    if params is None: params = {}
    
    # --- Topic 4: Shearing Forces and Bending Moments in Beams ---
    if "Shearing Forces" in topic:
        # P = Load Magnitude, A = Load Position (mapped 0 to 1)
        p_val = params.get('P', 22)
        raw_a = params.get('A', 400)
        pos = np.clip(raw_a / 1000, 0.05, 0.95) # Normalize position
        L = 1.0 # Normalized beam length
        
        # Create 3 stacked subplots
        fig, (ax_beam, ax_shear, ax_moment) = plt.subplots(3, 1, figsize=(4, 5), dpi=150, sharex=True)
        x = np.linspace(0, L, 500)
        
        # Reactions for a simple support
        r1 = p_val * (1 - pos / L)
        r2 = p_val * (pos / L)
        
        # 1. Beam Diagram
        ax_beam.axhline(0, color='grey', lw=6, zorder=1) # The Beam
        ax_beam.plot(0, 0, '^', color='green', ms=10) # Pin support
        ax_beam.plot(L, 0, 'o', color='green', ms=8)  # Roller support
        ax_beam.annotate('', xy=(pos, 0), xytext=(pos, 0.5), 
                        arrowprops=dict(arrowstyle='->', color='red', lw=2))
        ax_beam.text(pos, 0.6, f'P={p_val}kN', ha='center', color='red', fontsize=8, weight='bold')
        ax_beam.set_ylim(-0.2, 0.8)
        ax_beam.set_title("Beam Loading", fontsize=9)
        ax_beam.axis('off')

        # 2. Shear Force Diagram (SFD)
        v_x = np.where(x < pos, r1, -r2)
        ax_shear.fill_between(x, v_x, color='blue', alpha=0.2)
        ax_shear.plot(x, v_x, color='blue', lw=1.5)
        ax_shear.axhline(0, color='black', lw=1)
        ax_shear.set_ylabel("Shear (V)", color='blue', fontsize=8)
        ax_shear.text(0.02, r1, f'{r1:.1f}', color='blue', fontsize=7, va='bottom')
        ax_shear.text(L-0.02, -r2, f'{-r2:.1f}', color='blue', fontsize=7, va='top', ha='right')

        # 3. Bending Moment Diagram (BMD)
        # M = R1*x for x < pos; M = R1*x - P(x-pos) for x > pos
        m_x = np.where(x < pos, r1 * x, r1 * x - p_val * (x - pos))
        max_m = r1 * pos
        ax_moment.fill_between(x, m_x, color='red', alpha=0.2)
        ax_moment.plot(x, m_x, color='red', lw=1.5)
        ax_moment.axhline(0, color='black', lw=1)
        ax_moment.set_ylabel("Moment (M)", color='red', fontsize=8)
        ax_moment.text(pos, max_m, f'{max_m:.1f}', color='red', fontsize=7, va='bottom', ha='center')
        ax_moment.set_xlabel("Beam Length (L)", fontsize=8)

        plt.tight_layout()
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return buf

    # --- Topic 1, 2, 3 and Default logic (Compressed for brevity) ---
    fig, ax = plt.subplots(figsize=(3, 3), dpi=150)
    if topic == "Design Properties of Materials":
        # ... (keep existing stress-strain logic)
        ax.set_title("Stress-Strain Curve", fontsize=9)
    elif topic == "Direct Stress, Deformation, and Design":
        # ... (keep existing axial logic)
        ax.set_title("Direct Stress Analysis", fontsize=9)
    elif "Torsional" in topic:
        # ... (keep existing torsion logic)
        ax.set_title("Torsional Shear Analysis", fontsize=9)
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
    ax.axis('off')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf
