# 归档说明（2026-08-27）

本目录存放 mbb-deck 旧版框架与 PPTX 路径，均已**停止维护**，仅作恢复用途。

## 归档原因

| 文件 | 归档原因 |
|---|---|
| 旧 `SKILL.md` + 旧 references 5 件（routing / design-system / layout-catalog / narrative / quality-gates） | 建于 skills整合.md 初稿之上的留白框架（`🔲 待填` × 121），其前提与《skills整合-取舍反馈.md》裁决冲突：画布按 1920×1080 设计（已确认值是 1600×900）、设计系统按三套 MBB 配色预设设计（已确认用品牌蓝灰，不封预设）、字级按整合稿 pt 值（画布换算后为假冲突）。新骨架以内部分析定稿的已确认规则为底座重建 |
| `pptx-generation.md` + `generate_pptx.py` | PPTX 生成路径。反馈四条落地动作全部指向 HTML 路线，foundation 明确「原生 PPTX 暂不纳入」；经用户确认归档搁置 |
| `deck-template.html` | 旧 1920×1080 脚手架，被 assets/base-deck.html（1600×900，foundation 版）替代 |

## 若要恢复

- 恢复 PPTX 路径：把 `pptx-generation.md` 移回 `references/`、`generate_pptx.py` 移回 `scripts/`，并在 SKILL.md 恢复 Step 5B 分支；注意其主题色值需先改为品牌蓝灰、画布令牌改 1600×900
- 恢复旧框架：无必要，旧 references 中的整合稿素材已按反馈裁决吸收进新骨架的 layout-routing.md / storyline.md
