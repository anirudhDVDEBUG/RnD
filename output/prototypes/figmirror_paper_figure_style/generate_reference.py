"""
Generate a reference figure in a distinctive 'paper' style.
This simulates the kind of figure you'd find in a published paper,
which FigMirror would then analyze and replicate.
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

np.random.seed(42)

# -- Distinctive "Nature-style" figure --
mpl.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.linewidth': 1.2,
    'axes.grid': True,
    'grid.alpha': 0.25,
    'grid.linestyle': '--',
    'figure.facecolor': '#fafafa',
    'axes.facecolor': '#fafafa',
    'figure.dpi': 150,
})

colors = ['#2166ac', '#b2182b', '#4dac26', '#e08214']
markers = ['o', 's', '^', 'D']

x = np.array([1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
curves = {
    'ResNet-50':    2.3 * np.exp(-0.06 * x) + 0.10 + np.random.normal(0, 0.02, len(x)),
    'ViT-B/16':    2.1 * np.exp(-0.07 * x) + 0.08 + np.random.normal(0, 0.02, len(x)),
    'EfficientNet': 2.4 * np.exp(-0.055 * x) + 0.12 + np.random.normal(0, 0.02, len(x)),
    'DenseNet-121': 2.2 * np.exp(-0.065 * x) + 0.11 + np.random.normal(0, 0.02, len(x)),
}

fig, ax = plt.subplots(figsize=(8, 5))

for i, (name, y) in enumerate(curves.items()):
    ax.plot(x, y, color=colors[i], marker=markers[i], markersize=6,
            linewidth=2.0, linestyle=['-', '--', '-', '--'][i], label=name)

ax.set_xlabel('Training Epoch', fontsize=12, fontfamily='serif')
ax.set_ylabel('Validation Loss', fontsize=12, fontfamily='serif')
ax.set_title('Convergence Comparison of Vision Models',
             fontsize=14, fontweight='bold', fontfamily='serif')
ax.legend(frameon=True, framealpha=0.8, fontsize=10, ncol=2, loc='best')
ax.set_xlim(0, 52)
ax.set_ylim(0, 2.6)

plt.tight_layout()
plt.savefig('reference_figure.png', dpi=300, bbox_inches='tight', facecolor='#fafafa')
print("[OK] reference_figure.png saved (the style we want to replicate)")
