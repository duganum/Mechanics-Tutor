import matplotlib.pyplot as plt
import numpy as np
import os
import io

def render_problem_diagram(prob):
    """Generates precise FBDs or loads images from the HW directory structure."""
    if isinstance(prob, dict):
        pid = str(prob.get('id', '')).strip()
    else:
        pid = str(prob).strip()
        prob = {} 

    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    ax.set_aspect('equal')
    found = False

    # Procedural fallback for specific IDs
    if pid.startswith("SM"):
        ax.text(0.5, 0.5, f"Strength of Materials\nProblem {pid}", ha='center')
        found = True

    # HW Directory Image Loader
    if not found:
        hw_title = prob.get("hw_title")
        hw_subtitle = prob.get("hw_subtitle")
        if hw_title and hw_subtitle:
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
            except Exception: pass

    if not found:
        ax.text(0.5, 0.5, f"Diagram Not Found\nID: {pid}", color='red', ha='center')
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    ax.axis('off')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf

def render_lecture_visual(topic, params=None):
    """Visualizes all 8 chapters of Strength of Materials syllabus."""
    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
    if params is None: params = {}
    ax.set_title(f"Concept: {topic}", fontsize=12, pad=15)
    
    # 1. Design Properties
    if "Design Properties" in topic:
        strain = np.linspace(0, 0.5, 100)
        stress = np.where(strain < 0.1, 200 * strain, 20 + 50 * (strain**0.5))
        ax.plot(strain, stress, 'b-', lw=2)
        ax.set_xlabel("Strain ($\epsilon$)"); ax.set_ylabel("Stress ($\sigma$)")
        ax.axis('on')

    # 2. Direct Stress & Deformation
    elif "Direct Stress" in topic:
        ax.add_patch(plt.Rectangle((1, 1), 4, 1, color='lightgrey', ec='black'))
        ax.annotate('', xy=(5.5, 1.5), xytext=(5, 1.5), arrowprops=dict(arrowstyle='->', color='red'))
        ax.text(2.5, 1.2, r"$\delta = \frac{PL}{AE}$", fontsize=14)
        ax.set_xlim(0, 7); ax.set_ylim(0, 3)

    # 3. Torsional Shear
    elif "Torsional" in topic:
        ax.add_patch(plt.Circle((0.5, 0.5), 0.4, color='gray', alpha=0.3, ec='black'))
        ax.annotate('', xy=(0.8, 0.8), xytext=(0.5, 0.5), arrowprops=dict(arrowstyle='->', color='blue'))
        ax.text(0.4, 0.4, r"$\tau = \frac{Tr}{J}$", fontsize=14)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    # 4. Shearing Forces & Bending Moments
    elif "Shearing Force" in topic:
        ax.plot([1, 5], [1, 1], 'k-', lw=6)
        ax.plot([1, 1], [1, 2], 'r-') # Load
        ax.text(1, 2.1, "Shear (V) & Moment (M)")
        ax.set_xlim(0, 6); ax.set_ylim(0, 3)

    # 5. Stress Due to Bending
    elif "Stress Due to Bending" in topic:
        ax.add_patch(plt.Rectangle((2, 0.5), 2, 2, color='whitesmoke', ec='black'))
        ax.axhline(1.5, ls='--', color='blue') # Neutral Axis
        ax.text(4.2, 1.5, "N.A.")
        ax.text(2.2, 2.0, r"$\sigma = -\frac{My}{I}$", fontsize=14)
        ax.set_xlim(0, 6); ax.set_ylim(0, 3)

    # 6. Shearing Stresses in Beams
    elif "Shearing Stresses" in topic:
        ax.add_patch(plt.Rectangle((2, 0.5), 2, 2, color='whitesmoke', ec='black'))
        ax.text(2.2, 1.5, r"$\tau = \frac{VQ}{Ib}$", fontsize=14)
        ax.set_xlim(0, 6); ax.set_ylim(0, 3)

    # 7. Deflection of Beams
    elif "Deflection" in topic:
        x = np.linspace(1, 5, 50)
        y = -0.1 * (x-1)*(x-5)*(x**2 + x*1 + 1) # General elastic curve shape
        ax.plot(x, y + 2, 'b--', label="Elastic Curve")
        ax.plot([1, 5], [2, 2], 'k-', lw=4)
        ax.set_xlim(0, 6); ax.set_ylim(0, 4)

    # 8. Combined Load
    elif "Combined" in topic:
        # Mohr's Circle visualization
        circle = plt.Circle((3, 0), 2, fill=False, color='purple', lw=2)
        ax.add_patch(circle)
        ax.axhline(0, color='black'); ax.axvline(3, color='black', ls=':')
        ax.set_xlabel("$\sigma$"); ax.set_ylabel("$\tau$")
        ax.set_title("Combined Loading: Mohr's Circle")
        ax.set_xlim(0, 6); ax.set_ylim(-3, 3)
        ax.axis('on')

    if ax.get_xlabel() == "": ax.axis('off')
    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf
