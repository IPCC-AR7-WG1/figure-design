from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

ROOT = Path(__file__).parent

cmaps_dir = ROOT / "continuous_colormaps_rgb_0-1"
cmaps_path = {p.name: p for p in cmaps_dir.glob("*.txt")}
cmaps = [("Sequential", [name for name in cmaps_path.keys() if "seq" in name]),
         ("Diverging", [name for name in cmaps_path.keys() if "div" in name])]

gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))



# Function to create a colormap from a AR6 text file containing RGB values
def create_colormap_from_txt(filepath, cmap_name="custom_colormap"):
    """
    Read RGB values from a text file and create a LinearSegmentedColormap.
    RGB value shoud be 0-1 range.
    """
    rgb_data = np.loadtxt(filepath)
    colormap = mcolors.LinearSegmentedColormap.from_list(cmap_name, rgb_data)
    return colormap


def plot_color_gradients(cmap_category, cmap_list):
    # Create figure and adjust figure height to number of colormaps
    nrows = len(cmap_list)
    figh = 0.35 + 0.15 + (nrows + (nrows-1)*0.1)*0.22
    fig, axs = plt.subplots(nrows=nrows, figsize=(6.4, figh))
    fig.subplots_adjust(top=1-.35/figh, bottom=.15/figh, left=0.2, right=0.99)

    axs[0].set_title(f"{cmap_category} colormaps", fontsize=14)

    for ax, cmap_name in zip(axs, cmap_list):
        colormap = create_colormap_from_txt(cmaps_path[cmap_name], cmap_name)
        ax.imshow(gradient, aspect='auto', cmap=colormap)
        ax.text(-.01, .5, cmap_name.split(".")[0], va='center', ha='right', fontsize=10,
                transform=ax.transAxes)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axs:
        ax.set_axis_off()

    return fig

def save_colormap_figures():
    for cmap_category, cmap_list in cmaps:
        fig = plot_color_gradients(cmap_category, cmap_list)
        fig.savefig(ROOT / f"{cmap_category}_colormaps.png", dpi=300)
