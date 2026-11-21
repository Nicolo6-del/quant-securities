from __future__ import annotations

import numpy as np
import pandas as pd


def sharpe(returns: pd.Series, periods_per_year: int = 252) -> float:
    sd = returns.std()
    if sd == 0 or np.isnan(sd):
        return float("nan")
    return float(returns.mean() / sd * np.sqrt(periods_per_year))


def max_drawdown(returns: pd.Series) -> float:
    equity = (1.0 + returns).cumprod()
    peak = equity.cummax()
    return float((equity / peak - 1.0).min())


def summary(returns: pd.Series, periods_per_year: int = 252) -> dict:
    n = len(returns)
    equity_end = float((1.0 + returns).prod())
    ann_ret = equity_end ** (periods_per_year / n) - 1.0 if n else float("nan")
    return {
        "annual_return": ann_ret,
        "sharpe": sharpe(returns, periods_per_year),
        "max_drawdown": max_drawdown(returns),
    }
