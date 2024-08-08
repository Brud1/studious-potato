import os
from datetime import datetime

import pandas as pd


def read_data(ticker = "BTC", timeframe="1W") -> pd.DataFrame:
    _data = pd.read_csv(f"/media/sf_Shared_Folder/INDEX_{ticker}USD_{timeframe}.csv")
    _data.rename(
        columns={
            "MA": "MA100",
            #"ATR": "ATR1",
            #"ATR.1": "ATR14",
            "MA.1": "MA8",
            "MA.2": "MA50",
            "20w SMA": "MA20",
            "21w EMA": "EMA21",
            #"RSI-based MA": "RSI MA",
            "time": "DateTime",
        }, 
        inplace=True
    )
    _data = _data[
        [
            "DateTime",
            "open",
            "high",
            "low",
            "close",
            "Volume",
            #"Volume MA",
            "MA100",
            "MA50",
            "EMA21",
            "MA20",
            "MA8",
            #"RSI",
            #"RSI MA",
            #"ATR1",
            #"ATR14",
        ]
    ]
    _data["DateTime"] = _data["DateTime"].apply(
        lambda row: datetime.fromtimestamp(row)
    )

    return _data