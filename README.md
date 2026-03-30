# IPCC AR7 Figure Example

This repository provides **code example for creating IPCC AR7 figures**. It is designed to help authors standardise the visual appearance of figures, including size, titles, color bars, structure, and overall formatting.

 ## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/IPCC-AR7-WG1/figure-design.git
cd figure-design
```

Install the required dependencies (e.g., matplotlib):

```bash
conda env create -f environment.yml
conda activate ipcc_figure
```

## Examples

1. Line Plot
    - `line_plot.ipynb`
    - color palette for AR5 & AR6, from pyam package
    - example line plot

2. Map Plot
    - `one_map.ipynb`
    - map with standard colormaps, title and legend.

3. Colormaps
    - The folder continuous_colormaps_rgb_0-1 contains 12 colormaps, each with 256 RGB values in the range [0, 1].
    - These colormaps are the recommended standard for IPCC AR7 figure visualisations.
    - Use the function `create_colormap_from_rgb_txt` to load an RGB file:

    ```python
    def create_colormap_from_txt(filepath, cmap_name="custom_colormap"):
        """
        Read RGB values from a text file and create a LinearSegmentedColormap.
        RGB value shoud be 0-1 range.
        """
        rgb_data = np.loadtxt(filepath)
        colormap = mcolors.LinearSegmentedColormap.from_list(cmap_name, rgb_data)
        return colormap
    ```
