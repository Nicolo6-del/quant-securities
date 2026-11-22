"""逐项对照论文数值(Admati & Pfleiderer 1988)。论文表格保留两位或三位小数,故用对应容差。"""
import math

import pytest

from quantsec.theory.admati_pfleiderer import (
    equilibrium_n,
    info_revealed_q,
    informed_profit,
    kyle_lambda,
    price_change_variance,
    volumes,
)

# 论文示例: T'=2, T''=4; 非可选流动性方差=1; 可选交易者 A(方差4)、B(方差1) 都在第 3 期交易
PSI = [1, 1, 6, 1]            # 各期流动性交易总方差 Ψ_t
LIQ_SD = [1, 1, 4, 1]         # 各期 V^L = Σ sd = 2+1+1(第 3 期)


def test_table2_fixed_n():
    lam = [kyle_lambda(3, p) for p in PSI]
    assert lam == pytest.approx([0.43, 0.43, 0.18, 0.43], abs=0.005)

    vi, vl, vm, v = zip(*[volumes(3, PSI[t], LIQ_SD[t]) for t in range(4)])
    assert vi == pytest.approx((1.73, 1.73, 4.24, 1.73), abs=0.005)
    assert vl == pytest.approx((1.00, 1.00, 4.00, 1.00), abs=0.005)
    assert vm == pytest.approx((2.00, 2.00, 4.90, 2.00), abs=0.005)
    assert v == pytest.approx((4.73, 4.73, 13.14, 4.73), abs=0.005)

    # n 固定时价格信息量与 Ψ 无关(命题 3)
    assert [info_revealed_q(3)] * 4 == pytest.approx([0.25] * 4)


def test_table3_and_4_profits():
    assert [informed_profit(n, 6) for n in range(1, 8)] == pytest.approx(
        [1.225, 0.577, 0.354, 0.245, 0.183, 0.143, 0.116], abs=0.0005
    )
    assert [informed_profit(n, 1) for n in range(1, 5)] == pytest.approx(
        [0.500, 0.236, 0.144, 0.100], abs=0.0005
    )


def test_equilibrium_n_matches_paper():
    # 信息成本 c=0.13: Ψ=6 时 6 个知情交易者, Ψ=1 时 3 个
    assert equilibrium_n(6, 0.13) == 6
    assert equilibrium_n(1, 0.13) == 3


def test_table5_endogenous_n():
    ns = [equilibrium_n(p, 0.13) for p in PSI]
    assert ns == [3, 3, 6, 3]

    vi, vl, vm, v = volumes(6, 6, 4)
    assert (vi, vm, v) == pytest.approx((6.00, 6.48, 16.48), abs=0.005)
    assert kyle_lambda(6, 6) == pytest.approx(0.14, abs=0.005)
    assert info_revealed_q(6) == pytest.approx(0.14, abs=0.005)

    r = [price_change_variance(ns[t], ns[t - 1]) for t in range(1, 4)]
    assert r[0] == pytest.approx(1.00, abs=0.005)
    assert r[1] == pytest.approx(1.11, abs=0.005)
    # 论文表 5 印的是 0.90,按式(16)精确计算为 3/4 + 1/7 = 0.893(论文的舍入差异)
    assert r[2] == pytest.approx(3 / 4 + 1 / 7)
    assert r[2] == pytest.approx(0.90, abs=0.01)


def test_concentration_raises_volume_and_informativeness():
    """命题 2 与 4: 扎堆时段成交量更大、价格更有信息量、λ 更小。"""
    busy = volumes(6, 6, 4)[3]
    quiet = volumes(3, 1, 1)[3]
    assert busy > quiet
    assert info_revealed_q(6) < info_revealed_q(3)
    assert kyle_lambda(6, 6) < kyle_lambda(3, 1)


def test_price_variance_direction():
    assert price_change_variance(3, 3) == pytest.approx(1.0)
    assert price_change_variance(6, 3) > 1.0
    assert price_change_variance(3, 6) < 1.0


def test_exxon_calibration():
    """论文第 35 页: n=(4,1,3), σ_δ²=0.115661 时预测的价格变动标准差。"""
    s = math.sqrt(0.115661)
    n = [4, 1, 3]
    pred = [math.sqrt(price_change_variance(n[i], n[i - 1])) * s for i in range(3)]
    assert pred == pytest.approx([0.34849, 0.28454, 0.38023], abs=0.00001)
    # 与 1981 年 Exxon 观测值接近
    assert pred == pytest.approx([0.34959, 0.28371, 0.37984], abs=0.002)
