---
name: mbb-deck
description: 生成 MBB 咨询风（麦肯锡/BCG/贝恩风格）汇报 deck，双输出路径：单文件 HTML（1920×1080、16:9、内嵌 CSS、零依赖）或原生可编辑 PPTX（16:9，文本框/表格/图表均为原生对象）。当用户要求把报告、研究、分析结论或业务汇报材料做成咨询风演示（"麦肯锡风 / MBB 风 / 咨询风 PPT / deck / 汇报页"）时使用。核心机制：data-shape 强制中间产物 -> 版式路由表 -> SCQA 组装 -> 双 Agent 质量门；两条输出路径共用同一语义层（plan.json）。
---

# MBB 风 Deck（HTML / PPTX 双路径）

## 定位与输出契约

- **双输出路径**，Step 0 第一问确认：
  - **HTML**（默认）：单个 HTML 文件，内嵌全部 CSS，零外部依赖（无 CDN、无外链字体、无外链图片），1920×1080（16:9）严格无纵向滚动，键盘 <-/-> 翻页
  - **PPTX**：16:9（13.333"×7.5"）.pptx，文本框/表格/图表均为**原生可编辑对象**（非图片贴片）；由 `scripts/generate_pptx.py` 从 plan.json 确定性渲染
- **两路共用同一语义层**：governing thought、data-shape、版式路由、plan.json（Step 1–4 与格式无关）；格式只决定 Step 5 的渲染方式
- **交付物**：`<主题>-deck.html` 或 `<主题>-deck.pptx` + 质量门结果摘要（blocker 清零情况 + 未修 warning 披露）

## 5 条铁律（全流程贯穿）

1. **Action Title**--每页标题是带主语、含义完整的结论句，永不做话题标签
2. **One slide, one argument**--一页只承担一个沟通任务、推进一个论点
3. **两段式路由**--绝不直接"看内容选版式"；必须先产出 data-shape 强制中间产物，再查路由表匹配版式
4. **容量先校验**--先验证内容装不装得下，再渲染；超容换版式或拆页，永不缩字号硬塞
5. **判定规则封闭**--风格、输出格式等参数由用户显式指定，禁止模型自判（实测自判两次会得出不同结论）

弱/强标题对照、字数约束等细则见 [references/narrative.md](references/narrative.md) 与 [references/design-system.md](references/design-system.md)。

## 工作流（Step 0–7）

### Step 0 · 参数确认（AskUserQuestion，封闭枚举）

一次性向用户确认四个参数。选项必须来自封闭清单，不给自由发挥项：

| 参数 | 选项 | 默认 |
|---|---|---|
| **输出格式** | HTML 单文件 / PPTX 原生可编辑 | HTML |
| 风格预设 | A Executive Classic / B McKinsey Navy / C MBB Navy-Teal（定义见 design-system.md §1） | A |
| 叙事脊柱 | SCQA / What-SoWhat-NowWhat / Diagnosis-Choice-Mobilization / Hypothesis-Evidence-Implication（适用场景见 narrative.md §2） | 按内容类型推荐一项并给理由 |
| 页数配方 | 研究摘要配方 / 战略决策配方 / 用户自定页数（配方见 narrative.md §7） | 按内容类型推荐 |

**输出格式判定规则**：用户已明确要 .pptx / PowerPoint / "发给别人改" -> PPTX，不再询问；已明确要网页 / HTML / 零依赖 -> HTML；未明确 -> 询问，并附取舍提示（PPTX = 收件方原生可编辑、企业环境通用；HTML = 零依赖、渲染保真、不依赖 Office）。

其余三个参数：用户拒绝选择时采用默认值，并在交付说明中显式披露"未指定，已用默认 X"。

> **Step 1–4 与输出格式无关**：governing thought、data-shape、路由、plan.json 是语义层，两条路径共用同一份产物。plan.json 顶部写入 `format` 字段。

### Step 1 · Governing Thought（先于一切页面设计）

写一句能回答听众核心问题的中心论点，要求：具体到可以被反驳、有证据支撑、与决策相关、短到能凭记忆复述。质量标准与反例见 [references/narrative.md](references/narrative.md) §1。

产出的 governing thought 写入 plan.json 顶部（Step 3），后续每页标题都必须服务它。

### Step 2 · data-shape 抽取（强制中间产物 #1，不许跳过）

把输入材料**强制归类**为 9 类封闭 data-shape 之一或若干（禁止"其他"类）。识别特征表见 [references/routing.md](references/routing.md) §1。

产出 `shapes.json`（字段契约见 routing.md §4）。

> 为什么不许跳过：跳过中间产物，版式选择就退化为"看内容猜版式"--这是对 8 套竞品拆解后确认的核心失败模式（整合稿铁律 3）。

### Step 3 · 查路由表选版式（强制中间产物 #2 = plan.json）

对每个 shape 查 [references/routing.md](references/routing.md) §2 路由表，逐条执行三段判定：

1. **Use when / Don't use when**--确认该版式适配
2. **相邻版式辩护**--写一句"为什么不是隔壁那个版式"
3. **Capacity 校验**--内容量超容则换版式或拆页，不缩字号

产出 `plan.json`（deck 级：format + governing thought + 叙事脊柱 + 页清单；页级：layout + shape + not + fit_check；字段契约见 routing.md §4）。plan.json 同时是 Step 6 质量门的对照基准；**PPTX 路径下它还是生成器的直接输入**（Step 5B 扩展至内容级）。

### Step 4 · 组装单页骨架

- 单页分区骨架：`Action Title -> [Why 背景区] -> [How 主体区] -> [So-What 成果区]`（SCQA 落位规则见 routing.md §5）
- **主版式**由承载核心论点的 shape 决定；次要 shape 降为辅助区，用"能承载结论的最小版式"压缩
- 每页指派一个页面角色（orient / assert / prove / compare / explain / decide / mobilize / reference，定义见 narrative.md §5）
- **proof-object-first**：每个论点配一个承载论证的视觉结构，而非卡片+图标+bullet 堆叠（narrative.md §8）

### Step 5A · HTML 路径：Claude 直写 HTML

- 从 `assets/deck-template.html` 拷贝脚手架（设计令牌、网格、标题带/页脚带、翻页逻辑已在模板内）
- 版式按 [references/layout-catalog.md](references/layout-catalog.md) 的组件契约实现（含双层系统：Layer 1 数据层 + Layer 2 洞察标注层，overlay 一页 ≤ 2 种）
- 设计执行按 [references/design-system.md](references/design-system.md)：用户选定的预设配色、字级表、网格间距、禁用模式清单
- 数字全 deck 前后一致；每个数据页带来源注

### Step 5B · PPTX 路径：plan.json -> 生成器渲染

工作路径参考 lampertb / mbb-decks / mckinsey-pptx 三套 PPTX skill 的共识流程，细则见 [references/pptx-generation.md](references/pptx-generation.md)：

1. **扩展 plan.json 至内容级**：在 Step 3 的页骨架上，为每页补齐 slide 内容字段（版式专属字段 + Layer 2 overlays），字段契约见 pptx-generation.md §2/§3
2. **依赖自检**（每次运行前）：
   ```bash
   python3 -c "import pptx; print(pptx.__version__)"
   ```
   失败则提示用户 `pip install python-pptx`，不擅自继续
3. **生成**：
   ```bash
   python scripts/generate_pptx.py --plan plan.json --output <主题>-deck.pptx
   ```
4. **审读质量告警并迭代**：生成器输出机械质量告警；发现问题**改 plan.json 重跑，不手改 .pptx 产物**（手改内容会在下次重生成时丢失）

### Step 6 · 双 Agent 质量门（并行）+ 机械校验

派出两个并行 Agent，各持一份 checklist，**互不知晓对方结论**：

| 环节 | HTML 路径 | PPTX 路径 |
|---|---|---|
| Agent 1 · 内容门 | 共用：读 plan.json + 全部 action title 连读（checklist：[quality-gates.md](references/quality-gates.md) §1） | 同左 |
| Agent 2 · 版面门 | 浏览器渲染逐页目检（checklist：quality-gates.md §2） | 先渲染 PNG 预览再逐页目检（见下） |
| 机械校验 | `python scripts/check_deck.py <deck.html>` | 生成器自带质量告警（Step 5B 第 4 步） |

PPTX 的 PNG 预览渲染（mckinsey-pptx 模式）：

```bash
soffice --headless --convert-to pdf <deck>.pptx && pdftoppm -png -r 100 <deck>.pdf preview
```

`soffice`/`pdftoppm` 缺失时**不阻塞交付**，但必须在质量门摘要中披露"版面未经渲染目检"。

发现分级处理：`blocker` 必须修复才能交付；`warning` 须显式披露；`advisory` 酌情。

### Step 7 · 整合反馈定稿

1. 汇总两个 Agent + 机械校验的全部发现，逐条修复，blocker 清零（PPTX 路径的修复 = 改 plan.json 重生成）
2. 复跑机械校验确认机械项通过
3. 交付 `<主题>-deck.html` 或 `<主题>-deck.pptx`（可附 PNG 预览）+ 质量门摘要（含未修 warning 的披露）
4. 询问用户是否需要局部调整；HTML 路径做精准局部代码修改，PPTX 路径改 plan.json 重生成

## 附件导航（渐进式披露）

| 附件 | 何时用 | 用法 |
|---|---|---|
| [references/routing.md](references/routing.md) | Step 2–4 | 读入上下文，照表执行 |
| [references/narrative.md](references/narrative.md) | Step 1、Step 4 | 读入上下文 |
| [references/layout-catalog.md](references/layout-catalog.md) | Step 5A | 写 HTML 时读入 |
| [references/pptx-generation.md](references/pptx-generation.md) | Step 5B | 走 PPTX 路径时读入 |
| [references/design-system.md](references/design-system.md) | Step 5A / 5B | 渲染时读入（两路的视觉规范同源） |
| [references/quality-gates.md](references/quality-gates.md) | Step 6 | 分发给两个校对 Agent |
| [assets/deck-template.html](assets/deck-template.html) | Step 5A | 拷贝为起点，不整体读入上下文 |
| [scripts/generate_pptx.py](scripts/generate_pptx.py) | Step 5B | 直接执行，不读入上下文 |
| [scripts/check_deck.py](scripts/check_deck.py) | Step 6（HTML 路径）、Step 7 | 直接执行，不读入上下文 |

## 当前状态：框架版（约束留白）

本 skill 目前为**框架版**：工作流、文件结构、中间产物契约已定；所有 references 中标注 `🔲 待填` 的约束内容（识别特征、路由条目、配色值、字级、质量门清单、评分卡等）尚未回填。

**框架版使用限制**：约束未回填前，Step 2–3 的分类与路由、Step 5 的设计执行无细则可依，产出不保证 MBB 品质；Step 6 的两个 Agent checklist 为空，质量门不生效。可用的机械部分：`check_deck.py`（div 平衡、16:9、自包含）、`generate_pptx.py`（plan.json 校验、依赖自检、16:9 结构骨架渲染；版式内容渲染待 pptx-generation.md §3 映射表定稿）。

留白点统一以 `🔲 待填` 标记，可用 `grep -rn "待填" .` 清点；每个留白处注明来源章节（`skills整合.md` 对应部分），回填时按图索骥。
