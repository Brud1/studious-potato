from dataclasses import dataclass

import pandas as pd

from logic.plot import plot_backtest_results


@dataclass
class BacktestResults:
    metric: str
    trades: int
    final_account_balance: float
    amount_if_saved: float
    final_cash_balance: float
    final_btc_balance: float
    max_account_balance: float
    net_cash_profit: float
    net_btc_profit: float
    net_profit: float


def backtest_risk_metric(
    data: pd.DataFrame, 
    metric="risk_metric",
    starting_cash=10000, 
    starting_btc=1, 
    weekly_save=150, 
    weekly_spend=150, 
    weekly_sell=0.015
):
    _temp=data.copy(deep=True)
    
    CASH = starting_cash
    BTC = starting_btc
    WEEKLY_SAVE = weekly_save
    WEEKLY_SPEND = weekly_spend
    WEEKLY_SELL = weekly_sell
    SOLD = 0
    SPENT = 0
    TRADES = 0
    
    datetimes = []
    btc_balance = []
    cash_balance = []
    account_balance = []
    total_spent = []
    total_sold = []

    for week, row in enumerate(_temp.index):
        CASH += WEEKLY_SAVE
        if (BTC > 0) & (_temp[metric][row] >= 0.6):
            if (BTC >= 5*WEEKLY_SELL) & (_temp[metric][row] >= 0.9):
                BTC -= 5*WEEKLY_SELL
                CASH += 5*WEEKLY_SELL * _temp.close[row]
                SOLD += 5*WEEKLY_SELL
                TRADES += 1
        
            elif (BTC >= 4*WEEKLY_SELL) & (_temp[metric][row] >= 0.8):
                BTC -= 4*WEEKLY_SELL
                CASH += 4*WEEKLY_SELL * _temp.close[row]
                SOLD += 4*WEEKLY_SELL
                TRADES += 1

            elif (BTC >= 3*WEEKLY_SELL) & (_temp[metric][row] >= 0.7):
                BTC -= 3*WEEKLY_SELL
                CASH += 3*WEEKLY_SELL * _temp.close[row]
                SOLD += 3*WEEKLY_SELL
                TRADES += 1
                
            elif (BTC >= 2*WEEKLY_SELL) & (_temp[metric][row] >= 0.6):
                BTC -= 2*WEEKLY_SELL
                CASH += 2*WEEKLY_SELL * _temp.close[row]
                SOLD += 2*WEEKLY_SELL
                TRADES += 1
                
            else:
                CASH += BTC * _temp.close[row]
                SOLD += BTC
                BTC = 0
                TRADES += 1
                print(f"Run out of BTC {_temp.DateTime[row]}")
        
        elif (CASH > 0) & (_temp[metric][row] <= 0.4):
            if (CASH >= 5*WEEKLY_SPEND) & (_temp[metric][row] <= 0.1):
                CASH -= 5*WEEKLY_SPEND
                BTC += 5*WEEKLY_SPEND / _temp.close[row]
                SPENT += 5*WEEKLY_SPEND
                TRADES += 1
                
            elif (CASH >= 4*WEEKLY_SPEND) & (_temp[metric][row] <= 0.2):
                CASH -= 4*WEEKLY_SPEND
                BTC += 4*WEEKLY_SPEND / _temp.close[row]
                SPENT += 4*WEEKLY_SPEND
                TRADES += 1
                
            elif (CASH >= 3*WEEKLY_SPEND) & (_temp[metric][row] <= 0.3):
                CASH -= 3*WEEKLY_SPEND
                BTC += 3*WEEKLY_SPEND / _temp.close[row]
                SPENT += 3*WEEKLY_SPEND
                TRADES += 1
                
            elif (CASH >= 2*WEEKLY_SPEND) & (_temp[metric][row] <= 0.4):
                CASH -= 2*WEEKLY_SPEND
                BTC += 2*WEEKLY_SPEND / _temp.close[row]
                SPENT += 2*WEEKLY_SPEND
                TRADES += 1
                
            else:
                BTC += CASH / _temp.close[row]
                SPENT += CASH
                CASH = 0
                TRADES += 1
                print(f"Run out of capital {_temp.DateTime[row]}")
    
        datetimes.append(_temp.DateTime[row])
        cash_balance.append(CASH)
        btc_balance.append(BTC)
        account_balance.append(CASH + (BTC*_temp.close[row]))
        total_spent.append(SPENT)
        total_sold.append(SOLD)
        CASH += WEEKLY_SAVE

    backtest_results = BacktestResults(
        metric = metric,
        trades = TRADES,
        final_account_balance = round(account_balance[-1], 2),
        amount_if_saved = starting_cash + (len(datetimes)*WEEKLY_SAVE),
        final_cash_balance = cash_balance[-1],
        final_btc_balance = btc_balance[-1],
        max_account_balance = round(max(account_balance), 2),
        net_cash_profit = cash_balance[-1] - starting_cash - (len(datetimes)*WEEKLY_SAVE),
        net_btc_profit = btc_balance[-1] - starting_btc,
        net_profit = round(
            cash_balance[-1] 
            - (starting_cash + (len(datetimes)*WEEKLY_SAVE))
            + (
                (btc_balance[-1] - starting_btc) 
                * _temp.close[row]
            )
        ),
    )

    #plot_backtest_results(metric, datetimes, cash_balance, account_balance, btc_balance)
    #print(backtest_results)
    plot_data = metric, datetimes, cash_balance, account_balance, btc_balance

    return backtest_results, plot_data
