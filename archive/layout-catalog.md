# 版式组件契约（HTML 落地 + 双层系统）

> **本文件为框架留白版**：所有标注 `🔲 待填` 的约束内容待 `skills整合.md` 定稿后回填。
> 章节映射：本文件 ↔ skills整合.md **第三部分 · 双层系统** + 第二部分 Step 2 路由表的版式 HTML 化。
>
> | 本文件 | 整合稿来源 |
> |---|---|
> | §1 版式组件清单 | 第二部分 Step 2 + lampertb slide-type catalog |
> | §2 Layer 1 数据层组件 | 第三部分 Layer 1 |
> | §3 Layer 2 洞察标注层 | 第三部分 Layer 2 |
> | §4 overlay 触发规则 | 第三部分（lampertb 缺，我们补的规则） |

---

## §1 · 版式组件清单

每个版式 ID 对应一个 HTML/CSS 组件契约（DOM 结构 + CSS 要点 + 容量）。**本表 ID 必须与 [routing.md](routing.md) §2 的"首选版式 ID"一一对应。**

| 版式 ID | 对应 data-shape | HTML 结构要点 | 容量上限 |
|---|---|---|---|
| 🔲 待填 -- 来源：整合稿第二部分 Step 2 首选版式列 + lampertb catalog | 🔲 待填 | 🔲 待填 | 🔲 待填 |

（行数 = 路由表引用的全部版式；定稿时逐版式补齐组件契约，每个契约含：DOM 骨架代码样例 + 关键 CSS 类 + 填充规则。）

---

## §2 · Layer 1 · 数据层组件（base data）

图表、表格、原始事实的组件契约。表格规范（竖线/隔行底/对齐）与图表标注规范在此定义。

| 组件 | 字段/内容契约 | HTML 实现要点 |
|---|---|---|
| 🔲 待填 -- 来源：整合稿第三部分 Layer 1（data_table / bar_chart / line_chart / waterfall_chart / three_column / two_column / key_stat 等） | 🔲 待填 | 🔲 待填 |

MBB 表格规范：🔲 待填（无竖线/隔行交替底/数字右对齐等细则的落地写法）

图表标注规范：🔲 待填（直接标 labels、网格线克制、高亮结论等细则）

---

## §3 · Layer 2 · 洞察标注层（insight overlays）

盖在数据层之上的判断，用 HTML/CSS 绝对定位实现（对应 lampertb 的 x/y/width/height 字段，单位换算为画布百分比或 px）。

| overlay 类型 | 字段契约 | HTML/CSS 实现要点 |
|---|---|---|
| 🔲 待填 -- 来源：整合稿第三部分 Layer 2（callout_annotation / highlight_box / metric_badge / bracket_group / color_band / delta_indicator） | 🔲 待填 | 🔲 待填 |

---

## §4 · overlay 触发规则（防堆叠）

lampertb 原版无触发限制，导致一页堆 5 种 overlay。本节是**我们补的规则**：

| 触发条件 | 用哪种 overlay |
|---|---|
| 🔲 待填 -- 来源：整合稿第三部分"我们补的 overlay 触发规则"表 | 🔲 待填 |

**硬上限**：🔲 待填 -- 一页 Layer 2 overlay 的种类上限（整合稿定为 ≤ 2 种，定稿时确认）
