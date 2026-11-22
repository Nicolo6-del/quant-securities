"""用论文的数值例子检验实现(Table 2, 3, 4, 5 与第 7 节 Exxon 计算)。"""
from math import isclose, sqrt

from quantsec.models.admati_pfleiderer import (
    equilibrium_n,
    informed_profit,
    kyle_lambda,
    price_change_variance_R,
    price_informativeness_Q,
    volume_measures,
)


def test_lambda_matches_table2():
    assert isclose(kyle_lambda(3, 1.0), 0.4330, abs_tol=1e-3)
    assert isclose(kyle_lambda(3, 6.0), 0.1767, abs_tol=1e-3)


def test_lambda_decreasing_in_psi_and_n():
    assert kyle_lambda(3, 6.0) < kyle_lambda(3, 1.0)   # 流动性交易越多,市场越深
    assert kyle_lambda(6, 6.0) < kyle_lambda(3, 6.0)   # 相同信号下人越多越深


def test_volume_matches_table2():
    quiet = volume_measures(3, [], 1.0)
    busy = volume_measures(3, [4.0, 1.0], 1.0)
    assert isclose(quiet["V"], 4.73, abs_tol=0.01)
    assert isclose(busy["V"], 13.14, abs_tol=0.01)
    assert isclose(busy["V_I"], 4.24, abs_tol=0.01)
    assert isclose(busy["V_M"], 4.90, abs_tol=0.01)


def test_volume_matches_table5_endogenous_n():
    busy = volume_measures(6, [4.0, 1.0], 1.0)
    assert isclose(busy["V"], 16.48, abs_tol=0.01)
    assert isclose(busy["V_I"], 6.00, abs_tol=0.01)
    assert isclose(busy["lambda"], 0.14, abs_tol=0.005)


def test_profit_matches_table3_and_4():
    assert isclose(informed_profit(1, 6.0), 1.225, abs_tol=1e-3)
    assert isclose(informed_profit(6, 6.0), 0.143, abs_tol=1e-3)
    assert isclose(informed_profit(3, 1.0), 0.144, abs_tol=1e-3)


def test_equilibrium_n_matches_paper():
    assert equilibrium_n(6.0, 0.13) == 6
    assert equilibrium_n(1.0, 0.13) == 3


def test_Q_and_R_match_table5():
    assert isclose(price_informativeness_Q(3), 0.25, abs_tol=1e-9)
    assert isclose(price_informativeness_Q(6), 0.14, abs_tol=0.005)
    assert isclose(price_change_variance_R(6, 3), 1.11, abs_tol=0.005)
    assert isclose(price_change_variance_R(3, 6), 0.90, abs_tol=0.01)
    assert isclose(price_change_variance_R(3, 3), 1.0, abs_tol=1e-9)


def test_Q_independent_of_liquidity_variance_with_fixed_n():
    # 命题 3: n 固定时, 价格信息含量与流动性交易方差无关
    a = volume_measures(3, [], 1.0)["Q"]
    b = volume_measures(3, [4.0, 1.0], 1.0)["Q"]
    assert isclose(a, b)


def test_exxon_calibration_section7():
    var_delta = 0.115661
    n = (4, 1, 3)
    got = [
        sqrt(price_change_variance_R(n[i], n[i - 1]) * var_delta) for i in range(3)
    ]
    for g, want in zip(got, (0.34849, 0.28454, 0.38023)):
        assert isclose(g, want, abs_tol=1e-4)
