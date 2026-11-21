from __future__ import annotations

import numpy as np
import pandas as pd


def momentum_weights(
    prices: pd.DataFrame,
    lookback: int = 60,
    skip: int = 5,
    top_frac: float = 0.2,
) -> pd.DataFrame:
    """截面动量: 做多得分最高的一组、做空最低的一组,总敞口为 1。

    得分 = 过去 lookback 日涨幅,跳过最近 skip 日(减弱短期反转影响)。
    """
    score = prices.shift(skip) / prices.shift(lookback) - 1.0
    rank = score.rank(axis=1, pct=True)
    long = (rank >= 1.0 - top_frac).astype(float)
    short = (rank <= top_frac).astype(float)
    w = long - short
    gross = w.abs().sum(axis=1).replace(0, np.nan)
    return w.div(gross, axis=0).fillna(0.0)
