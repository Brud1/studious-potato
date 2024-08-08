import warnings

import pandas as pd

from logic.get import read_data
from logic.risk import create_risk_features


def btc_risk(suppress_warnings=True) -> pd.DataFrame:
    """
    """
    btc_data = read_data("BTC", "1W")

    if suppress_warnings:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            processed_btc_data = create_risk_features(btc_data)
    else:
        processed_btc_data = create_risk_features(btc_data)
    
    return processed_btc_data


def eth_risk(suppress_warnings=True) -> pd.DataFrame:
    """
    """
    eth_data = read_data("ETH", "1D")
    eth_data.ffill(inplace=True)

    if suppress_warnings:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            processed_eth_data = create_risk_features(eth_data)
    else:
        processed_eth_data = create_risk_features(eth_data)
    
    return processed_eth_data