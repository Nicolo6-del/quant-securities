# T00b 环境与系统摸底

分支:`task/T00b-environment`。前置:无,可与 T00 并行,**建议最先做**。

## 为什么需要
仓库里的代码此前只在 Claude 的沙箱里用等价断言验证过,**没有在真实的 pytest / CI 环境里跑过**。Claude 也无法访问你的机器和数据,需要你把真实情况如实告诉它。

## 逐项执行并记录(写入 `results/T00b_environment.md`)
1. **环境**:操作系统、CPU 核数、内存、磁盘剩余、Python 版本、是否有 GPU(无需用到)。
2. **安装**:克隆仓库,`pip install -e ".[dev]"`,贴出完整命令和输出的最后 20 行。失败的话贴完整报错。
3. **测试**:在 `master` 上运行 `pytest -v`,贴完整结果(通过/失败/跳过数量与失败详情)。
4. **理论分支**:切到 `feature/ap-model` 再运行一次 `pytest -v`,重点看 `tests/test_admati_pfleiderer.py` 是否全部通过。**如有失败,不要改测试让它通过,贴出实际值与预期值。**
5. **依赖版本**:`pip freeze` 中 numpy、pandas、scipy、statsmodels、pyarrow 的版本(缺哪个就说缺哪个)。后续任务可能需要 scipy/statsmodels/pyarrow,缺了要在 `pyproject.toml` 里加,并说明原因。
6. **GitHub Actions**:`.github/workflows/ci.yml` 在 `master` 上最近一次运行的结果(通过/失败,失败贴日志摘要)。
7. **性能摸底**:处理 300313 一个交易日的 tick/快照数据读入内存需要多少内存、多长时间。据此估计全样本(区间 × 股票数)的处理时间与存储,写出是否需要分批、分区存储。

## 不确定性与规则
- 看到的任何异常(版本冲突、测试不通过、CI 红灯)原样记录,不要私下修复后隐瞒。
- 修复若必要,单独开 PR `[fix] ...`,说明原因,不要混入本任务的报告。

## 交付
- `results/T00b_environment.md`
- 若需要补依赖:对 `pyproject.toml` 的修改(单独 PR)
