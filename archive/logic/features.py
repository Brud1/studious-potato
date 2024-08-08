import re

import numpy as np


def log_close_sma_extension(data):
    _data = data.copy()
    regex = r"^[A-Z]{2,3}[0-9]{1,3}$"
    ma_features = [f for f in _data.columns if re.match(regex, f)]
    for ma in ma_features:
        if "ATR" not in ma:
            _data[f"log_{ma}_extension"] = np.log(_data["close"] / _data[ma])
    return _data


def identify_bubble_data(data, ma_length=50, extension=2):
    _data = data.copy(deep=True)
    _data[f"MA{ma_length}_extension"] = _data.close / _data[f"MA{ma_length}"]
    _data["bubble_data"] = np.nan

    _data.loc[_data[f"MA{ma_length}_extension"] < extension, "bubble_data"] = 0
    _data.loc[_data[f"MA{ma_length}_extension"] > extension, "bubble_data"] = 1

    return _data


def determine_fair_value(data, ma_length=50, extension=2):
    _data = identify_bubble_data(data, ma_length, extension)
    _bubble_data = _data.loc[_data["bubble_data"] == 1]
    _non_bubble_data = _data.loc[_data["bubble_data"] == 0]

    x = np.log(_non_bubble_data.index)
    y = np.log(_non_bubble_data.close)

    model = np.poly1d(np.polyfit(x, y, 1))
    lobf = model(np.log(_data.index))
    _data["fair_value"] = np.exp(lobf)

    return _data