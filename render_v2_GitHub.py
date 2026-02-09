import matplotlib.pyplot as plt
import numpy as np
import io

def render_lecture_visual(topic, params=None):
    """Visualizes derivation components with dynamic updates. Reduced size by 50%."""
    # Reduced figsize from (6, 6) to (3, 3) for a 50% smaller footprint
    fig, ax = plt.subplots(figsize=(3, 3), dpi=150)
    if params is None: params = {}
    
    ax.axhline(0, color='black', lw=1.0, zorder=2)
    ax.axvline(0, color='black', lw=1.0, zorder=2)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Topic: Design Properties of Materials
    if topic == "Design Properties of Materials":
        # Generate standard stress-strain curve data
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
        
        # Approximate current strain
        curr_strain = curr_stress / 4000 if curr_stress <= 200 else 0.05 + ((curr_stress - 200) / 100)**2
            
        # Plot dynamic point
        ax.scatter(curr_strain, curr_stress, color='red', s=50, zorder=5)
        ax.annotate(f'σ={curr_stress:.1f}', xy=(curr_strain, curr_stress), 
                    xytext=(5, 5), textcoords='offset points', color='red', fontsize=8, weight='bold')

        ax.set_xlabel("Strain (ε)", fontsize=8)
        ax.set_ylabel("Stress (σ) [MPa]", fontsize=8)
        ax.set_title("Stress-Strain Curve", fontsize=9)
        ax.set_xlim(0, 0.6); ax.set_ylim(0, 400)

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf
