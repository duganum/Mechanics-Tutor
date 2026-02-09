import matplotlib.pyplot as plt
import numpy as np
import os
import io

def render_problem_diagram(prob):
    """
    Generates procedural FBDs for Statics or loads external images for Dynamics.
    """
    if isinstance(prob, dict):
        pid = str(prob.get('id', '')).strip()
    else:
        pid = str(prob).strip()
        prob = {}

    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    ax.set_aspect('equal')
    found = False

    # --- 1. Procedural Statics Diagrams ---
    if pid.startswith("S_1.1"):
        if pid == "S_1.1_1":
            ax.plot(0, 0, 'ko', markersize=8)
            ax.annotate('', xy=(-1.5, 0), xytext=(0, 0), arrowprops=dict(arrowstyle='<-', color='blue'))
            ax.annotate('', xy=(1.2, 1.2), xytext=(0, 0), arrowprops=dict(arrowstyle='<-', color='green'))
            ax.annotate('', xy=(0, -1.5), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='red'))
            ax.text(-1.4, 0.2, '$T_A$', color='blue'); ax.text(1.0, 1.3, '$T_B (45^\circ)$', color='green')
            ax.set_xlim(-2, 2); ax.set_ylim(-2, 2)
            found = True
        elif pid == "S_1.1_2":
            theta = np.radians(30)
            ax.plot([-2, 2], [2*np.tan(-theta), -2*np.tan(-theta)], 'k-', lw=2) 
            ax.add_patch(plt.Circle((0, 0.5), 0.5, color='gray', alpha=0.5)) 
            ax.annotate('', xy=(0.5*np.sin(theta), 0.5+0.5*np.cos(theta)), xytext=(0, 0.5), 
                        arrowprops=dict(arrowstyle='->', color='red')) 
            ax.set_xlim(-2, 2); ax.set_ylim(-1, 2)
            found = True

    # --- 2. HW Directory Image Loader ---
    if not found:
        hw_title = prob.get("hw_title")
        hw_subtitle = prob.get("hw_subtitle")
        if hw_title and hw_subtitle:
            folder_name = f"HW 7  ({hw_subtitle})" if hw_title == "HW 7" else f"{hw_title} ({hw_subtitle})"
            image_filename = f"{pid.split('_')[-1]}.png"
            img_path = os.path.join('images', folder_name, 'images', image_filename)
            try:
                if os.path.exists(img_path):
                    img = plt.imread(img_path)
                    ax.imshow(img)
                    h, w = img.shape[:2]
                    ax.set_xlim(0, w); ax.set_ylim(h, 0)
                    found = True
            except Exception: pass

    if not found:
        ax.text(0.5, 0.5, f"Diagram Not Found\nID: {pid}", color='red', ha='center', va='center')
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    ax.axis('off')
    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf

def render_lecture_visual(topic, params=None):
    """Visualizes derivation components with dynamic updates from sliders."""
    fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
    if params is None: params = {}
    
    # Grid and Origin Settings
    ax.axhline(0, color='black', lw=1.5, zorder=2)
    ax.axvline(0, color='black', lw=1.5, zorder=2)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # --- 1. Topic: Design Properties of Materials ---
    if topic == "Design Properties of Materials":
        # Generate a standard stress-strain curve
        strain_elastic = np.linspace(0, 0.05, 50)
        stress_elastic = 4000 * strain_elastic 
        strain_plastic = np.linspace(0.05, 0.5, 100)
        stress_plastic = 200 + 100 * np.sqrt(strain_plastic - 0.05)
        
        strain = np.concatenate([strain_elastic, strain_plastic])
        stress = np.concatenate([stress_elastic, stress_plastic])
        
        ax.plot(strain, stress, 'b-', lw=2, label="Material Property")
        
        p_val = params.get('P', 22)
        a_val = params.get('A', 817)
        curr_stress = (p_val * 1000) / a_val # MPa
        curr_strain = curr_stress/4000 if curr_stress <= 200 else 0.05 + ((curr_stress-200)/100)**2
            
        ax.scatter(curr_strain, curr_stress, color='red', s=100, zorder=5)
        ax.annotate(f'σ = {curr_stress:.1f} MPa', xy=(curr_strain, curr_stress), 
                    xytext=(10, 10), textcoords='offset points', color='red', weight='bold')

        ax.set_xlabel("Strain (ε)"); ax.set_ylabel("Stress (σ) [MPa]")
        ax.set_title("Stress-Strain Relationship")
        ax.set_xlim(0, 0.6); ax.set_ylim(0, 400)

    # --- 2. Topic: Direct Stress, Deformation, and Design ---
    elif topic == "Direct Stress, Deformation, and Design":
        ax.axis('off')
        rect = plt.Rectangle((-1, -0.5), 2, 1, linewidth=2, edgecolor='black', facecolor='#d3d3d3')
        ax.add_patch(rect)
        
        p_val = params.get('P', 22)
        a_val = params.get('A', 817)
        stress_val = round((p_val * 1000) / a_val, 2)
        
        ax.annotate('', xy=(1.5, 0), xytext=(1, 0), arrowprops=dict(arrowstyle='->', color='red', lw=3))
        ax.text(0, 0, f"$\\sigma = P/A$\n\n$\\sigma = {stress_val}$ MPa", 
                fontsize=14, ha='center', va='center', fontweight='bold')
        ax.set_xlim(-2, 2); ax.set_ylim(-2, 2)

    # --- 3. Existing Kinematics Topics ---
    elif topic == "Relative Motion":
        vA, vB = params.get('vA', [15, 5]), params.get('vB', [10, -5])
        ax.quiver(0, 0, vA[0], vA[1], color='blue', angles='xy', scale_units='xy', scale=1, label=r'$\vec{v}_A$')
        ax.quiver(0, 0, vB[0], vB[1], color='red', angles='xy', scale_units='xy', scale=1, label=r'$\vec{v}_B$')
        ax.set_xlim(-20, 20); ax.set_ylim(-20, 20)
        ax.legend()

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf
