from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from scipy.stats import norm

from backend.utility import (
    drop_zero_volume_days,
    read_data,
    rename_columns,
    select_features,
)


def calculate_moving_average(close_price: np.ndarray, ma_length: int) -> np.ndarray:
    weights = np.ones(ma_length) / ma_length
    moving_average = np.convolve(close_price, weights, mode="valid")
    moving_average_with_nans = np.concatenate(
        (np.full(ma_length - 1, np.nan), moving_average)
    )
    return moving_average_with_nans


def log_close_sma_extension(
    ticker_data: pd.DataFrame, ma_features: List[str]
) -> pd.DataFrame:
    _data = ticker_data.copy()
    for ma in ma_features:
        _data[f"log_{ma}_extension"] = np.log(_data["close"] / _data[ma])
    return _data


def normally_distributed_data_cdf_score(
    ticker_data: pd.DataFrame,
    normal_features: List[str],
    training_date: Optional[datetime] = None
) -> pd.DataFrame:
    _temp = ticker_data.copy(deep=True)
    no_zero_volume_data = drop_zero_volume_days(_temp)

    if training_date is not None:
        training_data = no_zero_volume_data.loc[
            no_zero_volume_data["DateTime"] < training_date
        ].copy(deep=True)
    else:
        training_data = no_zero_volume_data.copy()

    for feature in normal_features:
        x = training_data[feature]
        mu, std = norm.fit(x.dropna())
        model = norm(mu, std)
        _cdf_scores = model.cdf(ticker_data[feature])
        _temp[f"{feature}_cdf_score"] = _cdf_scores

    return _temp


def calculated_weighted_importance_cdf(
    risk_data: pd.DataFrame, risk_importances: Dict[str, int]
) -> pd.DataFrame:
    _temp = risk_data.copy(deep=True)

    weighted_sum = sum(
        _temp[feature] * weight for feature, weight in risk_importances.items()
        if feature in _temp.columns
    )
    total_weight = sum(risk_importances.values())
    weighted_average = weighted_sum / total_weight
    _temp["total_risk"] = weighted_average
    return _temp


if __name__ == "__main__":
    import os

    HOME = os.getcwd()

    data_location = f"{HOME}\data\INDEX_BTCUSD_1W.csv"
    output_location = f"{HOME}\data\processed_INDEX_BTCUSD_1W.csv"
    rename_dict = {
        "MA": "MA100",
        "MA.1": "MA8",
        "MA.2": "MA50",
        "20w SMA": "MA20",
        "21w EMA": "EMA21",
        "time": "DateTime",
    }

    features = [
        "DateTime",
        "open",
        "high",
        "low",
        "close",
        "Volume",
        "MA100",
        "MA50",
        "EMA21",
        "MA20",
        "MA8",
    ]
    moving_averages = ["MA100", "MA50", "EMA21", "MA20", "MA8"]
    log_ma_extension_features = [f"log_{ma}_extension" for ma in moving_averages]
    ma_importances = {
        "log_MA100_extension_cdf_score": 1,
        "log_MA50_extension_cdf_score": 1,
        "log_MA20_extension_cdf_score": 1,
        #"log_MA8_extension_cdf_score": 1,
    }
    training_date = datetime(2024, 1, 1)

    print(data_location)

    raw_data = read_data(data_location)
    renamed_data = rename_columns(raw_data, rename_dict)
    selected_data = select_features(renamed_data, features)
    featured_data = log_close_sma_extension(selected_data, moving_averages)
    risk_data = normally_distributed_data_cdf_score(
        featured_data, log_ma_extension_features, training_date
    )
    total_risk_data = calculated_weighted_importance_cdf(risk_data, ma_importances)

    total_risk_data.to_csv(output_location)
    
    cdf_columns = [col for col in risk_data.columns if "cdf_score" in col]
    print(total_risk_data[cdf_columns+["close"]+["DateTime"] + ["total_risk"]].head())
    print(total_risk_data[cdf_columns+["close"]+["DateTime"] + ["total_risk"]].tail())
    print(f"Pre-processed data and saved to {output_location}")
