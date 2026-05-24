"""
FigMirror Demo: Replicate a paper figure's visual style onto your own data.

This script:
  1. Loads a style specification extracted from a reference figure
  2. Loads the user's own data (CSV)
  3. Generates a new matplotlib figure that matches the reference style
  4. Saves both PNG and PDF outputs
"""
import json
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd


def load_style(style_path: str) -> dict:
    """Load style specification from JSON."""
    with open(style_path) as f:
        return json.load(f)


def apply_style(style: dict):
    """Apply extracted style to matplotlib rcParams."""
    typo = style["typography"]
    axes = style["axes"]
    layout = style["layout"]

    mpl.rcParams.update({
        'font.family': typo["font_family"],
        'font.size': typo["tick_label_size"],
        'axes.linewidth': axes["spine_width"],
        'axes.grid': axes["grid"],
        'grid.alpha': axes["grid_alpha"],
        'grid.linestyle': axes["grid_linestyle"],
        'figure.facecolor': style["colors"]["background"],
        'axes.facecolor': style["colors"]["background"],
        'figure.dpi': layout["dpi"],
    })


def generate_figure(data: pd.DataFrame, style: dict, output_prefix: str):
    """Generate a figure from user data using the extracted style."""
    colors_map = style["colors"]
    typo = style["typography"]
    line_cfg = style["lines"]
    legend_cfg = style["legend"]
    layout = style["layout"]

    color_list = [colors_map["line1"], colors_map["line2"],
                  colors_map["line3"], colors_map["line4"]]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(layout["figsize"][0] * 1.8,
                                                    layout["figsize"][1]))

    x = data["epoch"]

    # --- Left panel: Loss curves ---
    for i, col in enumerate(["train_loss", "val_loss"]):
        label = col.replace("_", " ").title()
        ax1.plot(x, data[col],
                 color=color_list[i],
                 marker=line_cfg["markers"][i],
                 markersize=line_cfg["marker_size"],
                 linewidth=line_cfg["linewidth"],
                 linestyle=line_cfg["linestyles"][i],
                 label=label)

    ax1.set_xlabel('Epoch', fontsize=typo["axis_label_size"])
    ax1.set_ylabel('Loss', fontsize=typo["axis_label_size"])
    ax1.set_title('Training & Validation Loss',
                  fontsize=typo["title_size"],
                  fontweight=typo["title_weight"])
    ax1.legend(frameon=legend_cfg["frameon"],
               framealpha=legend_cfg["frame_alpha"],
               fontsize=typo["legend_size"],
               loc=legend_cfg["position"])

    # --- Right panel: Accuracy curves ---
    for i, col in enumerate(["train_acc", "val_acc"]):
        label = col.replace("_", " ").title()
        ax2.plot(x, data[col] * 100,
                 color=color_list[i + 2],
                 marker=line_cfg["markers"][i + 2],
                 markersize=line_cfg["marker_size"],
                 linewidth=line_cfg["linewidth"],
                 linestyle=line_cfg["linestyles"][i + 2],
                 label=label)

    ax2.set_xlabel('Epoch', fontsize=typo["axis_label_size"])
    ax2.set_ylabel('Accuracy (%)', fontsize=typo["axis_label_size"])
    ax2.set_title('Training & Validation Accuracy',
                  fontsize=typo["title_size"],
                  fontweight=typo["title_weight"])
    ax2.legend(frameon=legend_cfg["frameon"],
               framealpha=legend_cfg["frame_alpha"],
               fontsize=typo["legend_size"],
               loc=legend_cfg["position"])

    plt.tight_layout()

    png_path = f"{output_prefix}.png"
    pdf_path = f"{output_prefix}.pdf"
    plt.savefig(png_path, dpi=300, bbox_inches='tight',
                facecolor=colors_map["background"])
    plt.savefig(pdf_path, bbox_inches='tight',
                facecolor=colors_map["background"])

    print(f"[OK] {png_path} saved (300 DPI)")
    print(f"[OK] {pdf_path} saved (vector)")
    return png_path, pdf_path


def compare_summary(style: dict):
    """Print a summary of the style attributes being replicated."""
    print("\n--- Style Attributes Replicated ---")
    print(f"  Chart type:    {style['chart_type']}")
    print(f"  Font family:   {style['typography']['font_family']}")
    print(f"  Color palette: {style['colors']['line1']}, {style['colors']['line2']}, "
          f"{style['colors']['line3']}, {style['colors']['line4']}")
    print(f"  Line width:    {style['lines']['linewidth']}pt")
    print(f"  Markers:       {', '.join(style['lines']['markers'])}")
    print(f"  Grid:          {'on' if style['axes']['grid'] else 'off'} "
          f"(alpha={style['axes']['grid_alpha']})")
    print(f"  Background:    {style['colors']['background']}")
    print(f"  Legend:         framed={style['legend']['frameon']}, "
          f"cols={style['legend']['ncol']}")
    print("-----------------------------------\n")


def main():
    style_path = sys.argv[1] if len(sys.argv) > 1 else "reference_style.json"
    data_path = sys.argv[2] if len(sys.argv) > 2 else "sample_data.csv"
    output_prefix = sys.argv[3] if len(sys.argv) > 3 else "output_figure"

    print("FigMirror Demo")
    print("==============")
    print(f"Style source:  {style_path}")
    print(f"Data source:   {data_path}")
    print(f"Output prefix: {output_prefix}")

    style = load_style(style_path)
    compare_summary(style)

    apply_style(style)

    data = pd.read_csv(data_path)
    print(f"Loaded {len(data)} data points with columns: {list(data.columns)}")

    generate_figure(data, style, output_prefix)

    print("\nDone! Compare output_figure.png side-by-side with reference_figure.png")
    print("to verify the style was replicated faithfully.")


if __name__ == "__main__":
    main()
