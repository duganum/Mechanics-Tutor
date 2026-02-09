import matplotlib.pyplot as plt
import numpy as np
import os
import io

def render_problem_diagram(prob):
    # ... (Keep your existing procedural and image loader code here) ...
    pass

def render_lecture_visual(topic, params=None):
    """Visualizes derivation components with dynamic updates. Reduced size by 50%."""
    # Reduced figsize from (6, 6) to (3, 3) to satisfy the 50% size reduction request
    fig, ax = plt.subplots(figsize=(3, 3), dpi=150)
    if params is None: params = {}
    
    # Grid and Origin Settings
    ax.axhline(0, color='black', lw=1.0, zorder=2)
    ax.axvline(0, color='black', lw=1.0, zorder=2)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # --- 1. Topic: Design Properties of Materials (NEW LOGIC) ---
    if topic == "Design Properties of Materials":
        # Generate a standard stress-strain curve
        # Elastic: linear; Plastic: power law
        strain_elastic = np.linspace(0, 0.05, 50)
        stress_elastic = 4000 * strain_elastic 
        strain_plastic = np.linspace(0.05, 0.5, 100)
        stress_plastic = 200 + 100 * np.sqrt(strain_plastic - 0.05)
        
        strain = np.concatenate([strain_elastic, strain_plastic])
        stress = np.concatenate([stress_elastic, stress_plastic])
        
        ax.plot(strain, stress, 'b-', lw=1.5, label="Material Property")
        
        # Calculate current state from sliders
        p_val = params.get('P', 22)
        a_val = params.get('A', 817)
        curr_stress = (p_val * 1000) / a_val # MPa
        
        # Approximate strain calculation
        if curr_stress <= 200:
            curr_strain = curr_stress / 4000
        else:
            curr_strain = 0.05 + ((curr_stress - 200) / 100)**2
            
        # Plot the dynamic point representing current load
        ax.scatter(curr_strain, curr_stress, color='red', s=50, zorder=5)
        ax.annotate(f'σ={curr_stress:.1f}', xy=(curr_strain, curr_stress), 
                    xytext=(5, 5), textcoords='offset points', color='red', 
                    weight='bold', fontsize=8)

        ax.set_xlabel("Strain (ε)", fontsize=8)
        ax.set_ylabel("Stress (σ) [MPa]", fontsize=8)
        ax.set_title("Stress-Strain Curve", fontsize=9)
        ax.tick_params(labelsize=7)
        ax.set_xlim(0, 0.6)
        ax.set_ylim(0, 400)

    # --- 2. Topic: Direct Stress, Deformation, and Design ---
    elif topic == "Direct Stress, Deformation, and Design":
        ax.axis('off')
        rect = plt.Rectangle((-0.8, -0.4), 1.6, 0.8, linewidth=1.5, edgecolor='black', facecolor='#d3d3d3')
        ax.add_patch(rect)
        
        p_val = params.get('P', 22)
        a_val = params.get('A', 817)
        stress_val = round((p_val * 1000) / a_val, 2)
        
        ax.annotate('', xy=(1.2, 0), xytext=(0.8, 0), arrowprops=dict(arrowstyle='->', color='red', lw=2))
        ax.text(0, 0, f"$\\sigma = P/A$\n{stress_val} MPa", 
                fontsize=10, ha='center', va='center', fontweight='bold')
        ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)

    # --- 3. Existing Kinematics Topics ---
    elif topic == "Relative Motion":
        vA, vB = params.get('vA', [15, 5]), params.get('vB', [10, -5])
        ax.quiver(0, 0, vA[0], vA[1], color='blue', angles='xy', scale_units='xy', scale=1)
        ax.quiver(0, 0, vB[0], vB[1], color='red', angles='xy', scale_units='xy', scale=1)
        ax.set_xlim(-20, 20); ax.set_ylim(-20, 20)

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf
