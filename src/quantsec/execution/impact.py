from __future__ import annotations

import numpy as np
import pandas as pd


def estimate_kyle_lambda(price_change: pd.Series, order_flow: pd.Series) -> float:
    """估计 Kyle's lambda: 价格变动对净订单流的回归斜率 cov(dP, q) / var(q)。

    lambda 越小,市场越深,单位订单流对价格的冲击越小。
    """
    df = pd.concat([price_change, order_flow], axis=1, keys=["dp", "q"]).dropna()
    var_q = df["q"].var()
    if len(df) < 3 or var_q == 0 or np.isnan(var_q):
        return float("nan")
    return float(df["dp"].cov(df["q"]) / var_q)


def lambda_by_bucket(price_change: pd.Series, order_flow: pd.Series, buckets) -> pd.Series:
    """按时段(如一天中的半小时)分组估计 lambda,用于检验高成交量时段 lambda 是否更小。"""
    df = pd.concat([price_change, order_flow], axis=1, keys=["dp", "q"]).dropna()
    b = pd.Series(buckets, index=price_change.index).reindex(df.index)
    return pd.Series(
        {k: estimate_kyle_lambda(g["dp"], g["q"]) for k, g in df.groupby(b)}
    )


def intraday_volume_profile(volume: pd.Series) -> pd.Series:
    """历史日内成交量曲线: 按一天中的时间取平均并归一化(和为 1)。要求 DatetimeIndex。"""
    tod = volume.groupby(volume.index.time).mean()
    return tod / tod.sum()


def schedule_order(total_shares: float, profile: pd.Series) -> pd.Series:
    """按成交量曲线拆分母单(类 VWAP),把交易量放到市场更厚的时段。"""
    return profile * total_shares
