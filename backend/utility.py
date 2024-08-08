from datetime import datetime
from typing import Dict, List

import pandas as pd


def read_data(ticker_data_location: str) -> pd.DataFrame:
    ticker_data = pd.read_csv(ticker_data_location)

    if "time" in ticker_data.columns:
        ticker_data["time"] = ticker_data["time"].apply(
            lambda row: datetime.fromtimestamp(row)
        )
    elif "DateTime" in ticker_data.columns:
        ticker_data["DateTime"] = ticker_data["DateTime"].apply(
            lambda row: pd.to_datetime(row)
        )

    return ticker_data


def drop_zero_volume_days(ticker_data: pd.DataFrame) -> pd.DataFrame:
    drop_zero_volume_data = ticker_data.loc[ticker_data["Volume"] != 0].copy(deep=True)
    return drop_zero_volume_data


def rename_columns(
    ticker_data: pd.DataFrame, rename_dict: Dict[str, str]
) -> pd.DataFrame:
    renamed_data = ticker_data.rename(columns=rename_dict).copy(deep=True)
    return renamed_data


def select_features(ticker_data: pd.DataFrame, features: List[str]) -> pd.DataFrame:
    selected_data = ticker_data[features].copy(deep=True)
    return selected_data