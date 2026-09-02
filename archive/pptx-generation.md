# PPTX 路径（生成器工作流与契约）

> **本文件为框架留白版**：所有标注 `🔲 待填` 的约束内容待定稿后回填。
> 来源说明：`skills整合.md` 原定位为单 HTML 输出（第七部分取舍表"统一弃 PPTX 绑定"）；PPTX 路径为**新增裁量**，工作路径综合自三套 PPTX 系 skill：lampertb（plan.json 契约 + 生成器告警迭代）、mckinsey-pptx（PNG 预览渲染目检）、mbb-decks（依赖自检）。
>
> | 本文件 | 来源 |
> |---|---|
> | §1 工作流 | lampertb Step 2–5 + mbb-decks 依赖自检 + mckinsey-pptx 预览 |
> | §2 plan.json 内容级契约 | lampertb plan.json Specification |
> | §3 版式 ID -> slide type 映射 | lampertb Slide Types ↔ routing.md §2 |
> | §4 生成器质量告警清单 | 整合稿 6.2 可机械化子集 |
> | §5 预览渲染与版面目检 | mckinsey-pptx（soffice + pdftoppm） |

---

## §0 · 何时走 PPTX 路径

Step 0 输出格式 = PPTX。判定规则与取舍提示见 [SKILL.md](../SKILL.md) Step 0。

---

## §1 · 工作流（SKILL.md Step 5B 的展开）

```
Step 3 的 plan.json（页骨架级）
   │  ① 扩展至内容级（本文件 §2/§3 契约）
   ▼
plan.json（内容级）
   │  ② 依赖自检：python3 -c "import pptx"
   ▼
   │  ③ python scripts/generate_pptx.py --plan plan.json --output <主题>-deck.pptx
   ▼
.pptx + 生成器质量告警
   │  ④ 审读告警 -> 改 plan.json 重跑（不手改 .pptx）
   ▼
（Step 6）渲染 PNG 预览 -> 版面门目检
```

**迭代铁则**：PPTX 路径的唯一修改入口是 plan.json。发现任何问题（文字超界、配色、内容错漏）都回到 plan.json 修改后重新生成；直接编辑 .pptx 的改动会在下次重生成时丢失。

内容级扩展的字段填写细则：🔲 待填 -- 来源：lampertb plan.json Specification + 定稿后的版式契约

---

## §2 · plan.json 内容级契约（PPTX 专用扩展）

在 [routing.md](routing.md) §4.2 的骨架上追加：

```json
{
  "theme": {
    "font": "<字体>",
    "primary": "#<主色>",
    "accent1": "#<强调色1>", "accent2": "#<强调色2>", "accent3": "#<强调色3>"
  },
  "pages": [
    {
      "...routing.md §4.2 的全部骨架字段...": "...",
      "source": "<来源注，8pt 斜体左下>",
      "footnotes": ["<脚注，10pt，来源行上方>"],
      "content": { "<版式专属内容字段>" : "..." },
      "overlays": [ { "<Layer 2 overlay 规格>" : "..." } ]
    }
  ]
}
```

公共字段契约（所有 slide 通用）：

| 字段 | 必填 | 说明 |
|---|---|---|
| `source` | 🔲 待填 -- 来源：lampertb Common Fields | 来源注的格式与必填条件（数据页必填） |
| `footnotes` | 🔲 待填 | 脚注触发条件（有 caveat 就加） |
| `overlays` | 🔲 待填 | Layer 2 overlay 规格与坐标单位（英寸，内容区起点约 1.2"/0.75"） |
| `content` | 🔲 待填 | 版式专属字段的公共规则 |

`theme` 块与三套风格预设的映射：🔲 待填 -- 来源：design-system.md §1（预设 A/B/C -> pptx theme 字段）

---

## §3 · 版式 ID -> slide type 映射表

routing.md §2 选出的版式 ID 在 PPTX 路径下对应一个 slide type（生成器按 type 分发渲染）。**本表 ID 必须与 routing.md §2、layout-catalog.md §1 三处一一对应。**

| routing.md 版式 ID | pptx slide type | 版式专属 content 字段 | 容量差异（vs HTML 契约） |
|---|---|---|---|
| 🔲 待填 -- 来源：lampertb Slide Types + 定稿版式清单 | 🔲 待填 | 🔲 待填 | 🔲 待填 |

（定稿时逐版式补齐：type 名、字段清单、默认值、与 HTML 版式的容量差异。）

---

## §4 · 生成器质量告警清单

`generate_pptx.py` 在生成过程中输出的机械告警（PPTX 路径的机械校验，对应 HTML 路径的 `check_deck.py`）：

🔲 待填 -- 来源：整合稿 6.2 版面质量门中可机械化的子集（文字超界、字号低于下限、标题溢出换行、来源注缺失等）+ lampertb 生成器的告警项

---

## §5 · 预览渲染与版面目检

```bash
soffice --headless --convert-to pdf <deck>.pptx
pdftoppm -png -r 100 <deck>.pdf preview
```

- 工具缺失（`soffice` / `pdftoppm`）时**不阻塞交付**，但必须在质量门摘要中披露"版面未经渲染目检"
- 安装提示（一次性告知用户）：`brew install --cask libreoffice && brew install poppler`
- 渲染后逐页目检，checklist 复用 [quality-gates.md](quality-gates.md) §2（版面门）

目检补充细则（PNG 预览特有的检查点）：🔲 待填

---

## §6 · 依赖

- Python 3.9+，`python-pptx`（`pip install python-pptx`）
- 预览渲染（可选）：LibreOffice（soffice）+ poppler（pdftoppm）
