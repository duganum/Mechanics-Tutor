import matplotlib.pyplot as plt
import numpy as np
import os
import io

def render_problem_diagram(prob):
    """
    Generates procedural FBDs or loads images from the local repository.
    Path: images/HW Title (HW Subtitle)/[ID_number].png
    """
    if isinstance(prob, dict):
        pid = str(prob.get('id', '')).strip()
    else:
        pid = str(prob).strip()
        prob = {}

    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    ax.set_aspect('equal')
    found = False

    # --- 1. HW Directory Image Loader ---
    hw_title = prob.get("hw_title")
    hw_subtitle = prob.get("hw_subtitle")
    
    if hw_title and hw_subtitle:
        # Construct path based on your folder structure: images/HW 6 (subtitle)/1.png
        folder_name = f"{hw_title} ({hw_subtitle})"
        image_num = pid.split('_')[-1]
        img_path = os.path.join('images', folder_name, f"{image_num}.png")
        
        try:
            if os.path.exists(img_path):
                img = plt.imread(img_path)
                ax.imshow(img)
                h, w = img.shape[:2]
                ax.set_xlim(0, w); ax.set_ylim(h, 0)
                found = True
        except Exception:
            pass

    # --- 2. Procedural Fallbacks (Strength of Materials visuals) ---
    if not found:
        if "SM_2" in pid: # Axial Loading
            ax.add_patch(plt.Rectangle((1, 0.4), 3, 0.2, color='gray', alpha=0.7))
            ax.annotate('', xy=(4.5, 0.5), xytext=(4, 0.5), arrowprops=dict(arrowstyle='->', color='red'))
            ax.text(4.6, 0.5, "P", color='red')
            ax.set_xlim(0, 6); ax.set_ylim(0, 1)
            found = True
        else:
            # Generic placeholder if no image or specific logic exists
            ax.text(0.5, 0.5, f"Diagram: {pid}", color='blue', ha='center', va='center')
            ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    ax.axis('off')
    buf = io.BytesIO()
    # Explicit bbox_inches='tight' prevents the tight_layout ValueError on Streamlit
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return buf

def render_lecture_visual(topic, params=None):
    """
    Visualizes all 8 chapters of the Strength of Materials syllabus.
    Includes explicit padding to handle Streamlit rendering errors.
    """
    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
    params = params or {}
    
    # 1. Design Properties (Stress-Strain)
    if "Design Properties" in topic:
        strain = np.linspace(0, 0.5, 100)
        stress = np.where(strain < 0.1, 200 * strain, 20 + 50 * (strain**0.5))
        ax.plot(strain, stress, 'b-', lw=2)
        ax.set_xlabel("Strain ($\epsilon$)"); ax.set_ylabel("Stress ($\sigma$)")
        ax.set_title("Stress-Strain Relationship")
        ax.grid(True, linestyle=':', alpha=0.6)

    # 2. Direct Stress & Deformation
    elif "Direct Stress" in topic:
        ax.add_patch(plt.Rectangle((1, 1), 4, 1, color='lightgrey', ec='black'))
        ax.annotate('', xy=(5.5, 1.5), xytext=(5, 1.5), arrowprops=dict(arrowstyle='->', color='red', lw=2))
        ax.text(2.5, 1.4, r"$\sigma = P/A$", fontsize=14)
        ax.set_xlim(0, 7); ax.set_ylim(0, 3)

    # 3. Torsional Shear
    elif "Torsional" in topic:
        circle = plt.Circle((0.5, 0.5), 0.4, color='gray', alpha=0.3, ec='black')
        ax.add_patch(circle)
        ax.annotate('', xy=(0.8, 0.8), xytext=(0.5, 0.5), arrowprops=dict(arrowstyle='->', color='blue'))
        ax.text(0.35, 0.45, r"$\tau = \frac{Tr}{J}$", fontsize=14)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    # 4. Shearing Forces & Bending Moments
    elif "Shearing Forces" in topic:
        ax.plot([1, 5], [1, 1], 'k-', lw=6)
        ax.plot(1, 0.8, 'k^', markersize=10) # Support
        ax.annotate('', xy=(3, 1), xytext=(3, 2), arrowprops=dict(arrowstyle='->', color='red'))
        ax.set_title("Beam Loading Diagram")
        ax.set_xlim(0, 6); ax.set_ylim(0, 3)

    # 5. Stress Due to Bending
    elif "Stress Due to Bending" in topic:
        ax.add_patch(plt.Rectangle((2, 0.5), 2, 2, color='whitesmoke', ec='black'))
        ax.axhline(1.5, ls='--', color='blue', label="Neutral Axis")
        ax.text(2.2, 2.0, r"$\sigma = -\frac{My}{I}$", fontsize=14)
        ax.set_xlim(0, 6); ax.set_ylim(0, 3)

    # 6. Shearing Stresses in Beams
    elif "Shearing Stresses" in topic:
        ax.add_patch(plt.Rectangle((2, 0.5), 2, 2, color='whitesmoke', ec='black'))
        ax.text(2.2, 1.4, r"$\tau = \frac{VQ}{Ib}$", fontsize=14)
        ax.set_xlim(0, 6); ax.set_ylim(0, 3)

    # 7. Deflection of Beams
    elif "Deflection" in topic:
        x = np.linspace(1, 5, 50)
        y = -0.05 * (x-1)*(x-5)*(x+2) 
        ax.plot(x, y + 2, 'b--', label="Deflected Shape")
        ax.plot([1, 5], [2, 2], 'k-', lw=4)
        ax.set_title("Elastic Curve Analysis")
        ax.set_xlim(0, 6); ax.set_ylim(0, 4)

    # 8. Combined Load (Mohr's Circle)
    elif "Combined" in topic:
        circle = plt.Circle((3, 0), 2, fill=False, color='purple', lw=2)
        ax.add_patch(circle)
        ax.axhline(0, color='black', lw=1); ax.axvline(3, color='black', ls=':')
        ax.set_xlabel("$\sigma$"); ax.set_ylabel("$\tau$")
        ax.set_xlim(0, 6); ax.set_ylim(-3, 3)
        ax.grid(True, linestyle=':')

    # Formatting fix: Use explicit padding and avoid standard tight_layout
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    
    buf = io.BytesIO()
    # bbox_inches='tight' is safer for Streamlit environments
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf
