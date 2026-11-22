"""Admati & Pfleiderer (1988) 模型的均衡公式(相同信号情形,Lemma 1 / 命题 3-4)。

论文: A Theory of Intraday Patterns: Volume and Price Variability, RFS 1(1), 3-40.

记号(与论文一致): n=知情交易者人数, psi=流动性交易总方差 Ψ,
phi=信号噪声方差 φ, var_delta=公共信息方差(论文归一化为 1)。
"""
from __future__ import annotations

import math


def kyle_lambda(n: int, psi: float, phi: float = 0.0, var_delta: float = 1.0) -> float:
    """式(5): λ = var(δ)/(n+1) * sqrt(n / (Ψ (var(δ)+φ)))。λ 越小,市场越深。"""
    return var_delta / (n + 1) * math.sqrt(n / (psi * (var_delta + phi)))


def informed_beta(n: int, psi: float, phi: float = 0.0, var_delta: float = 1.0) -> float:
    """式(4): 每个知情交易者的下单强度 β = sqrt(Ψ / (n (var(δ)+φ)))。"""
    return math.sqrt(psi / (n * (var_delta + phi)))


def volumes(n: int, psi: float, liquidity_sds: float):
    """式(8)-(11),假设 var(δ)+φ 与 β 满足均衡关系。

    liquidity_sds = Σ_j sqrt(var(y_j)) + sqrt(var(z)),即流动性交易量 V^L。
    返回 (V_I, V_L, V_M, V_total)。
    """
    v_i = math.sqrt(n * psi)                # 式(12)
    v_m = math.sqrt(psi * (n + 1))          # var(ω) = n²β²(var+φ) + Ψ = Ψ(n+1)
    v_l = liquidity_sds
    return v_i, v_l, v_m, v_i + v_l + v_m


def info_revealed_q(n: int, phi: float = 0.0) -> float:
    """式(15): Q = (1 + n/(1+φ+nφ))^-1,价格未揭示的私有信息方差(越小越有信息量)。"""
    return 1.0 / (1.0 + n / (1.0 + phi + n * phi))


def price_change_variance(n_t: int, n_prev: int, phi: float = 0.0) -> float:
    """式(16): R_t = 1/(1+φ) * ( n_t/(1+n_t) + 1/(1+n_{t-1}) + φ ),公共信息方差归一化为 1。

    n_t > n_prev 时 R_t > 1,反之 R_t < 1;n 不变时 R_t = 1。
    """
    return (n_t / (1 + n_t) + 1 / (1 + n_prev) + phi) / (1 + phi)


def informed_profit(n: int, psi: float, phi: float = 0.0) -> float:
    """式(17): 每个知情交易者的期望利润 π(n,Ψ) = 1/(n+1) * sqrt(Ψ / (n(1+φ)))。"""
    return 1.0 / (n + 1) * math.sqrt(psi / (n * (1 + phi)))


def equilibrium_n(psi: float, cost: float, phi: float = 0.0, n_max: int = 10_000) -> int:
    """第二种进入模型: 唯一满足 π(n+1,Ψ) < c <= π(n,Ψ) 的 n。无解时返回 0。"""
    for n in range(1, n_max):
        if informed_profit(n + 1, psi, phi) < cost <= informed_profit(n, psi, phi):
            return n
    return 0
