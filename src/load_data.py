from pathlib import Path

import pandas as pd


def load_csv(path):
    """
    Load a CSV file and return it as a pandas DataFrame.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    return pd.read_csv(path)


def load_era5(path):
    """
    Load ERA5 wave data and standardize the datetime column.
    """
    df = load_csv(path)

    possible_time_columns = ["Data_Hora", "time", "date", "datetime"]

    time_column = next(
        (col for col in possible_time_columns if col in df.columns),
        None
    )

    if time_column is None:
        raise ValueError(
            "ERA5 file does not contain a recognized datetime column."
        )

    df["Data_Hora"] = pd.to_datetime(
        df[time_column],
        errors="coerce"
    )

    df = df.dropna(subset=["Data_Hora"])
    df = df.sort_values("Data_Hora").reset_index(drop=True)

    return df


def load_buoy(path):
    """
    Load SiMCosta buoy data.

    Metadata lines beginning with "/" are ignored.
    Datetime is reconstructed from YEAR, MONTH, DAY,
    HOUR, MINUTE and SECOND columns.

    HM0 is used as the observed significant wave height.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    df = pd.read_csv(
        path,
        comment="/"
    )

    required_time_columns = [
        "YEAR",
        "MONTH",
        "DAY",
        "HOUR",
        "MINUTE",
        "SECOND",
    ]

    missing_columns = [
        col for col in required_time_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing buoy datetime columns: {missing_columns}"
        )

    df["Data_Hora"] = pd.to_datetime(
        {
            "year": df["YEAR"],
            "month": df["MONTH"],
            "day": df["DAY"],
            "hour": df["HOUR"],
            "minute": df["MINUTE"],
            "second": df["SECOND"],
        },
        errors="coerce"
    )

    if "HM0" not in df.columns:
        raise ValueError(
            "Buoy file does not contain the HM0 wave-height variable."
        )

    df["Hs_Boia"] = pd.to_numeric(
        df["HM0"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["Data_Hora", "Hs_Boia"]
    )

    df = (
        df
        .sort_values("Data_Hora")
        .reset_index(drop=True)
    )

    return df