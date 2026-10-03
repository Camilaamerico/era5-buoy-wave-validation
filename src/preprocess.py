import pandas as pd


def prepare_era5(era5):
    """
    Prepare ERA5 data for buoy comparison.

    The ERA5 dataset is hourly, so Data_Hora is used
    directly as the temporal index.
    """
    required_columns = ["Data_Hora", "Hs_m"]

    missing = [
        col for col in required_columns
        if col not in era5.columns
    ]

    if missing:
        raise ValueError(
            f"Missing ERA5 columns: {missing}"
        )

    df = era5.copy()

    df = df[
        ["Data_Hora", "Hs_m"]
    ].dropna()

    df = (
        df
        .sort_values("Data_Hora")
        .set_index("Data_Hora")
    )

    return df


def prepare_buoy(buoy):
    """
    Prepare SiMCosta buoy data for comparison with hourly ERA5 data.

    Buoy timestamps are rounded to the nearest hour and
    observations assigned to the same hour are averaged,
    reproducing the original validation workflow.
    """
    required_columns = ["Data_Hora", "Hs_Boia"]

    missing = [
        col for col in required_columns
        if col not in buoy.columns
    ]

    if missing:
        raise ValueError(
            f"Missing buoy columns: {missing}"
        )

    df = buoy.copy()

    df = df[
        ["Data_Hora", "Hs_Boia"]
    ].dropna()

    df["Data_Hora"] = (
        df["Data_Hora"]
        .dt.round("h")
    )

    df = (
        df
        .groupby("Data_Hora", as_index=True)
        ["Hs_Boia"]
        .mean()
        .to_frame()
    )

    return df


def align_era5_buoy(era5, buoy):
    """
    Align hourly ERA5 significant wave height with
    hourly-averaged buoy observations.

    Only timestamps present in both datasets are retained.
    """
    era5_prepared = prepare_era5(era5)
    buoy_prepared = prepare_buoy(buoy)

    validation = era5_prepared.join(
        buoy_prepared,
        how="inner"
    )

    validation = validation.dropna(
        subset=["Hs_m", "Hs_Boia"]
    )

    return validation