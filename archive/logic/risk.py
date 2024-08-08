from datetime import datetime
import re

import numpy as np
import pandas as pd

from logic.normal import normal_distribution_model
from logic.features import log_close_sma_extension


def risk_metric(x: pd.Series) -> np.array:
    """Returns the risk metric for a given log(close/ma) dataset."""
    model_info = normal_distribution_model(x)
    pdf_data = model_info.model.pdf(x)
    normalised_pdf_data = pdf_data / model_info.model.pdf(model_info.mu)
    x_avg = model_info.mu
    factor = np.empty_like(np.array(x))
    factor[np.where(x > x_avg)] = 1
    factor[np.where(x < x_avg)] = -1
    return 0.5 + (factor * (1 - normalised_pdf_data) * 0.5)  

def log_ma_risk_metric(data):
    _data = data.copy()
    regex = r"^log_[A-Z]{2,3}[0-9]{1,3}_extension$"
    log_ma_extension_features = [f for f in _data.columns if re.match(regex, f)]
    for log_ma in log_ma_extension_features:
        regex =  r"[A-Z]{2,3}[0-9]{1,3}"
        _match = re.search(regex, log_ma)
        ma = _match.group(0)
        _data[f"risk_{ma}"] = risk_metric(_data[log_ma])
    return _data

def create_risk_features(data):
    _data = log_close_sma_extension(data)
    _data = log_ma_risk_metric(_data)
    _data["combined_risk"] = (
        _data["risk_MA100"] 
        + _data["risk_MA50"] 
        + _data["risk_MA20"]
        + _data["risk_MA8"]
    ) / 4
    return _data