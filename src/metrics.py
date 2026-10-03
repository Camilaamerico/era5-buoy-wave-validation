import numpy as np


def calculate_validation_metrics(observed, modeled):
    """
    Calculate statistical metrics for model validation.
    """

    observed = np.asarray(observed, dtype=float)
    modeled = np.asarray(modeled, dtype=float)

    valid = np.isfinite(observed) & np.isfinite(modeled)

    observed = observed[valid]
    modeled = modeled[valid]

    if len(observed) == 0:
        raise ValueError("No valid observation pairs available.")

    rmse = np.sqrt(
        np.mean((modeled - observed) ** 2)
    )

    bias = np.mean(
        modeled - observed
    )

    r = np.corrcoef(
        observed,
        modeled
    )[0, 1]

    slope, intercept = np.polyfit(
        observed,
        modeled,
        1
    )

    return {
        "n": len(observed),
        "r": r,
        "r_squared": r ** 2,
        "rmse": rmse,
        "bias": bias,
        "slope": slope,
        "intercept": intercept,
    }


def filter_extremes(validation_df, threshold=2.5):
    """
    Filter validation pairs where observed buoy Hs
    is greater than or equal to the threshold.
    """

    return validation_df[
        validation_df["Hs_Boia"] >= threshold
    ].copy()