# 版式路由（data-shape -> 版式）

> **本文件为框架留白版**：所有标注 `🔲 待填` 的约束内容待 `skills整合.md` 定稿后回填。
> 章节映射：本文件 ↔ skills整合.md **第二部分 · 核心机制：内容 -> 版式三段路由**。
>
> | 本文件 | 整合稿来源 |
> |---|---|
> | §1 data-shape 分类表 | 第二部分 Step 1 |
> | §2 路由表 | 第二部分 Step 2 |
> | §3 相邻版式辩护 | 第二部分 Step 2 |
> | §4 强制中间产物契约 | 第二部分 Step 1/2 |
> | §5 单页分区组合 | 第二部分 Step 3 |

---

## §1 · data-shape 封闭分类表（9 类）

把输入内容强制归入以下封闭集合，**禁止发明"其他"类**。判定依据是下表的识别特征（硬条件），不是语感。

| data-shape | 识别特征（判这个的硬条件） | 典型内容 |
|---|---|---|
| `comparison` | 🔲 待填 -- 来源：整合稿第二部分 Step 1 表 | 🔲 待填 |
| `decomposition` | 🔲 待填 | 🔲 待填 |
| `progression` | 🔲 待填 | 🔲 待填 |
| `scorecard` | 🔲 待填 | 🔲 待填 |
| `matrix-2x2` | 🔲 待填 | 🔲 待填 |
| `process-flow` | 🔲 待填 | 🔲 待填 |
| `bridge` | 🔲 待填 | 🔲 待填 |
| `evaluation` | 🔲 待填 | 🔲 待填 |
| `narrative` | 🔲 待填 | 🔲 待填 |

**增删规则**：类目可按需增删，但必须保持**可枚举、封闭**；新增类目必须同步补齐 §2 的路由条目。

---

## §2 · 路由表（shape -> 版式 ID）

每个 shape 映射到首选版式。**每个路由条目必须带三段**：Use when / Don't use when / Capacity。判定顺序：先过 Use/Don't use 两栏，再过 Capacity 栏；三段全过才锁定版式。

| data-shape | 首选版式 ID | Use when | Don't use when | Capacity（超了就换/拆） |
|---|---|---|---|---|
| `comparison` | 🔲 待填 -- 来源：整合稿第二部分 Step 2 表 | 🔲 待填 | 🔲 待填 | 🔲 待填 |
| `decomposition` | 🔲 待填 | 🔲 待填 | 🔲 待填 | 🔲 待填 |
| `progression` | 🔲 待填 | 🔲 待填 | 🔲 待填 | 🔲 待填 |
| `scorecard` | 🔲 待填 | 🔲 待填 | 🔲 待填 | 🔲 待填 |
| `matrix-2x2` | 🔲 待填 | 🔲 待填 | 🔲 待填 | 🔲 待填 |
| `process-flow` | 🔲 待填 | 🔲 待填 | 🔲 待填 | 🔲 待填 |
| `bridge` | 🔲 待填 | 🔲 待填 | 🔲 待填 | 🔲 待填 |
| `evaluation` | 🔲 待填 | 🔲 待填 | 🔲 待填 | 🔲 待填 |
| `narrative` | 🔲 待填 | 🔲 待填 | 🔲 待填 | 🔲 待填 |

版式 ID 在 [layout-catalog.md](layout-catalog.md) §1 中登记，两处必须一一对应。

---

## §3 · 相邻版式辩护（选版式时必写）

锁定版式的同时，必须写一句**"为什么不是最容易混淆的相邻版式"**。格式：

```
<版式ID> -- "<一句话适配理由>；不是 <相邻版式ID>，因为 <本质差异>。"
```

示例写法（🔲 待填，来源：整合稿第二部分 Step 2）：

- 🔲 待填：`prioritization_matrix` 的辩护示例
- 🔲 待填：`phases_chevron_3` 的辩护示例

---

## §4 · 强制中间产物契约

两个中间产物**都不许跳过**；产出后写入工作区文件，供 Step 6 质量门对照。

### 4.1 shapes.json（Step 2 产出）

```json
{
  "shapes": ["<从 §1 的 9 类中枚举>"],
  "reason": "<每个 shape 一句判定依据，引用 §1 识别特征>"
}
```

字段说明：
- `shapes`：🔲 待填 -- 取值范围与多 shape 时的排序规则（来源：整合稿第二部分 Step 1）
- `reason`：🔲 待填 -- 判定依据的写法要求

### 4.2 plan.json（Step 3 产出）

```json
{
  "format": "html | pptx",
  "governing_thought": "<Step 1 的中心论点>",
  "spine": "<Step 0 选定的叙事脊柱>",
  "pages": [
    {
      "page_no": 1,
      "role": "<页面角色，见 narrative.md §5>",
      "action_title": "<结论句>",
      "layout": "<版式 ID，来自 §2>",
      "shape": "<主 data-shape>",
      "not": "<相邻版式辩护：为什么不是隔壁那个>",
      "fit_check": "<容量校验结论：未超容/已拆页/已换版式>"
    }
  ]
}
```

字段说明：
- `format`：Step 0 确认的输出格式；**两路共用本契约的语义层骨架**
- `governing_thought` / `spine`：🔲 待填 -- 质量要求（来源：整合稿第四部分）
- `pages[].*`：🔲 待填 -- 各字段的填写细则与反例

**PPTX 路径扩展**：走 PPTX 时，Step 5B 在每页 `pages[]` 上追加内容级字段（`content` 块：版式专属字段 + Layer 2 overlays）+ deck 级 `theme` 块，契约见 [pptx-generation.md](pptx-generation.md) §2。HTML 路径不扩展，plan.json 保留页骨架级即可。

---

## §5 · 单页分区组合规则（多 shape -> 单页分区）

一页常含多个 shape。组合规则：

- **主版式**由承载核心论点的 shape 决定
- 次要 shape 降为**辅助区**（背景条 / 成果带），用"能承载结论的最小版式"原则压缩
- 单页分区骨架：`Action Title -> [Why 背景/语境区] -> [How 主体区] -> [So-What 成果/结论区]`

分区细则：🔲 待填 -- 来源：整合稿第二部分 Step 3（各区的内容边界、占比、升降级规则）
