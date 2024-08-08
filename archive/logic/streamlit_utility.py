import pickle
import re
from datetime import datetime

from scipy.stats import norm

from logic.features import log_close_sma_extension
from logic.get import read_data
from logic.normal import NormalDistributionModel


def preprocess_data(data):
    data = data.interpolate()
    preprocessed_data = log_close_sma_extension(data)
    return preprocessed_data


def fit_normal_distribution(x):
    _x = x.dropna().values
    mu, var = norm.fit(_x)
    model = norm(mu, var)
    return NormalDistributionModel(model, mu, var)

def save_as_pickle(item, name):
    with open(name, "wb") as handle:
        pickle.dump(item, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"{name}.pickle saved.")


def train_and_save_btc_risk_models(name="btc_risk_models", test_train_split_date=datetime.now()):
    data = read_data("BTC", "1W")
    train_X = data.loc[data.DateTime < test_train_split_date].copy(deep=True)
    preprocessed_X = preprocess_data(train_X)

    model_dictionary = {}
    
    regex = r"^log_[A-Z]{2,3}[0-9]{1,3}_extension$"
    for log_ma in [
        f for f in preprocessed_X.columns 
        if re.match(r"^log_[A-Z]{2,3}[0-9]{1,3}_extension$", f)
    ]:
        x = preprocessed_X[log_ma]
        metadata = fit_normal_distribution(x)
        model_dictionary[log_ma] = metadata
        print(f"{log_ma} model trained with data < {test_train_split_date}")

    save_as_pickle(model_dictionary, name)

    return model_dictionary


def read_in_pickle(name):
    with open(name, "rb") as handle:
        return pickle.load(handle)


def score_btc_data_with_existing_models(name="btc_risk_models"):
    data = read_data("BTC", "1W")
    X = data.copy(deep=True)
    preprocessed_X = preprocess_data(X)

    models = read_in_pickle(name)

    for feature, metadata in models.items():
        x = preprocessed_X[feature]
        cdf_data = metadata.model.cdf(x)
        preprocessed_X[f"{feature}_risk"] = cdf_data

    return preprocessed_X


def combine_risks(data, metric_weights):
    risk = 0
    n = sum(metric_weights.values())
    
    for metric, weight in metric_weights.items():
        risk += data[metric]*weight

    combined_risk = risk / n
    return combined_risk


def combined_btc_risk_with_existing_models(metric_weights, name="btc_risk_models"):
    risk_data = score_btc_data_with_existing_models(name)
    risk_data["combined_risk"] = combine_risks(risk_data, metric_weights)
    return risk_data
