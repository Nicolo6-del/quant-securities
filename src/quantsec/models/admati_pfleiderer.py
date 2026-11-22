"""Admati & Pfleiderer (1988) 单期均衡的数值实现。

设定(论文第 1、2 节): 所有知情交易者观察同一信号 δ_{t+1} + ε_t,
并取 var(δ)=1 (论文说明此归一化不失一般性), φ = var(ε)。

符号:
    n    知情交易者人数
    psi  该时段流动性交易的总方差 Ψ_t (不可选 + 可选流动性交易)
    phi  信号噪声方差 φ
"""
from __future__ import annotations

from math import sqrt


def kyle_lambda(n: float, psi: float, phi: float = 0.0) -> float:
    """市场深度参数 λ_t, 即论文式(5)。1/λ 为 Kyle 的市场深度。"""
    return (1.0 / (n + 1.0)) * sqrt(n / (psi * (1.0 + phi)))


def informed_beta(n: float, psi: float, phi: float = 0.0) -> float:
    """每个知情交易者的下单系数 β_t, 即论文式(4)。"""
    return sqrt(psi / (n * (1.0 + phi)))


def informed_profit(n: float, psi: float, phi: float = 0.0) -> float:
    """每个知情交易者的单期期望利润 π(n, Ψ), 即论文式(17)。"""
    return (1.0 / (n + 1.0)) * sqrt(psi / (n * (1.0 + phi)))


def equilibrium_n(psi: float, cost: float, phi: float = 0.0, n_max: int = 10_000) -> int:
    """内生信息获取下的知情者人数(论文第二种进入模型)。

    返回唯一满足 π(n+1, Ψ) < c <= π(n, Ψ) 的 n。
    """
    if informed_profit(1, psi, phi) < cost:
        raise ValueError("信息成本过高: 连 1 个知情交易者都无法盈利")
    n = 1
    while n < n_max and informed_profit(n + 1, psi, phi) >= cost:
        n += 1
    return n


def price_informativeness_Q(n: float, phi: float = 0.0) -> float:
    """Q_t = var(δ_{t+1} | P_t), 即论文式(15)。越小说明价格越有信息量。"""
    return 1.0 / (1.0 + n / (1.0 + phi + n * phi))


def price_change_variance_R(n_t: float, n_prev: float, phi: float = 0.0) -> float:
    """R_t = var(P_t - P_{t-1}), 即论文式(16); var(δ)=1。"""
    return (n_t / (1.0 + n_t) + 1.0 / (1.0 + n_prev) + phi) / (1.0 + phi)


def volume_measures(
    n: float,
    discretionary_vars: list[float],
    var_z: float,
    phi: float = 0.0,
) -> dict:
    """某一时段的成交量分解, 即论文式(8)-(11)。

    discretionary_vars: 在该时段交易的各可选流动性交易者的需求方差。
    var_z: 不可选流动性交易的方差。
    """
    psi = sum(discretionary_vars) + var_z
    v_i = sqrt(n * psi)                               # 知情者 (式 8 / 12)
    v_l = sum(sqrt(v) for v in discretionary_vars) + sqrt(var_z)  # 流动性交易者 (式 9)
    v_m = sqrt(psi * (n + 1.0))                       # 做市商 (式 10), var(ω)=Ψ(n+1)
    return {
        "psi": psi,
        "lambda": kyle_lambda(n, psi, phi),
        "V_I": v_i,
        "V_L": v_l,
        "V_M": v_m,
        "V": v_i + v_l + v_m,
        "Q": price_informativeness_Q(n, phi),
    }
