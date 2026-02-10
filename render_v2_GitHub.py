import matplotlib.pyplot as plt
import numpy as np
import io

def render_lecture_visual(topic, params=None):
    if params is None: params = {}
    lec_id = params.get('lec_id', 'SM_0')
    
    # SM_1: Design Properties (With Red Tracking Dot)
    if lec_id == "SM_1":
        fig, ax = plt.subplots(figsize=(4, 3), dpi=150)
        strain_coords = np.linspace(0, 0.5, 100)
        # Define the reference blue curve
        stress_coords = np.where(strain_coords < 0.1, strain_coords * 10, 1.0 + (strain_coords - 0.1) * 0.5)
        ax.plot(strain_coords, stress_coords, color='blue', lw=2)
        
        # --- Red Dot Logic ---
        # Get live stress from params, then scale for the graph (max y-axis is 1.2)
        curr_s_raw = params.get('stress', 0.0)
        # Normalize stress to fit graph scale (assume 100 MPa = 1.0 stress unit on graph)
        curr_s = curr_s_raw / 100.0 
        
        # Calculate strain based on the same curve logic
        if curr_s <= 1.0:
            curr_e = curr_s / 10.0
        else:
            curr_e = 0.1 + (curr_s - 1.0) / 0.5
            
        # Draw the tracking red dot if within bounds
        if curr_e <= 0.5: 
            ax.plot(curr_e, curr_s, 'ro', ms=8, label='Current State')
        
        ax.set_title(f"{lec_id}: Stress-Strain Behavior", fontsize=9)
        ax.set_xlabel("Strain (ε)"); ax.set_ylabel("Stress (σ)")
        ax.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        return save_to_buffer(fig)

    # SM_2: Direct Stress
    elif lec_id == "SM_2":
        fig, ax = plt.subplots(figsize=(4, 3), dpi=150)
        ax.add_patch(plt.Rectangle((0.35, 0.2), 0.3, 0.6, color='skyblue', ec='black'))
        ax.set_title("SM_2: Axial Load Diagram", fontsize=9); ax.axis('off')
        return save_to_buffer(fig)

    # SM_3: Torsional Shear
    elif lec_id == "SM_3":
        fig, ax = plt.subplots(figsize=(4, 3), dpi=150)
        ax.add_patch(plt.Circle((0.5, 0.5), 0.3, color='lightgray', ec='black'))
        ax.set_title("SM_3: Torsional Cross-Section", fontsize=9); ax.axis('off')
        return save_to_buffer(fig)

    # SM_4, SM_5, SM_6: Beam Labs
    elif lec_id in ["SM_4", "SM_5", "SM_6"]:
        p_val, pos = params.get('P', 22), np.clip(params.get('L_pos', 500) / 1000, 0.05, 0.95)
        sigma_b = params.get('sigma_b')
        L, x = 1.0, np.linspace(0, 1.0, 500)
        r1, r2 = p_val * (1 - pos), p_val * pos
        
        fig, (ax_b, ax_s, ax_m) = plt.subplots(3, 1, figsize=(4, 6), dpi=150, sharex=True)
        ax_b.axhline(0, color='grey', lw=6); ax_b.plot([0, L], [0, 0], marker='^', color='green', ms=10, ls='')
        ax_b.annotate('', xy=(pos, 0), xytext=(pos, 0.1), arrowprops=dict(arrowstyle='->', color='red', lw=2))
        
        title = f"Bending Stress (σ): {sigma_b:.2f} MPa" if sigma_b else "Beam Diagram"
        ax_b.set_title(title, fontsize=9); ax_b.axis('off')
        
        v_x = np.where(x < pos, r1, -r2); ax_s.fill_between(x, v_x, color='blue', alpha=0.15)
        m_x = np.where(x < pos, r1 * x, r1 * x - p_val * (x - pos)); ax_m.fill_between(x, m_x, color='red', alpha=0.15)
        
        plt.tight_layout(); return save_to_buffer(fig)

    return save_to_buffer(plt.figure(figsize=(3,3)))

def render_problem_diagram(prob):
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.text(0.5, 0.5, f"ID: {prob.get('id', 'N/A')}", ha='center'); ax.axis('off')
    return save_to_buffer(fig)

def save_to_buffer(fig):
    buf = io.BytesIO(); fig.savefig(buf, format='png', bbox_inches='tight'); plt.close(fig); buf.seek(0)
    return buf
