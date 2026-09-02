# Layout Routing：内容 -> 版式查询表

本文件是内容关系到视觉结构的判断参考：先识别主要关系，再用适用条件和容量约束缩小候选范围。它降低无依据的随机选择，但不追求同一内容只能得到唯一版式。

入口：[page-logic.md](page-logic.md) 最小内部契约的 `data_shape` 字段在此查表。出口：确定版式后，才进入 [visual-language.md](visual-language.md) 的页面设计。

## 1. data-shape：12 类常用关系

每类给识别信号与典型内容。页面可以包含多个 shape；特殊关系允许使用 `custom` 并用自然语言说明，不能为了塞进枚举而改写业务含义。

| data-shape | 识别信号 | 典型内容 |
|---|---|---|
| `comparison` | A vs B / 前后 / 现状与目标 / 两难权衡 | 转型前后对比、方案对比 |
| `decomposition` | 一个整体拆成 N 个并列且 MECE 的部分 | 三大举措、业务构成 |
| `progression` | 有明确时间 / 阶段 / 步骤递进 | 能力建设两阶段、roadmap |
| `scorecard` | ≥3 个 KPI / 关键数字需要冲击感 | 利润、回报率、份额 |
| `matrix-2x2` | 两个维度交叉定位一组对象 | 优先级矩阵、风险矩阵 |
| `process-flow` | 机制 / 价值链 / 漏斗 / 飞轮 / 顺序工作流 | 运营模型、转化漏斗 |
| `bridge` | 起点 -> 终点之间的增减拆解 | 利润桥、成本桥、差异分析 |
| `evaluation` | 多对象 × 多准则的打分比较 | 评估矩阵、供应商评分、热力图 |
| `narrative` | 纯文字论点 / 结论 / 引用，无数据 | 执行摘要、金句页、闭幕页 |
| `causal` | 单个因果链：A 导致 B（含反推） | 问题归因、根因分析 |
| `hierarchy` | 层级 / 从属 / 树形结构 | 组织架构、issue tree、decision tree |
| `path-to-result` | 一组并列要素构成整体路径，共同导向一个结果 | 举措组合 -> 回报（某转型案例页骨架） |

新增三类的依据（BCG Grid 16:9 模板印证，见 §5/§6）：

- **path-to-result**：BCG 为「箭头」专门做了 one third / half / two third 三档宽度版式--「组合路径导向结果」在其体系里是一等公民，不是随手画的装饰
- **causal**：BCG 的 Left arrow / Green left arrow（反向箭头）即反推因果
- **hierarchy**：麦肯锡 toolkit 的 Issue tree / Decision tree / Org chart 是独立模式家族；process-flow 的「顺序」语义覆盖不了「从属」

复杂页面可在内部留下简短判断记录，例如：

```json
{ "shapes": ["comparison", "path-to-result", "scorecard"],
  "reason": "困境是前后对比、举措组合整体导向回报、成果是三个KPI" }
```

## 2. 路由表：shape 到候选版式

对主要 shape 查看 **Use when / Don't use when / Capacity**。仅在候选版式相近或结果明显不稳定时补充相邻版式比较。

| data-shape | 首选版式 | Use when | Don't use when | Capacity（超了换/拆） | 相邻辩护要点 |
|---|---|---|---|---|---|
| comparison | 两栏对比 | 两个平衡对照、3–5 个可比维度 | 三方以上对比 | 2 方 × ≤5 维度 | 不是 decomposition：只有两方且对立 |
| decomposition | 三/四栏并列 | 3–4 个 MECE 并列项，每项 1 标题 + 1 论据 | 项数 >4，或存在层级（-> hierarchy） | 恰 3–4 栏 | 不是 path-to-result：并列项无共同结果区 |
| progression | 阶梯 / 演进轴 | 有明确先后阶段 | 无时间逻辑的并列（-> decomposition） | 2–5 阶段 | 不是 process-flow：阶段是里程碑不是工作环节 |
| scorecard | KPI 英雄数字带 | 3–6 个关键数字、要视觉冲击 | 数字需配图表佐证 | 1 hero + ≤5 辅 | 不是 narrative：有数字冲击诉求 |
| matrix-2x2 | 四象限 | 两个有意义变量定位 ≤12 项 | 单维度排序 | 4 象限 ≤12 点 | 不是 evaluation：无打分准则列 |
| process-flow | 流程 / 价值链图 | 顺序工作流或因果机制 | 非顺序的并列 | 3–7 环节 | 不是 causal：多环节机制不是单因单果 |
| bridge | 瀑布 / 桥图 | 起点到终点的增减拆解 | 无中间增量 | 3–10 个驱动 | 不是 scorecard：重点是拆解过程不是数字冲击 |
| evaluation | 评分矩阵 / 热力图 | 多对象 × 多准则比较 | 单一对象 | 4–12 行 × 3–8 列 | 不是 matrix-2x2：有显式准则维度 |
| narrative | 结论横幅 / 引用页 | 纯论点、执行摘要 | 有数据要呈现 | 1 句 + ≤3 支撑 | -- |
| causal | 因果箭头图 | 单因果链（含反推） | 多环节机制（-> process-flow） | ≤3 个因果对 | 不是 path-to-result：单个因果不是组合路径 |
| hierarchy | 树 / 组织图 | 从属或逐层分解 | 平铺无层级 | ≤3 层 × 每层 ≤5 节点 | 不是 decomposition：节点间有父子关系 |
| path-to-result | 组合路径 + 结果区 | 并列要素整体导向一个结果 | 只有一条路径（-> causal） | 3–5 路径要素 + 1 结果区 | 箭头必须从整个路径组出发，不专属最后一栏 |

当两个候选版式难以判断时，可写一句相邻版式比较：

> `three-column` --「恰好三个 MECE 举措；**不是** four-column，因为只有三项；**不是** path-to-result，因为举措间无共同结果区。」
> `arrow-combo` --「三条举措组合导向回报结果；**不是** three-column，因为存在显式结果区且箭头从整组出发。」

需要记录时可使用以下内部格式；普通任务不要求输出或落盘：

```json
{ "layout": "arrow-combo", "shape": "path-to-result",
  "not": "three-column，因为有显式结果区",
  "fit_check": "3 路径 × 2 论据 + 1 结果区，未超容" }
```

## 3. 组合成页（多 shape -> 单页分区）

一页常含多个 shape（如 comparison + path-to-result + scorecard）。规则：

- **主版式**由承载核心论点的 shape 决定
- 次要 shape 降为**辅助区**（背景条 / 成果带），用「能承载结论的最小版式」压缩
- 单页分区骨架 = `Action Title -> [背景/Why 区] -> [主体/How 区] -> [成果/So-What 区]`
- 一页仍只服务一个论点；装不下时**优先拆页**，不压缩到失真

## 4. 分档：同一关系按内容量选宽度

吸收自 BCG 模板的 one third / half / two third 命名体系：同一逻辑关系不因内容略超就换版式，先在同版式的**宽度档**里调。

| 档 | 主辅占比 | 适用 |
|---|---|---|
| one third | 1/3 : 2/3 | 辅区内容轻（背景、单条结论） |
| half | 1/2 : 1/2 | 两侧平衡对照（comparison 默认档） |
| two third | 2/3 : 1/3 | 主区内容重、辅区只放结论（图表 + takeaways 默认档） |

判定顺序：先问「换档能否装下」-> 再问「是否换版式」-> 最后才「拆页」。

## 5. 几何参照（验证用，不覆盖 foundation 已确认值）

来源：BCG Grid 16:9 模板（`测试用ppt.pptx`）的 Layout guide 标尺版式，数值实测自版式占位符，按 1in = 120px 换算到 1600×900。用途是**验证** foundation 几何值的合理性并补 12 列网格参数，不是改已确认值。

| 项 | BCG 实测 | 换算 1600×900 | foundation 现值 | 结论 |
|---|---|---|---|---|
| 左右边距 | 0.69in | 83px | 72px | 同量级，维持 72px |
| 可用宽度 | 11.96in | 1435px | 1456px（1600 − 2×72） | 一致量级 |
| 标题带 top | 0.68in | 82px | 72px | 维持 72px |
| 留白带 top | 1.64in | 197px | 分隔线 176px | 接近，维持 176px |
| 正文区 | y 2.28–6.74in | 274–809px | 206px 起、796px 止 | 我们标题区更紧凑，起点更早，维持 |
| 12 列网格 | 每栏 0.7125in、栏距 0.31in | 每栏 85.5px、栏距 37px | -- | 需要细分栏时采用 |

12 列自洽验证：(12 × 0.7125) + (11 × 0.31) = 8.55 + 3.41 = 11.96in，与标尺实测可用宽度吻合。

麦肯锡 toolkit Default 版式分区（同为参照）：

- 标题带 y 0.39–1.19in（47–143px），副标带紧随其下
- 图表页 = 左图区约 8in（958px）+ 右侧 Key takeaways 栏约 3.9in（464px），takeaways 与图表说明**同一起点**
- Source 左下、Footnote 在其上方--与 foundation「来源放左下」一致

## 6. 麦肯锡模式目录对照（第二参考源）

麦肯锡 Business & Consulting Toolkit（205 页）本质是一套「逻辑模式目录」，其命名规律本身可迁移：**视觉结构 + 逻辑修饰词**（with takeaways / with two scenarios / with quadrants / historic and forecast）。做路由时可交叉验证：

| 模式家族（toolkit 页例） | 对应 data-shape |
|---|---|
| Waterfall chart（±修饰词） | bridge |
| Option evaluation / Harvey Balls / M&A comparison | evaluation |
| Issue tree / Decision tree / Org chart / Decision hierarchy | hierarchy |
| Process overview（linear / circular）/ Customer journey / Path overview | process-flow |
| Left arrow（反推） | causal |
| Levers -> outcomes / Findings and recommendations / Challenges and solutions / Synergy / Savings-investments | path-to-result |
| Competitor positioning / Value proposition comparison / Product comparison | comparison |
| Three / Four / Five key trends or areas / Initiatives / Honeycomb | decomposition |
| Timelines / Phases / Roadmap | progression |
| Scatter with quadrants / Competitor matrix / BCG 矩阵 / GE-McKinsey 矩阵 / SWOT | matrix-2x2 |
| Assessment or status overview / KPI 页 | scorecard |
| Executive summary / Big statement（BCG）/ Quote | narrative |
| Line chart with scenarios and gap analysis | comparison × progression（组合，走 §3） |

两个可迁移的用法：

- **with takeaways 修饰词**：任何数据版式都可挂「右侧结论栏」--图表放左约 2/3（two third 档），结论栏放右约 1/3，二者同一起点。这是「图表不单独成页」的标准实现（见 visual-language.md §7）
- **with scenarios / historic and forecast 修饰词**：时间分段（实际 vs 预测、基线 vs 情景）是数据页的通用增强，不改变基础 shape

注意：该模板自身使用左上角 section header（kicker）。本版默认不使用，但若它承担真实章节导航或语境作用，可在盲测中单独判断；其余几何与分类逻辑仅作参考。
