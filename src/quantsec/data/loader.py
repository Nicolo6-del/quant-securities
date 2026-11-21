from __future__ import annotations

import pandas as pd


def load_prices_csv(path: str) -> pd.DataFrame:
    """读取长表 CSV(列: date, symbol, close),返回宽表: index=日期, columns=标的。"""
    df = pd.read_csv(path, parse_dates=["date"])
    missing = {"date", "symbol", "close"} - set(df.columns)
    if missing:
        raise ValueError(f"缺少列: {sorted(missing)}")
    prices = df.pivot(index="date", columns="symbol", values="close").sort_index()
    return validate_prices(prices)


def validate_prices(prices: pd.DataFrame) -> pd.DataFrame:
    if not prices.index.is_monotonic_increasing:
        raise ValueError("日期索引必须单调递增")
    if prices.index.has_duplicates:
        raise ValueError("日期索引存在重复")
    if (prices <= 0).any().any():
        raise ValueError("价格必须为正数")
    return prices
