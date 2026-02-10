import matplotlib.pyplot as plt
import numpy as np
import io

def render_lecture_visual(topic, params=None):
    """Visualizes beam diagrams with 3-way interactivity: Magnitude, Location, and Area."""
    if params is None: params = {}
    
    # --- Topic: Shearing Forces and Bending Moments in Beams ---
    if "Shearing Forces" in topic:
        # 1. Slide: Force Magnitude (P)
        p_val = params.get('P', 22) 
        # 2. Slide: Force Location (L_pos) - normalized 0.05 to 0.95
        raw_loc = params.get('L_pos', 817) 
        pos = np.clip(raw_loc / 1000, 0.05, 0.95)
        # 3. Slide: Beam Area (A) for stress calculation
        a_val = params.get('A', 500) 
        
        L = 1.0 # Normalized beam length
        x = np.linspace(0, L, 500)
        
        # Reactions for simple supports
        r1 = p_val * (1 - pos / L) # Left support reaction
        r2 = p_val * (pos / L)     # Right support reaction
        
        # Calculate Stress based on Area Slide
        max_v = max(abs(r1), abs(r2))
        shear_stress = (max_v * 1000) / a_val # Convert kN to N for MPa
        
        # Setup 3-tier plot
        fig, (ax_beam, ax_shear, ax_moment) = plt.subplots(3, 1, figsize=(4, 6), dpi=150, sharex=True)
        
        # --- 1. Beam Diagram ---
        ax_beam.axhline(0, color='grey', lw=6, zorder=1) 
        ax_beam.plot(0, 0, '^', color='green', ms=10) # Pin
        ax_beam.plot(L, 0, 'o', color='green', ms=8)  # Roller
        ax_beam.annotate('', xy=(pos, 0), xytext=(pos, 0.5), 
                        arrowprops=dict(arrowstyle='->', color='red', lw=2))
        ax_beam.text(pos, 0.6, f'P={p_val}kN', ha='center', color='red', fontsize=8, weight='bold')
        ax_beam.set_title(f"Beam Analysis (Area: {a_val} mm²)", fontsize=9)
        ax_beam.set_ylim(-0.2, 0.8)
        ax_beam.axis('off')

        # --- 2. Shear Force Diagram (SFD) ---
        v_x = np.where(x < pos, r1, -r2)
        ax_shear.fill_between(x, v_x, color='blue', alpha=0.15)
        ax_shear.plot(x, v_x, color='blue', lw=1.5)
        ax_shear.axhline(0, color='black', lw=0.8)
        ax_shear.set_ylabel("Shear (V) [kN]", color='blue', fontsize=7)
        ax_shear.text(0.02, r1, f'{r1:.1f}', color='blue', fontsize=7, va='bottom')
        ax_shear.text(L-0.02, -r2, f'{-r2:.1f}', color='blue', fontsize=7, va='top', ha='right')

        # --- 3. Bending Moment Diagram (BMD) ---
        m_x = np.where(x < pos, r1 * x, r1 * x - p_val * (x - pos))
        max_m = r1 * pos
        ax_moment.fill_between(x, m_x, color='red', alpha=0.15)
        ax_moment.plot(x, m_x, color='red', lw=1.5)
        ax_moment.axhline(0, color='black', lw=0.8)
        ax_moment.set_ylabel("Moment (M) [kNm]", color='red', fontsize=7)
        ax_moment.text(pos, max_m, f'M_max={max_m:.1f}', color='red', fontsize=7, va='bottom', ha='center')
        ax_moment.set_xlabel(f"Max Shear Stress: {shear_stress:.2f} MPa", fontsize=8, weight='bold', color='darkgreen')

        plt.tight_layout()
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        return buf

    # --- Standard visual fallback for other topics ---
    fig, ax = plt.subplots(figsize=(3, 3), dpi=150)
    ax.text(0.5, 0.5, f"Visualizing:\n{topic}", ha='center', va='center', fontsize=8)
    ax.axis('off')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf

def render_problem_diagram(prob):
    """Generates standard problem diagrams."""
    fig, ax = plt.subplots(figsize=(3, 3), dpi=150)
    ax.text(0.5, 0.5, f"ID: {prob.get('id', 'Unknown')}", ha='center', va='center', weight='bold')
    ax.axis('off')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf
