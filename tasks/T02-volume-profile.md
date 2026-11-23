# T02 日内成交量曲线(检验 P1、P2)

分支:`task/T02-volume-profile`。前置:T01 已合并。

## 目标
估计每只股票的日内平均成交量曲线,检验:(P1) 是否在 13:00 复牌后有第二个高峰;(P2) 天山生物的"聚集程度"是否弱于 `inst_heavy` 对照组。

## 定义(请严格按此实现)
- 每根 bar 的相对成交量 `v_{d,k} = volume_{d,k} / Σ_k volume_{d,k}`(d=日,k=48 根 bar 的序号)。按日归一化是为了消除不同日期成交量水平的差异。
- 曲线 `profile_k` = 所有有效日 `v_{d,k}` 的均值。
- **聚集程度**用两个指标:(a) 前 6 根 bar(开盘 30 分钟)与最后 6 根 bar 的占比之和;(b) `profile` 的基尼系数。
- **13:00 高峰**:13:00-13:05 这根 bar 的 `profile` 相对于其前一根(11:25-11:30)和后三根平均值的比值。

## 有效日
剔除:停牌日、涨跌停日、T01 标记的校验失败日、新股上市前 5 日。**事件日先不剔除**(T05 再做对比),但本任务要在剔除前后各跑一遍并分别输出。

## 不确定性
对日做 bootstrap(固定 seed,2000 次),给出每根 bar 的 `profile` 95% 区间,以及指标 (a)(b)、13:00 高峰比值的 95% 区间。

## 检验
- P1:天山生物及每只对照股的 13:00 高峰比值,其 95% 区间是否整体 > 1。
- P2:天山生物与 `inst_heavy` 组在指标 (a)(b) 上的差,用日 bootstrap 给区间。再与 `size_matched` 组比较。

## 交付
- `src/quantsec/research/volume_profile.py` + 测试(合成数据:构造已知 U 形/W 形曲线,检验函数能还原)
- `results/T02_profile.csv`(code,k,time,profile,lo,hi)、`results/T02_metrics.csv`、`results/T02_profile.png`
- `results/T02_report.md`:按 P1、P2 分别写"支持/不支持/不确定"及依据数字
