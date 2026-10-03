from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_validation_scatter(
    validation,
    global_metrics,
    extreme_metrics,
    threshold=2.5,
    output_path=None,
):
    """
    Create side-by-side scatter plots for global
    and extreme-wave validation.
    """

    observed_global = validation["Hs_Boia"]
    modeled_global = validation["Hs_m"]

    extremes = validation[
        validation["Hs_Boia"] >= threshold
    ]

    observed_extreme = extremes["Hs_Boia"]
    modeled_extreme = extremes["Hs_m"]

    max_value = max(
        observed_global.max(),
        modeled_global.max()
    ) + 0.2

    fig, (ax1, ax2) = plt.subplots(
        1,
        2,
        figsize=(12, 5.5),
        dpi=300
    )

    _plot_panel(
        ax=ax1,
        observed=observed_global,
        modeled=modeled_global,
        metrics=global_metrics,
        title="(a) Global wave regime",
        min_value=0,
        max_value=max_value,
    )

    _plot_panel(
        ax=ax2,
        observed=observed_extreme,
        modeled=modeled_extreme,
        metrics=extreme_metrics,
        title=(
            f"(b) Extreme wave regime "
            f"($H_s \\geq$ {threshold} m)"
        ),
        min_value=2.0,
        max_value=max_value,
    )

    plt.tight_layout()

    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        fig.savefig(
            output_path,
            bbox_inches="tight"
        )

    return fig


def _plot_panel(
    ax,
    observed,
    modeled,
    metrics,
    title,
    min_value,
    max_value,
):
    """
    Plot one validation scatter panel.
    """

    ax.scatter(
    observed,
    modeled,
    alpha=0.25,
    s=15,
    edgecolors="none",
    zorder=1,
)

    # Limit the 1:1 line to the actual data range
    line_min = max(
        min(observed.min(), modeled.min()) - 0.1,
        min_value,
    )

    line_max = min(
        max(observed.max(), modeled.max()) + 0.1,
        max_value,
    )

    ax.plot(
        [line_min, line_max],
    [line_min, line_max],
    linestyle="--",
    linewidth=1.8,
    color="dimgray",
    zorder=4,
    label="1:1 reference",
)

    x_values = np.array([
        min_value,
        max_value,
    ])

    y_values = (
        metrics["intercept"]
        + metrics["slope"] * x_values
    )

    ax.plot(
    x_values,
    y_values,
    linewidth=1.8,
    color="darkorange",
    zorder=3,
    label="Linear regression",
    )

    ax.set_xlim(
        min_value,
        max_value
    )

    ax.set_ylim(
        min_value,
        max_value
    )

    ax.set_aspect(
        "equal",
        adjustable="box"
    )

    ax.set_xlabel(
        "In situ $H_s$ (m)"
    )

    ax.set_ylabel(
        "ERA5 $H_s$ (m)"
    )

    ax.set_title(title)

    ax.grid(
        True,
        linestyle=":",
        alpha=0.6
    )

    stats_text = (
        f"N = {metrics['n']}\n"
        f"R = {metrics['r']:.2f}\n"
        f"R² = {metrics['r_squared']:.2f}\n"
        f"RMSE = {metrics['rmse']:.2f} m\n"
        f"BIAS = {metrics['bias']:.2f} m"
    )

    ax.text(
        0.05,
        0.95,
        stats_text,
        transform=ax.transAxes,
        verticalalignment="top",
        bbox={
            "boxstyle": "square,pad=0.4",
            "facecolor": "white",
            "alpha": 0.85,
            "edgecolor": "lightgray",
        },
    )

    ax.legend(
        loc="lower right",
        frameon=False
    )

def plot_validation_timeseries(
    validation,
    threshold=2.5,
    year=2025,
    output_path=None,
):
    """
    Plot ERA5 and buoy significant wave height
    for a selected year.
    """

    data = validation[
        validation.index.year == year
    ].copy()

    fig, ax = plt.subplots(
        figsize=(12, 6),
        dpi=300
    )

    ax.plot(
        data.index,
        data["Hs_m"],
        label="ERA5 reanalysis",
        linewidth=1.2,
    )

    ax.plot(
        data.index,
        data["Hs_Boia"],
        label="SiMCosta buoy",
        linewidth=1.0,
        alpha=0.8,
    )

    ax.axhline(
        threshold,
        linestyle="--",
        linewidth=1.4,
        label=f"Extreme-wave threshold ({threshold} m)",
    )

    ax.set_xlabel(f"Date ({year})")
    ax.set_ylabel("Significant wave height $H_s$ (m)")
    ax.set_title(
        f"ERA5 and in-situ wave-height time series ({year})"
    )

    ax.grid(
        True,
        linestyle=":",
        alpha=0.5
    )

    ax.legend(
        loc="upper right",
        frameon=False
    )

    plt.tight_layout()

    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        fig.savefig(
            output_path,
            bbox_inches="tight"
        )

    return fig