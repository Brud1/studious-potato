import re

import matplotlib.pyplot as plt


def plot_risk_metrics(data):
    risk_metric_features = [f for f in data.columns if "risk" in f]
    
    for metric in risk_metric_features:
        fig, ax = plt.subplots()
        fig.set_size_inches(14, 8)
        ax2 = ax.twinx()
        
        ax.set_yscale("log")
        
        ax.plot(data.DateTime, data.close)
        ax2.plot(data.DateTime, data[metric], color="green", linestyle=":")
    
        ax.set_title(f"{metric}")
        plt.show()


def plot_ma_extensions(data):
    regex = r"^[A-Z]{2,3}[0-9]{1,3}$"
    ma_features = [f for f in data.columns if re.match(regex, f)]
    
    for ma in ma_features:
        extension = data.close / data[ma]
        fig, ax = plt.subplots()
        fig.set_size_inches(14, 8)
        ax2 = ax.twinx()
        
        ax.set_yscale("log")
        
        ax.plot(data.DateTime, data.close)
        ax2.plot(data.DateTime, extension, color="green", linestyle=":")
    
        ax.set_title(f"{ma} extension")
        plt.show()


def plot_backtest_results(metric, datetimes, cash_balance, account_balance, btc_balance):
    fig, ax = plt.subplots()
    fig.set_size_inches(14, 8)
    ax2 = ax.twinx()
        
    ax.plot(datetimes, cash_balance, color="green", label="cash balance")
    ax.plot(datetimes, account_balance, color="blue", label="account balance")
    ax2.plot(datetimes, btc_balance, color="green", linestyle=":", label="btc balance")
    
    ax.set_title(f"{metric} backtest - {(datetimes[-1] - datetimes[0]).days / 7} weeks")
    
    ax.legend(loc="upper left")
    ax2.legend(loc="lower left")
    plt.show()