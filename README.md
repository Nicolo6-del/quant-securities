# quant-securities

量化证券研究与回测框架(Python,市场无关)。

## 结构

| 目录 | 作用 |
|---|---|
| `src/quantsec/data` | 行情加载与校验 |
| `src/quantsec/signals` | 因子与信号,输出目标权重 |
| `src/quantsec/backtest` | 向量化回测,含手续费与滑点 |
| `src/quantsec/execution` | 日内成交量曲线、订单拆分、市场深度(Kyle λ)估计 |
| `src/quantsec/risk` | 夏普、最大回撤等指标 |
| `research/` | 研究笔记与待验证假设 |
| `tests/` | 单元测试 |

## 快速开始

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

```python
from quantsec.data.loader import load_prices_csv
from quantsec.signals.momentum import momentum_weights
from quantsec.backtest.engine import backtest
from quantsec.risk.metrics import summary

prices = load_prices_csv("data/prices.csv")   # 列: date,symbol,close
w = momentum_weights(prices)
res = backtest(prices, w, fee_bps=1.0, slippage_bps=2.0)
print(summary(res["net"]))
```

## 约定

- 信号在第 t 日收盘后计算,**第 t+1 日**才按该权重持仓(回测引擎内部已做 shift,避免未来函数)。
- 成本 = 换手率 × (手续费 + 滑点),单位 bp。
- 数据文件不要提交到仓库(见 `.gitignore`)。
