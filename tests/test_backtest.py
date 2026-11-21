import numpy as np
import pandas as pd

from quantsec.backtest.engine import backtest


def _prices():
    idx = pd.date_range("2024-01-01", periods=5, freq="D")
    return pd.DataFrame({"A": [100, 101, 102, 101, 103]}, index=idx, dtype=float)


def test_no_lookahead_first_day_zero():
    p = _prices()
    w = pd.DataFrame(1.0, index=p.index, columns=p.columns)
    res = backtest(p, w, fee_bps=0, slippage_bps=0)
    assert res["net"].iloc[0] == 0.0


def test_zero_cost_matches_buy_and_hold():
    p = _prices()
    w = pd.DataFrame(1.0, index=p.index, columns=p.columns)
    res = backtest(p, w, fee_bps=0, slippage_bps=0)
    expected = p["A"].iloc[-1] / p["A"].iloc[0]
    assert np.isclose(res["equity"].iloc[-1], expected)


def test_costs_reduce_returns():
    p = _prices()
    w = pd.DataFrame(1.0, index=p.index, columns=p.columns)
    free = backtest(p, w, 0, 0)["equity"].iloc[-1]
    paid = backtest(p, w, 10, 10)["equity"].iloc[-1]
    assert paid < free
