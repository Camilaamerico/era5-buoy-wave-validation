import numpy as np
import pandas as pd

from src.metrics import (
    calculate_validation_metrics,
    filter_extremes,
)


def test_validation_metrics_perfect_match():
    observed = np.array([1.0, 2.0, 3.0])
    modeled = np.array([1.0, 2.0, 3.0])

    metrics = calculate_validation_metrics(
        observed,
        modeled
    )

    assert metrics["n"] == 3
    assert np.isclose(metrics["r"], 1.0)
    assert np.isclose(metrics["r_squared"], 1.0)
    assert np.isclose(metrics["rmse"], 0.0)
    assert np.isclose(metrics["bias"], 0.0)
    assert np.isclose(metrics["slope"], 1.0)
    assert np.isclose(metrics["intercept"], 0.0)

def test_validation_metrics_known_error():
    observed = np.array([1.0, 2.0, 3.0])
    modeled = np.array([2.0, 3.0, 4.0])

    metrics = calculate_validation_metrics(
        observed,
        modeled
    )

    assert metrics["n"] == 3
    assert np.isclose(metrics["r"], 1.0)
    assert np.isclose(metrics["r_squared"], 1.0)
    assert np.isclose(metrics["rmse"], 1.0)
    assert np.isclose(metrics["bias"], 1.0)
    assert np.isclose(metrics["slope"], 1.0)
    assert np.isclose(metrics["intercept"], 1.0)
def test_filter_extremes():
    validation = pd.DataFrame(
        {
            "Hs_Boia": [1.2, 2.5, 2.7, 3.1],
            "Hs_m": [1.3, 2.4, 2.8, 3.0],
        }
    )

    extremes = filter_extremes(
        validation,
        threshold=2.5
    )

    assert len(extremes) == 3

    assert np.all(
        extremes["Hs_Boia"] >= 2.5
    )

    assert extremes["Hs_Boia"].tolist() == [
        2.5,
        2.7,
        3.1,
    ]