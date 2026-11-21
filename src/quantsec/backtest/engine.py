from __future__ import annotations

import pandas as pd


def backtest(
    prices: pd.DataFrame,
    weights: pd.DataFrame,
    fee_bps: float = 1.0,
    slippage_bps: float = 1.0,
) -> pd.DataFrame:
    """向量化回测。

    weights 为 t 日收盘后得到的目标权重,引擎延后一期(shift(1))生效,避免未来函数。
    返回列: gross(毛收益), cost(成本), net(净收益), turnover(换手), equity(净值)。
    """
    rets = prices.pct_change().fillna(0.0)
    w = weights.reindex(index=prices.index, columns=prices.columns).fillna(0.0)
    w = w.shift(1).fillna(0.0)

    gross = (w * rets).sum(axis=1)
    turnover = w.diff().abs().sum(axis=1)
    turnover.iloc[0] = w.iloc[0].abs().sum()
    cost = turnover * (fee_bps + slippage_bps) / 1e4
    net = gross - cost

    return pd.DataFrame(
        {
            "gross": gross,
            "cost": cost,
            "net": net,
            "turnover": turnover,
            "equity": (1.0 + net).cumprod(),
        }
    )
