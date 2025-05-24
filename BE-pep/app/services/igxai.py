import tensorflow as tf
import numpy as np

def interpolate_inputs(baseline, input, alphas):
    return baseline + alphas * (input - baseline)

def compute_integrated_gradients(model, input_tensor, baseline=None, steps=50):
    if baseline is None:
        baseline = tf.zeros_like(input_tensor)
    alphas = tf.linspace(0.0, 1.0, steps+1)
    alphas_x = tf.reshape(alphas, (-1, 1, 1))
    interpolated_inputs = interpolate_inputs(baseline, input_tensor, alphas_x)
    with tf.GradientTape() as tape:
        tape.watch(interpolated_inputs)
        predictions = model(interpolated_inputs)
    grads = tape.gradient(predictions, interpolated_inputs)
    avg_grads = tf.reduce_mean(grads, axis=0)
    ig = (input_tensor - baseline) * avg_grads
    return ig.numpy()

def explain_ig_top_k(ig_matrix, k=3):
    property_names = [
        "hydrophobicity", "vdw_volume", "polarity",
        "polarizability", "charge", "secondary_structure", "solvent_accessibility"
    ]
    property_groups = {
        "hydrophobicity": ["polar", "neutral", "hydrophobic"],
        "vdw_volume": ["small", "medium", "large"],
        "polarity": ["polar", "neutral", "nonpolar"],
        "polarizability": ["low", "medium", "high"],
        "charge": ["negative", "neutral", "positive"],
        "secondary_structure": ["helix", "sheet", "coil"],
        "solvent_accessibility": ["buried", "intermediate", "exposed"]
    }
    results = []
    ig_copy = np.abs(ig_matrix.copy())
    for _ in range(k):
        if np.max(ig_copy) == 0:
            break  
        timestep, feature_idx = np.unravel_index(np.argmax(ig_copy), ig_copy.shape)
        prop = property_names[timestep]
        group_idx = feature_idx // 6
        pos_idx = feature_idx % 6
        percentile = int(pos_idx * 20)
        results.append({
            "property": prop,
            "group": property_groups[prop][group_idx],
            "position_percentile": f"{percentile}%",
            "ig_value": float(ig_matrix[timestep, feature_idx])
        })
        ig_copy[timestep, feature_idx] = 0 
    return results  


#Vẽ biểu đồ IG
def draw_ig_highlight_full(sequence, top_features, figsize_scale=0.5):
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    property_groups = {
        "hydrophobicity": {"polar": "RKEDQN", "neutral": "GASTPHY", "hydrophobic": "CLVIMFW"},
        "vdw_volume": {"small": "GASTPDC", "medium": "NVEQIL", "large": "MHKFRYW"},
        "polarity": {"polar": "EDQNKR", "neutral": "GASTPHY", "nonpolar": "CLVIMFW"},
        "polarizability": {"low": "GASDT", "medium": "CPNVEQIL", "high": "KMHFRYW"},
        "charge": {"negative": "DE", "neutral": "ACFGHILMNPQSTVWY", "positive": "KR"},
        "secondary_structure": {"helix": "EALMQKRH", "sheet": "VIYCWT", "coil": "GNPSD"},
        "solvent_accessibility": {"buried": "ALFCGIVW", "intermediate": "MPSTHY", "exposed": "DEKNQR"}
    }
    base_colors = ['#c6dbef', '#fbb4ae', '#b2df8a', '#ffffcc', '#d9d9d9']
    fig, axes = plt.subplots(
        len(top_features), 1,
        figsize=(len(sequence) * figsize_scale, 1.2 * len(top_features)),
        gridspec_kw={'hspace': 0.1} 
    )
    if len(top_features) == 1:
        axes = [axes]
    for idx, (feature, ax) in enumerate(zip(top_features, axes)):
        prop = feature["property"]
        group = feature["group"]
        perc = int(feature["position_percentile"].replace("%", ""))
        aa_group = property_groups[prop][group]
        base_color = base_colors[idx % len(base_colors)]
        highlight = ['lightgray'] * len(sequence)
        positions = [i for i, aa in enumerate(sequence) if aa in aa_group]
        for pos in positions:
            highlight[pos] = base_color
        if positions:
            target_idx = int(np.floor(len(positions) * (perc / 100)))
            target_idx = min(target_idx, len(positions) - 1)
            final_pos = positions[target_idx]
            highlight[final_pos] = '#FFD700'
        title_str = f"{prop} - {group} at {feature['position_percentile']} — IG: {feature['ig_value']:.4f}"
        ax.text(len(sequence) / 2, -1.3, title_str,
                ha='center', va='center', fontsize=11, weight='bold')
        for i, aa in enumerate(sequence):
            facecolor = highlight[i]
            ax.text(i, 0, aa, ha='center', va='center', fontsize=12,
                    bbox=dict(boxstyle="round,pad=0.25", facecolor=facecolor, edgecolor='gray', linewidth=0.5))
        ax.set_xlim(-1, len(sequence))
        ax.set_ylim(-1.5, 1.5)
        ax.axis('off')
    plt.tight_layout(pad=0.5)
    return fig

