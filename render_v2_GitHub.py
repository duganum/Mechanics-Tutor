import matplotlib.pyplot as plt
import numpy as np
import io
import matplotlib.transforms as mtransforms

def render_lecture_visual(topic, params=None):
    if params is None: params = {}
    lec_id = params.get('lec_id', 'SM_0')
    
    # SM_1 to SM_7 logic remains unchanged as per instructions
    if lec_id == "SM_1":
        fig, ax = plt.subplots(figsize=(4, 3), dpi=150)
        strain_coords = np.linspace(0, 0.5, 100)
        stress_coords = np.where(strain_coords < 0.1, strain_coords * 10, 1.0 + (strain_coords - 0.1) * 0.5)
        ax.plot(strain_coords, stress_coords, color='blue', lw=2)
        curr_s_raw = params.get('stress', 0.0)
        curr_s = curr_s_raw / 100.0 
        curr_e = curr_s / 10.0 if curr_s <= 1.0 else 0.1 + (curr_s - 1.0) / 0.5
        if curr_e <= 0.5: 
            ax.plot(curr_e, curr_s, 'ro', ms=8, label='Current State')
        ax.set_title(f"{lec_id}: Stress-Strain Behavior", fontsize=9)
        ax.set_xlabel("Strain (ε)"); ax.set_ylabel("Stress (σ)")
        ax.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        return save_to_buffer(fig)

    elif lec_id == "SM_2":
        fig, ax = plt.subplots(figsize=(4, 3), dpi=150)
        p_val = params.get('P', 0)
        stress = params.get('stress', 0.0)
        ax.add_patch(plt.Rectangle((0.35, 0.2), 0.3, 0.6, color='skyblue', ec='black'))
        ax.text(0.5, 0.5, f"σ = {stress:.2f} MPa", ha='center', va='center', fontweight='bold')
        ax.annotate(f'P = {p_val} kN', xy=(0.5, 0.8), xytext=(0.5, 0.95),
                    arrowprops=dict(arrowstyle='<-', color='red', lw=2), ha='center')
        ax.set_title("SM_2: Axial Load Diagram", fontsize=9)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
        return save_to_buffer(fig)

    elif lec_id == "SM_3":
        fig, ax = plt.subplots(figsize=(4, 4), dpi=150)
        stress = params.get('stress', 0.0)
        radius, cx, cy = 0.3, 0.5, 0.5
        cyan_col = '#00bcd4'
        ax.add_patch(plt.Circle((cx, cy), radius, color='none', ec=cyan_col, lw=2))
        ax.axhline(cy, color=cyan_col, ls=':', lw=1)
        ax.axvline(cx, color=cyan_col, ls=':', lw=1)
        ax.plot([cx - radius, cx + radius], [cy - 0.15, cy + 0.15], color=cyan_col, lw=2)
        for i in range(1, 6):
            d = (radius/5) * i
            ax.annotate('', xy=(cx+d, cy+(0.15/5)*i), xytext=(cx+d, cy), 
                        arrowprops=dict(arrowstyle='->', color=cyan_col, lw=1))
            ax.annotate('', xy=(cx-d, cy-(0.15/5)*i), xytext=(cx-d, cy), 
                        arrowprops=dict(arrowstyle='->', color=cyan_col, lw=1))
        ax.text(cx + radius + 0.02, cy + 0.15, r'$\tau_{max}$', color=cyan_col, fontsize=12)
        ax.text(cx, cy - radius - 0.1, 'd = 2r', color=cyan_col, ha='center', fontsize=10)
        ax.text(0.05, 0.95, f"τ_max = {stress:.2f} MPa", transform=ax.transAxes, 
                color=cyan_col, fontweight='bold', fontsize=10)
        ax.set_title("SM_3: Torsional Stress Distribution", fontsize=9)
        ax.set_aspect('equal'); ax.axis('off')
        return save_to_buffer(fig)

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

    elif lec_id == "SM_7":
        p_val = params.get('P', 22)
        pos = np.clip(params.get('L_pos', 500) / 1000, 0.05, 1.0)
        L = 1.0
        x = np.linspace(0, L, 500)
        fig, (ax_beam, ax_defl) = plt.subplots(2, 1, figsize=(4, 6), dpi=150)
        ax_beam.axhline(0, color='grey', lw=8) 
        ax_beam.axvline(0, color='black', lw=10)
        ax_beam.annotate('', xy=(pos, 0), xytext=(pos, 0.3), 
                         arrowprops=dict(arrowstyle='->', color='red', lw=2))
        ax_beam.text(pos, 0.35, f"P={p_val}kN", color='red', ha='center', fontweight='bold')
        ax_beam.set_title("Cantilever Beam: Load Application", fontsize=9)
        ax_beam.set_xlim(-0.1, 1.1); ax_beam.set_ylim(-0.2, 0.5); ax_beam.axis('off')
        defl_curve = np.where(x <= pos, 
                              -(p_val * x**2 * (3*pos - x)), 
                              -(p_val * pos**2 * (3*x - pos)))
        ax_defl.plot(x, defl_curve, color='blue', lw=2, ls='--')
        ax_defl.axhline(0, color='grey', alpha=0.3)
        ax_defl.axvline(0, color='black', lw=4) 
        ax_defl.set_title("Relative Deflection Curve", fontsize=9)
        ax_defl.set_xlim(-0.1, 1.1); ax_defl.axis('off')
        plt.tight_layout(); return save_to_buffer(fig)

    # FINAL REVISION: SM_8 with correct Normal Surface Projections and Complementary Shear
    elif lec_id == "SM_8":
        sig_x = params.get('P', 0)
        sig_y = params.get('sigma_y', 0)
        tau_xy = params.get('A', 0) / 5
        
        center = (sig_x + sig_y) / 2
        radius = np.sqrt(((sig_x - sig_y) / 2)**2 + tau_xy**2)
        if radius == 0: radius = 0.001

        sig_1 = center + radius
        sig_2 = center - radius
        tau_max = radius
        theta_p_rad = 0.5 * np.arctan2(2 * tau_xy, sig_x - sig_y)
        theta_p_deg = np.degrees(theta_p_rad)
        theta_s_deg = theta_p_deg - 45 

        fig, axs = plt.subplots(2, 2, figsize=(6, 6), dpi=150)
        
        def draw_rotated_element(ax, angle_deg, title, s_x, s_y=0, t_xy=0, mode='normal'):
            ax.set_aspect('equal')
            ax.set_xlim(-1, 1); ax.set_ylim(-1, 1)
            tr = mtransforms.Affine2D().rotate_deg_around(0, 0, angle_deg) + ax.transData
            
            # Element Square
            color = 'green' if (s_x >= 0 and mode != 'shear') else 'red'
            if mode == 'shear': color = 'orange'
            rect = plt.Rectangle((-0.3, -0.3), 0.6, 0.6, fill=False, lw=2, color=color)
            rect.set_transform(tr)
            ax.add_patch(rect)
            
            # Normal Arrows (Projecting Normal to surface faces)
            if mode != 'shear':
                # Sigma X faces (Right & Left)
                # Right
                ax.annotate('', xy=(0.5 if s_x >=0 else 0.3, 0), xytext=(0.3 if s_x>=0 else 0.5, 0),
                            arrowprops=dict(arrowstyle='->' if s_x>=0 else '<-', color='blue', lw=1.5), transform=tr)
                ax.text(0.55 if s_x >=0 else 0.25, 0.05, f'{s_x:.0f}', transform=tr, fontsize=7, color='blue', fontweight='bold')
                
                # Sigma Y faces (Top & Bottom)
                # Top
                ax.annotate('', xy=(0, 0.5 if s_y >=0 else 0.3), xytext=(0, 0.3 if s_y>=0 else 0.5),
                            arrowprops=dict(arrowstyle='->' if s_y>=0 else '<-', color='purple', lw=1.5), transform=tr)
                ax.text(0.05, 0.55 if s_y >=0 else 0.25, f'{s_y:.0f}', transform=tr, fontsize=7, color='purple', fontweight='bold')

            # Complementary Shear Arrows (For Original and Max Shear)
            if (t_xy != 0 or mode == 'shear'):
                val = t_xy if mode != 'shear' else tau_max
                # Right face shear (y-direction)
                ax.annotate('', xy=(0.3, 0.25 if val >=0 else -0.25), xytext=(0.3, -0.25 if val >=0 else 0.25),
                            arrowprops=dict(arrowstyle='->', color='orange', lw=1.5), transform=tr)
                
                # Top face shear (x-direction, complementary to right face for equilibrium)
                # If Right face shear is (+), Top face must be (-) to maintain zero moment
                ax.annotate('', xy=(-0.25 if val >=0 else 0.25, 0.3), xytext=(0.25 if val >=0 else -0.25, 0.3),
                            arrowprops=dict(arrowstyle='->', color='orange', lw=1.5), transform=tr)
                
                ax.text(0.4, 0, f'{val:.0f}', transform=tr, fontsize=7, color='orange')

            ax.set_title(f"{title}\nθ = {angle_deg:.1f}°", fontsize=8)
            ax.axis('off')

        # Mohr's Circle
        ax_mohr = axs[1, 0]
        c = plt.Circle((center, 0), radius, fill=False, color='red', lw=1.5)
        ax_mohr.add_patch(c)
        ax_mohr.axhline(0, color='black', lw=0.8); ax_mohr.axvline(0, color='black', lw=0.8)
        ax_mohr.plot([sig_x, sig_y], [tau_xy, -tau_xy], 'ko--', ms=4)
        lim = radius * 2.5
        ax_mohr.set_xlim(center - lim/2, center + lim/2); ax_mohr.set_ylim(-lim/2, lim/2)
        ax_mohr.set_title("Mohr's Circle", fontsize=8)

        draw_rotated_element(axs[0, 0], 0, "Original Element", sig_x, sig_y, tau_xy)
        draw_rotated_element(axs[0, 1], theta_p_deg, "Principal Element", sig_1, sig_2, 0)
        draw_rotated_element(axs[1, 1], theta_s_deg, "Max Shear Element", 0, 0, mode='shear')

        plt.tight_layout(); return save_to_buffer(fig)

    return save_to_buffer(plt.figure(figsize=(3,3)))

def render_problem_diagram(prob):
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.text(0.5, 0.5, f"ID: {prob.get('id', 'N/A')}", ha='center'); ax.axis('off')
    return save_to_buffer(fig)

def save_to_buffer(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf
