import pandas as pd

from pathlib import Path

from load_data import load_era5, load_buoy
from preprocess import align_era5_buoy
from metrics import (
    calculate_validation_metrics,
    filter_extremes,
)
from plots import (
    plot_validation_scatter,
    plot_validation_timeseries,
)


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

ERA5_FILE = DATA_DIR / "era5_Marica_data.csv"
BUOY_FILE = DATA_DIR / "buoy_data.csv"


def main():
    era5 = load_era5(ERA5_FILE)
    buoy = load_buoy(BUOY_FILE)

    validation = align_era5_buoy(
        era5,
        buoy
    )

    validation = validation[
    validation.index.year == 2025
].copy()

    print("\nValidation dataset:")
    print(validation.head())

    print(f"\nMatched observations: {len(validation)}")

    print(
        f"Period: "
        f"{validation.index.min()} -> "
        f"{validation.index.max()}"
    )

    # Global validation
    metrics = calculate_validation_metrics(
        observed=validation["Hs_Boia"],
        modeled=validation["Hs_m"]
    )

    print("\nGlobal validation metrics:")
    print(f"N: {metrics['n']}")
    print(f"R: {metrics['r']:.3f}")
    print(f"R²: {metrics['r_squared']:.3f}")
    print(f"RMSE: {metrics['rmse']:.3f} m")
    print(f"BIAS: {metrics['bias']:.3f} m")
    print(f"Slope: {metrics['slope']:.3f}")
    print(f"Intercept: {metrics['intercept']:.3f}")

    # Extreme-wave validation
    extremes = filter_extremes(
        validation,
        threshold=2.5
    )

    extreme_metrics = calculate_validation_metrics(
        observed=extremes["Hs_Boia"],
        modeled=extremes["Hs_m"]
    )

    print("\nExtreme-wave validation metrics:")
    print(f"N: {extreme_metrics['n']}")
    print(f"R: {extreme_metrics['r']:.3f}")
    print(f"R²: {extreme_metrics['r_squared']:.3f}")
    print(f"RMSE: {extreme_metrics['rmse']:.3f} m")
    print(f"BIAS: {extreme_metrics['bias']:.3f} m")
    print(f"Slope: {extreme_metrics['slope']:.3f}")
    print(f"Intercept: {extreme_metrics['intercept']:.3f}")

    # Export metrics table
    metrics_table = pd.DataFrame([
        {
            "regime": "global",
            "n": metrics["n"],
            "r": metrics["r"],
            "r_squared": metrics["r_squared"],
            "rmse_m": metrics["rmse"],
            "bias_m": metrics["bias"],
            "slope": metrics["slope"],
            "intercept": metrics["intercept"],
        },
        {
            "regime": "extreme",
            "n": extreme_metrics["n"],
            "r": extreme_metrics["r"],
            "r_squared": extreme_metrics["r_squared"],
            "rmse_m": extreme_metrics["rmse"],
            "bias_m": extreme_metrics["bias"],
            "slope": extreme_metrics["slope"],
            "intercept": extreme_metrics["intercept"],
        },
    ])

    metrics_path = (
        BASE_DIR
        / "outputs"
        / "tables"
        / "validation_metrics.csv"
    )

    metrics_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    metrics_table.to_csv(
        metrics_path,
        index=False
    )

    print(
        f"\nMetrics table saved to: {metrics_path}"
    )

    # Scatter plot
    scatter_path = (
    BASE_DIR
    / "outputs"
    / "figures"
    / "scatter_2025.png"
    )

    print(f"Scatter path: {repr(str(scatter_path))}")

    plot_validation_scatter(
        validation=validation,
        global_metrics=metrics,
        extreme_metrics=extreme_metrics,
        threshold=2.5,
        output_path=scatter_path,
    )

    print(
        f"Scatter figure saved to: {scatter_path}"
    )

    # Time-series plot
    timeseries_path = (
    BASE_DIR
    / "outputs"
    / "figures"
    / "timeseries_2025.png"
    )

    print(f"Time-series path: {repr(str(timeseries_path))}")

    plot_validation_timeseries(
        validation=validation,
        threshold=2.5,
        year=2025,
        output_path=timeseries_path,
    )

    print(
        f"Time-series figure saved to: {timeseries_path}"
    )


if __name__ == "__main__":
    main()