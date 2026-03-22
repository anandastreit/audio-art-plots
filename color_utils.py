import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches


def show_cmap(name, n=20):
    """Visual strip showing a colormap with sampled values labeled."""
    cmap = plt.get_cmap(name) if isinstance(name, str) else name
    fig, ax = plt.subplots(figsize=(10, 1))
    for i, v in enumerate(np.linspace(0, 1, n)):
        ax.add_patch(mpatches.Rectangle([i / n, 0], 1 / n, 1, color=cmap(v)))
        ax.text(i / n + 0.5 / n, 0.5, f'{v:.2f}', fontsize=7, ha='center')
    ax.set_xlim(0, 1)
    ax.axis('off')


def trim_cmap(name, minval=0.0, maxval=1.0):
    """Slice a colormap to only use colors between minval and maxval."""
    cmap = plt.get_cmap(name) if isinstance(name, str) else name
    label = cmap.name if hasattr(cmap, 'name') else 'cmap'
    return LinearSegmentedColormap.from_list(
        f'{label}_trim', cmap(np.linspace(minval, maxval, 256))
    )


def blend_cmap(base, overlay, start=0.8, overlay_range=(0.6, 0.9)):
    """Replace the top portion of base colormap with colors from overlay.

    start         - where the overlay begins in the base (0.0 to 1.0)
    overlay_range - which part of the overlay colormap to use
    """
    base_cmap = plt.get_cmap(base) if isinstance(base, str) else base
    overlay_cmap = plt.get_cmap(overlay) if isinstance(overlay, str) else overlay

    colors = base_cmap(np.linspace(0, 1, 256))
    n = int((1 - start) * 256)
    colors[-n:] = overlay_cmap(np.linspace(*overlay_range, n))

    base_label = base if isinstance(base, str) else 'cmap'
    overlay_label = overlay if isinstance(overlay, str) else 'overlay'
    return LinearSegmentedColormap.from_list(f'{base_label}_{overlay_label}_blend', colors)
