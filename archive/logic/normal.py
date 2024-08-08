from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm


@dataclass
class NormalDistributionModel:
    model: object
    mu: float
    var: float

@dataclass
class GammaDistributionModel:
    model: object
    alpha: float
    loc: float
    beta: float


def normal_distribution_log_likelihood(
    params: Tuple[float, float], x: pd.Series
) -> float:
    """Returns the log likelihood that a dataset is normally distributed given a set of
    parameters.
    """
    mu = params[0]
    var = params[1]
    n = len(x)
    log_likelihood = (
        -(n / 2) * np.log(2 * np.pi)
        - (n / 2) * np.log(var)
        - (1 / (2 * var) * sum((x - mu) ** 2))
    )
    return -log_likelihood


def mle_two_parameter_normal(x: pd.Series) -> Tuple[float, float]:
    """Returns the MLE for the mean and variance of a normally distributed set of data.
    """
    res = minimize(
        normal_distribution_log_likelihood, [0, 0], args=(x), method="Nelder-Mead"
    )
    mu = res.x[0]
    var = res.x[1]
    return mu, var


def normal_distribution_model(x: pd.Series, scipy: bool = False) -> NormalDistributionModel:
    """Returns a normal distribution model for a dataset using two parameter MLE for
    the parameter values.
    """
    if scipy:
        mu, var = norm.fit(x.dropna().values)
    else:
        mu, var = mle_two_parameter_normal(x.dropna().values)
    model = norm(mu, var)
    return NormalDistributionModel(model, mu, var)