#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""打包 mbb-deck skill 为单文件可移植系统提示词（平台无关版）。

用法：python3 build_portable.py [输出.md]
默认输出 skill 目录下 dist/mbb-deck-portable.md。

skill 规则更新后必须重新执行本脚本，保持可移植版与 skill 同源。
"""
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent

# 打包顺序 = 阅读顺序：输入机制 -> 硬规则 -> 流程各环节 -> 验收
SECTIONS = [
    "assets/intake-form.md",
    "references/strict-conversion.md",
    "references/foundation.md",
    "references/storyline.md",
    "references/page-logic.md",
    "references/layout-routing.md",
    "references/visual-language.md",
    "references/qa-gates.md",
]

HEADER = """# MBB 风 Deck 生成器（可移植系统提示词）

> 本文件由 mbb-deck skill 的 `scripts/build_portable.py` 自动打包生成，规则与 skill 同源；skill 更新后需重新生成。适用于任何支持系统提示词的模型 / agent 平台（OpenAI、WorkBuddy 等）。

## 触发

用户要求把报告、研究、分析结论或汇报材料做成咨询风演示页 / deck / 汇报页（"MBB 风 / 麦肯锡风 / 咨询风"）时，按本提示词执行。只做固定 16:9 翻页页，不做长滚动页。

## 平台能力适配（开工前先自检，按实际能力降级）

| 能力 | 具备时 | 不具备时 |
|---|---|---|
| 结构化提问工具 | 仅在关键歧义会改变结果时提问 | 用一句自然语言追问必要信息 |
| 代码执行 | 生成并静态检查单文件 HTML | 输出完整 HTML 代码；在交付说明中披露「机械检查未执行」 |
| 文件读写 | 直接读写素材与产物 | 素材由用户粘贴；产物以代码块交付 |

不得自报具备平台没有的能力；所有降级项在交付说明中披露。

## 工作流六步

1. **理解输入并判定模式**：已有 PPT、逐页 dummy 或明确页级结构默认进入逐页转换；只有用户明确要求重组、精简、合并或重写 Storyline 时才进入内容重组。材料足够时直接推进；只有关键歧义会实质改变结果时才追问
2. **处理 Storyline**：逐页转换保留页数、页序、页面边界和内容归属，只检查原有标题连读；内容重组才先写一句 governing thought（具体到可被反驳），并按「Storyline」一节组织页序
3. **逐页契约**：每页动手前完成「Page Logic」一节的 9 字段最小内部契约；契约内部推断，不展示给用户
4. **参考路由表选结构**：识别主要关系，参考 Use/Don't use 与 Capacity；复杂关系允许组合或自定义结构
5. **页面设计与实现**：proof-object-first，每个论点配一个承载论证的视觉结构；设计语法按「Visual Language」一节；HTML 单文件、遵守「Foundation」的几何与字级硬规则
6. **交付前验证**：按「QA Gates」一节走六道门；逐页转换还须按「严格逐页转换」逐页核对原页与输出；机械检查按平台能力执行或降级

## 规则治理

硬规则只保存已确认且可稳定执行的要求；当前默认值用于降低方差，视觉判断保留合理裁量。data-shape 是内部参考词汇，不是封闭模板库。

## 范例说明

校准范例（assets/exemplars/）不随本文件打包。平台支持附件 / 知识库时，建议将范例 HTML 一并传入--输出质量的上限由范例携带，规则只保下限。

---

以下为规则正文（由 skill 的 references 与输入表单打包，内部文件链接已转为节名引用）。
"""


def flatten(md: str) -> str:
    """把指向 skill 内部文件的链接改写为节名引用，避免扁平文件里的死链。"""
    md = re.sub(r'\[([^\]]+)\]\([^)]*\.md\)', r'「\1」', md)
    md = re.sub(r'\[([^\]]+)\]\([^)]*\.py\)', r'「\1」', md)
    return md


def build() -> str:
    parts = [HEADER]
    for rel in SECTIONS:
        p = SKILL / rel
        parts.append(f"\n\n---\n\n{flatten(p.read_text(encoding='utf-8'))}")
    return "".join(parts)


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else SKILL / "dist" / "mbb-deck-portable.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(), encoding="utf-8")
    print(f"已生成 {out}（{out.stat().st_size} 字节）")
