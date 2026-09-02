<div align="center">

# mbb-deck

**MBB 咨询风汇报 Deck 生成技能（Claude Code Skill）**

输入文字素材或已有 PPT，输出可直接汇报的 16:9 咨询风翻页 HTML

![Claude Code](https://img.shields.io/badge/Claude_Code-原生_Skill-0A3D8A)
![跨平台](https://img.shields.io/badge/跨平台-OpenAI_WorkBuddy_等-0E58C4)
![交付形态](https://img.shields.io/badge/交付形态-单文件_HTML-17233B)
![机械检查](https://img.shields.io/badge/机械检查-溢出_重叠_数据读回-4C5568)
![License](https://img.shields.io/badge/License-MIT-4A8EF2)

</div>

---

## 这是什么

一套自研的咨询风 deck 生成系统：把报告、研究、分析结论或已有 PPT 转化为深浅不一品牌蓝配色的 16:9 演示页。

核心设计立场：**skill 提供判断标准，不把内容机械套入固定模板**。几何、字级、文本框行数预算是硬规则并用脚本复核；版式由「内容理解 -> 版式选择」两段式路由自主决定；观感上限由校准范例携带，不假装规则能覆盖审美。

两种工作模式：

- **逐页转换模式**（默认）：已有 PPT、逐页 dummy 或明确页级结构时，页数、页序、Action Title、数字与来源按输入保留，只升级视觉；契约见 `references/strict-conversion.md`
- **内容重组模式**：用户明确要求重组、精简或重写 Storyline 时才进入

## 工作流

```
 文字素材 / 已有 PPT
    │
    ▼
 ① 理解输入     模式判定（逐页转换 / 内容重组）+ intake 解析
 ② 组织 Storyline   一句 governing thought，Action Title 连读成文
 ③ 形成单页逻辑     每页 9 字段内部契约（page_question / evidence / data_shape …）
 ④ 选择视觉结构     版式路由表为默认起点，不封闭；参考页保真可自定义结构
 ⑤ 设计与实现       proof-object-first，品牌蓝灰设计语法，1600×900 单文件
 ⑥ 验证与交付       QA 门 + 机械检查，逐页转换按源页面清单核对
    │
    ▼
 16:9 单文件 HTML（可打印 / reduced-motion 终态）
```

## BD 固定页包

面向 BD / 提案 / 商务拓展类材料的成品页资产（`assets/templates/bd/`），7 页两类：

| 类型 | 页面 | 用法 |
|---|---|---|
| 模板页（每次调整） | 目录页 · 章节页 · 优势总览页 | 换占位符（目录条目 / 章节名 / 客户名） |
| 固定页（直接可用） | 公司名片页 · 智库背书页 · 国资经验页 · 服务优势页 | 原样拼入，仅填页码 |

配套 `references/bd-pages.md` 收录从成熟提案提炼的组件模式集（Subtitle 变体 / 箭头流向 / 数字名片 / 三栏矩阵 / 阶段矩阵等），供论证部分自由组合。

> **公开版说明**：`assets/templates/bd/img/`（客户 logo 墙、活动照片等图片资产）不随公开仓库分发，私有部署时按该目录 README 从源材料提取。`assets/exemplars/` 同理不附带范例文件。

## 安装

```bash
# 全局安装
git clone https://github.com/Gnomeshgh0714/mbb-deck.git ~/.claude/skills/mbb-deck

# 或项目级安装（在 Claude Code 项目根目录）
git clone https://github.com/Gnomeshgh0714/mbb-deck.git .claude/skills/mbb-deck
```

## 使用

打开 [docs/标准调用prompt.md](docs/标准调用prompt.md)，按板块式模板改关键信息即可。味道长这样：

```
请根据我给你的内容，用 mbb-deck skill 输出一版汇报 deck，整体颜色以深浅不一的蓝色为主。

第一页：主标题是"<这页的结论句>"；
        左边放"<板块小标题>"，具体内容是<背景或现状>；
        中间第一部分核心内容是<小标题>，具体包括<支撑内容，数字带单位、时间、口径>；
        ……
        本页资料来源：<来源行>。
```

输入足够时直接推进，交付说明中披露关键假设；只有受众、事实口径或业务含义的不同解释会实质改变结果时才追问。做 BD 材料时可直接点名固定页包页面名（如「这次要用目录页、公司名片页和智库背书页」）。

### 交付前机械检查

```bash
python3 scripts/check_deck.py <产出.html>    # 边界 / 溢出 / 重叠 / 交互门
```

## 质量体系（三层）

| 层 | 职责 | 载体 |
|---|---|---|
| 硬规则层 | 几何 / 字级 / 文本框行数预算 | `references/foundation.md` |
| 机械验证层 | 边界、溢出、重叠、图表数据读回，发现即退回 | `scripts/check_deck.py` |
| 范例校准层 | 观感上限 | `assets/exemplars/`（**公开版不附带范例文件**，内部资产；私有部署时放入该目录，见其 README） |

三层各司其职：规则保正确性，脚本堵回归，范例定审美。

## 仓库结构

```
├── SKILL.md               # 技能入口：六步工作流 + 模式判定
├── references/            # 规则真源：foundation / storyline / page-logic / strict-conversion /
│                          # layout-routing / visual-language / qa-gates / bd-pages / open-questions
├── scripts/               # check_deck.py（纯标准库）· build_portable.py · build_bd_demo.py
├── assets/
│   ├── base-deck.html     # 起步模板（画布 / 翻页 / 打印）
│   ├── intake-form.md     # 输入解析参考（含 BD 固定页包清单）
│   ├── templates/bd/      # BD 固定页包：7 页成品模板（图片资产不随公开版分发）
│   └── exemplars/         # 校准范例（公开版不附带）
├── agents/openai.yaml     # OpenAI 兼容平台配置
├── archive/               # 旧版骨架归档（停止维护，仅作恢复参考）
└── docs/
    ├── 标准调用prompt.md      # 员工调用模板（平台无关）
    ├── 可移植prompt.md        # 单文件系统提示词（约48KB），任何平台直接粘贴
    └── 多平台部署指南.md      # 各平台接法与能力降级对照表
```

## 跨平台部署

规则本体平台无关--Claude Code 原生可用，也可用 [docs/可移植prompt.md](docs/可移植prompt.md) 部署到 OpenAI、WorkBuddy 等任何支持系统提示词的模型 / agent 平台。接法与能力降级对照见 [docs/多平台部署指南.md](docs/多平台部署指南.md)。

规则改动后重新生成可移植版，保持同源：

```bash
python3 scripts/build_portable.py docs/可移植prompt.md
```

## 路线图

- [ ] **范例资产**：扩充 3–4 个带设计决策标注的校准范例
- [ ] **BD 包扩展**：固定页内容更新机制（新材料驱动的数字/案例/照片更新流程）
- [ ] **QA 升级**：策展密度软门、构造级观感比对、盲测回归

## 开发参考

路由机制拆解自四个公开咨询风 skill：zairuilab/consulting-deck、appautomaton/presentation、lampertb/MBBDeckBuilderSkill、farhan85azad/bcg-slide-engine，在此致谢。

## License

[MIT](LICENSE)
