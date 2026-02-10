import matplotlib.pyplot as plt
import numpy as np
import io

def render_lecture_visual(topic, params=None):
    """Visualizes derivation components with dynamic updates."""
    if params is None: params = {}
    
    # --- Topic: Shearing Forces and Bending Moments in Beams ---
    if "Shearing Forces" in topic:
        # P = Load Magnitude from 'Force' slider
        # L_pos = Load Position from 'Area' slider (mapped 0.0 to 1.0)
        p_val = params.get('P', 22)
        area_slider = params.get('A', 817)
        
        # We normalize the 'Area' slider value (typically 0-1000) to a 0-1 beam length
        # This effectively turns the Area slider into a Location slider
        L = 1.0 
        pos = np.clip(area_slider / 1000, 0.05, 0.95) 
        
        # Create 3 stacked subplots aligned vertically
        fig, (ax_beam, ax_shear, ax_moment) = plt.subplots(3, 1, figsize=(4, 6), dpi=150, sharex=True)
        x = np.linspace(0, L, 500)
        
        # Static Equilibrium Reactions
        r1 = p_val * (1 - pos / L) # Left support
        r2 = p_val * (pos / L)     # Right support
        
        # 1. Physical Beam Diagram
        ax_beam.axhline(0, color='grey', lw=6, zorder=1) 
        ax_beam.plot(0, 0, '^', color='green', ms=10, label='Pin') 
        ax_beam.plot(L, 0, 'o', color='green', ms=8, label='Roller') 
        # The Red Arrow moves as you slide the 'Area' slider
        ax_beam.annotate('', xy=(pos, 0), xytext=(pos, 0.5), 
                        arrowprops=dict(arrowstyle='->', color='red', lw=2))
        ax_beam.text(pos, 0.6, f'P={p_val}kN', ha='center', color='red', fontsize=8, weight='bold')
        ax_beam.set_ylim(-0.2, 0.8)
        ax_beam.set_title("Beam Loading & Support", fontsize=9)
        ax_beam.axis('off')

        # 2. Shear Force Diagram (SFD)
        v_x = np.where(x < pos, r1, -r2)
        ax_shear.fill_between(x, v_x, color='blue', alpha=0.15)
        ax_shear.plot(x, v_x, color='blue', lw=1.5)
        ax_shear.axhline(0, color='black', lw=0.8)
        ax_shear.set_ylabel("Shear (V)", color='blue', fontsize=8)
        ax_shear.text(0.02, r1, f'{r1:.1f}', color='blue', fontsize=7, va='bottom')
        ax_shear.text(L-0.02, -r2, f'{-r2:.1f}', color='blue', fontsize=7, va='top', ha='right')

        # 3. Bending Moment Diagram (BMD)
        m_x = np.where(x < pos, r1 * x, r1 * x - p_val * (x - pos))
        max_m = r1 * pos
        ax_moment.fill_between(x, m_x, color='red', alpha=0.15)
        ax_moment.plot(x, m_x, color='red', lw=1.5)
        ax_moment.axhline(0, color='black', lw=0.8)
        ax_moment.set_ylabel("Moment (M)", color='red', fontsize=8)
        ax_moment.text(pos, max_m, f'M_max={max_m:.1f}', color='red', fontsize=7, va='bottom', ha='center')
        ax_moment.set_xlabel("Beam Length (x/L)", fontsize=8)

        plt.tight_layout()
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return buf

    # --- Topic 1, 2, 3 Logic ---
    fig, ax = plt.subplots(figsize=(3, 3), dpi=150)
    if topic == "Design Properties of Materials":
        ax.set_title("Stress-Strain Curve", fontsize=9)
    elif topic == "Direct Stress, Deformation, and Design":
        ax.set_title("Direct Stress Analysis", fontsize=9)
    elif "Torsional" in topic:
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
    """Placeholder for individual problem diagrams."""
    fig, ax = plt.subplots(figsize=(3, 3), dpi=150)
    ax.text(0.5, 0.5, f"Problem Diagram\nID: {prob.get('id', 'Unknown')}", 
            ha='center', va='center', weight='bold', fontsize=9)
    ax.axis('off')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf
