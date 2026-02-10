import matplotlib.pyplot as plt
import numpy as np
import io

def render_lecture_visual(topic, params=None):
    if params is None: params = {}
    lec_id = params.get('lec_id', 'SM_0')
    
    # SM_1: Design Properties (Stress-Strain with Red Dot)
    if lec_id == "SM_1":
        fig, ax = plt.subplots(figsize=(4, 3), dpi=150)
        strain = np.linspace(0, 0.5, 100)
        stress = np.where(strain < 0.1, strain * 10, 1.0 + (strain - 0.1) * 0.5)
        ax.plot(strain, stress, color='blue', lw=2)
        curr_s = params.get('stress', 0.0)
        curr_e = curr_s / 10.0 if curr_s <= 1.0 else 0.1 + (curr_s - 1.0) / 0.5
        if curr_e <= 0.5: ax.plot(curr_e, curr_s, 'ro', ms=8)
        ax.set_title("SM_1: Stress-Strain Behavior", fontsize=9)
        return save_to_buffer(fig)

    # SM_2: Direct Stress (Axial Load)
    elif lec_id == "SM_2":
        fig, ax = plt.subplots(figsize=(4, 3), dpi=150)
        ax.add_patch(plt.Rectangle((0.35, 0.2), 0.3, 0.6, color='skyblue', ec='black'))
        ax.set_title("SM_2: Direct Stress/Axial Load", fontsize=9)
        ax.axis('off')
        return save_to_buffer(fig)

    # SM_3: Torsional Shear Stress
    elif lec_id == "SM_3":
        fig, ax = plt.subplots(figsize=(4, 3), dpi=150)
        circle = plt.Circle((0.5, 0.5), 0.3, color='lightgray', ec='black')
        ax.add_patch(circle)
        ax.set_title("SM_3: Torsional Cross-Section", fontsize=9)
        ax.axis('off')
        return save_to_buffer(fig)

    # SM_4, SM_5, SM_6: Beam Related Labs
    elif lec_id in ["SM_4", "SM_5", "SM_6"]:
        p_val = params.get('P', 22)
        pos = np.clip(params.get('L_pos', 500) / 1000, 0.05, 0.95)
        sigma_b = params.get('sigma_b')
        L, x = 1.0, np.linspace(0, 1.0, 500)
        r1, r2 = p_val * (1 - pos), p_val * pos
        
        fig, (ax_b, ax_s, ax_m) = plt.subplots(3, 1, figsize=(4, 6), dpi=150, sharex=True)
        ax_b.axhline(0, color='grey', lw=6)
        # Short vector: xytext=0.1
        ax_b.annotate('', xy=(pos, 0), xytext=(pos, 0.1), arrowprops=dict(arrowstyle='->', color='red', lw=2))
        
        title = f"{lec_id}: Stress (σ): {sigma_b:.2f} MPa" if sigma_b else f"{lec_id}: Beam Diagram"
        ax_b.set_title(title, fontsize=9); ax_b.axis('off')
        
        v_x = np.where(x < pos, r1, -r2); ax_s.fill_between(x, v_x, color='blue', alpha=0.15); ax_s.set_ylabel("Shear")
        m_x = np.where(x < pos, r1 * x, r1 * x - p_val * (x - pos)); ax_m.fill_between(x, m_x, color='red', alpha=0.15); ax_m.set_ylabel("Moment")
        return save_to_buffer(fig)

    # Fallback for unrecognized IDs
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.text(0.5, 0.5, f"ID: {lec_id}\nVisual Missing", ha='center')
    ax.axis('off')
    return save_to_buffer(fig)

def render_problem_diagram(prob):
    """Retained for FE Exam review problems."""
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.text(0.5, 0.5, f"Diagram ID: {prob.get('id', 'N/A')}", ha='center', weight='bold')
    ax.axis('off')
    return save_to_buffer(fig)

def save_to_buffer(fig):
    buf = io.BytesIO(); fig.savefig(buf, format='png', bbox_inches='tight'); plt.close(fig); buf.seek(0)
    return buf
