# T04 分时段市场深度:Kyle λ、价差、盘口深度(修订版)

分支:`task/T04-depth-by-bucket`。前置:T01(修订版)、T02 已合并。
修订说明:原版因无买卖方向只能用 Amihud 代理;现有 tick 与 5 档盘口,直接估计论文的 λ,Amihud 降为稳健性检验。

## 新增预注册预测(在看数据前写下,提交时间即证据)
- **P4(升级)**:高成交量时段的 Kyle λ 更小,即 `λ_H < λ_L`(论文假设 1)。
- **P5**:高成交量时段的相对价差更低、五档深度更大。
- **P6**:λ 的时段差异在 `inst_heavy` 对照组中比在天山生物中更明显(与 P2 一致)。

## 一、Kyle λ(主检验)
论文中 λ 是价格变动对**当期净订单流**的回归系数(式 3,并见第 32 页对假设 1 的检验方法)。
- 对每个有效日 d、bar k:`dP_{d,k} = (mid_close − mid_open) / mid_open × 1e4`(bp,用中间价避免买卖价差跳动);`q_{d,k} = buy_amount − sell_amount`(元,按该股票全样本日均成交额标准化,写明标准化方式)。
- **分 bar 估计**:对每个 k,跨日回归 `dP = λ_k · q + e`(不加截距,与论文一致;截距版作为稳健性),日 bootstrap(2000 次,固定 seed)给 95% 区间。
- **H/L 比较**:沿用 T03 的**样本外**分类(前半样本定 H/L,后半样本检验)。合并回归 `dP = (λ_L + δ · 1[k∈H]) · q + e`,日聚类标准误。预测 δ < 0。
- **跨 bar 相关**:`λ_k` 与 T02 的 `profile_k` 的 Spearman 相关,预测为负,日 bootstrap 给区间。
- 稳健性:(i) 用 `sign(q)·√|q|` 处理价格冲击的非线性;(ii) 只用 `is_short=False` 且 `one_sided=False` 的 bar;(iii) 用 1 分钟 bar 重算(若数据体量允许)。

**需要诚实说明的局限(写入报告)**:同期回归反映的是"冲击 + 信息",论文的 λ 也正是这个含义,所以口径一致;但买卖方向由规则判定,有误差,误差会让 λ 被低估(衰减偏误),T01 报告里的准确率可用来估计偏误方向。

## 二、价差与盘口深度
对每个 bar k,汇总 `spread_rel`、`depth5_amount`(中位数及日 bootstrap 区间),比较 H 与 L:
- P5 预测:`spread_rel_H < spread_rel_L` 且 `depth5_amount_H > depth5_amount_L`。
- 注意:盘口深度的单位和挂单被撤单的特征(挂单可能是假单),在报告里只描述事实,不要过度解释。

## 三、稳健性:Amihud(原 T04 设定)
`A = |r| / amount`,按 bar 序号与 `profile_k` 做 Spearman 相关;同时做**安慰剂**:在每个 bar 序号 k 内,把 `|r|` 在日期间随机置换(500 次),得到"仅由分母造成"的机械斜率分布,报告真实斜率相对安慰剂的位置。

## 交付
- `src/quantsec/research/price_impact.py` + 测试(合成数据:已知 λ 的价格-订单流过程,检验还原;含方向判定错误率引入衰减偏误的测试)
- `results/T04_lambda_by_bar.csv`、`T04_lambda_HL.csv`、`T04_spread_depth.csv`、`T04_amihud_placebo.csv`
- `results/T04_report.md`:对天山生物及两个对照组,分别给出 P4、P5、P6 的"支持/不支持/不确定"及关键数字,并写明买卖方向判定的准确率
