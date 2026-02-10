import matplotlib.pyplot as plt
import numpy as np
import io

def render_lecture_visual(topic, params=None):
    """Visualizes derivation components with dynamic updates. Reduced size by 50%."""
    fig, ax = plt.subplots(figsize=(3, 3), dpi=150)
    if params is None: params = {}
    
    # --- Topic 1: Design Properties of Materials ---
    if topic == "Design Properties of Materials":
        strain_elastic = np.linspace(0, 0.05, 50)
        stress_elastic = 4000 * strain_elastic 
        strain_plastic = np.linspace(0.05, 0.5, 100)
        stress_plastic = 200 + 100 * np.sqrt(strain_plastic - 0.05)
        strain = np.concatenate([strain_elastic, strain_plastic])
        stress = np.concatenate([stress_elastic, stress_plastic])
        ax.plot(strain, stress, 'b-', lw=1.5)
        
        p_val = params.get('P', 22)
        a_val = params.get('A', 817)
        curr_stress = (p_val * 1000) / a_val
        curr_strain = curr_stress / 4000 if curr_stress <= 200 else 0.05 + ((curr_stress - 200) / 100)**2
        ax.scatter(curr_strain, curr_stress, color='red', s=50, zorder=5)
        ax.set_title("Stress-Strain Curve", fontsize=9)
        ax.set_xlim(0, 0.6); ax.set_ylim(0, 400)

    # --- Topic 2: Direct Stress ---
    elif topic == "Direct Stress, Deformation, and Design":
        p_val = params.get('P', 22)
        ax.add_patch(plt.Rectangle((0.35, 0.2), 0.3, 0.6, color='skyblue', alpha=0.6, ec='black'))
        ax.annotate('', xy=(0.5, 0.95), xytext=(0.5, 0.8), arrowprops=dict(arrowstyle='->', lw=2, color='red'))
        ax.text(0.5, 0.98, f'P = {p_val} kN', ha='center', color='red', fontsize=8, weight='bold')
        ax.set_xlim(0, 1); ax.set_ylim(0, 1.1); ax.axis('off')

    # --- Topic 3: Torsional Shear ---
    elif "Torsional" in topic:
        t_val = params.get('P', 22)
        circle = plt.Circle((0.5, 0.5), 0.35, color='lightgray', ec='black', lw=2)
        ax.add_patch(circle)
        ax.text(0.5, 0.5, f"T = {t_val} kN-m", ha='center', va='center', fontsize=8)
        ax.set_title("Torsional Shear Analysis", fontsize=9)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

    # --- NEW Topic 4: Shearing Forces and Bending Moments ---
    elif "Shearing Forces" in topic:
        # P = Load Magnitude, A = Load Position (mapped 0-1)
        p_val = params.get('P', 22)
        pos = (params.get('A', 400) / 817) # Normalize slider A to beam length
        
        x = np.linspace(0, 1, 100)
        # Simple support reactions for a point load P at position 'pos'
        r2 = p_val * pos
        r1 = p_val - r2
        
        # Shear Force V(x)
        v_x = np.where(x < pos, r1, -r2)
        ax.fill_between(x, v_x, color='orange', alpha=0.3, label='Shear (V)')
        ax.plot(x, v_x, color='darkorange', lw=1.5)
        
        # Add a visual of the beam and load
        ax.axhline(0, color='black', lw=2) # The Beam
        ax.annotate('', xy=(pos, 0), xytext=(pos, p_val/2), 
                    arrowprops=dict(arrowstyle='->', color='red', lw=2))
        ax.text(pos, p_val/2 + 2, f'{p_val}kN', color='red', ha='center', fontsize=7, weight='bold')
        
        ax.set_title("Shear Force Diagram (SFD)", fontsize=9)
        ax.set_xlabel("Beam Length", fontsize=7)
        ax.set_ylabel("Force (kN)", fontsize=7)
        ax.grid(True, linestyle=':', alpha=0.5)

    # --- Default Case ---
    else:
        ax.text(0.5, 0.5, f"Visualizing:\n{topic}", ha='center', va='center', fontsize=8)
        ax.axis('off')

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf
