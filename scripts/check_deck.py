#!/usr/bin/env python3
"""
mbb-deck · 机械质量校验（check_deck.py）

对单文件 HTML deck 做无需浏览器渲染的静态机械校验。检查项对应
references/qa-gates.md「机械检查」节（foundation.md §7 禁用模式的可机械化子集）：

  [blocker] div 平衡       -- <div> 与 </div> 数量差 = 0（不闭合会静默破坏分页）
  [blocker] 零依赖自包含    -- 不得引用任何外部资源（src/href/url()/@import 中的外链）
  [blocker] 禁用模式        -- emoji / 玻璃拟态 backdrop-filter
  [warning] 循环动效        -- animation 含 infinite（foundation §6 禁止循环）
  [warning] 厚圆角          -- border-radius ≥ 24px（foundation §7 禁用厚圆角卡片）
  [warning] 16:9 画布       -- 静态确认 1600×900 与 overflow:hidden 的存在
  [warning] 结构识别        -- .slide 页数、每页标题元素、DOCTYPE/title
  [blocker] 翻页交互        -- 多页 deck 必须带 #nav 控件（纯键盘导航不可发现，
                              2026-08-28 员工实测反馈"只有一页"后补入）；缺滚轮
                              监听为 warning

用法：
  python check_deck.py <deck.html> [--json]

退出码：0 = 无 blocker；1 = 存在 blocker；2 = 用法/文件错误。
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 禁用模式（可机械检测子集，来源：foundation.md §6/§7）
# ---------------------------------------------------------------------------

# 每项：(正则, 级别, 说明)。级别取 "blocker" / "warning" / "advisory"。
BANNED_PATTERNS = [
    # emoji 图形（Miscellaneous Symbols / Dingbats / Emoji 块；
    # 箭头与几何形状如 ←→▲▼ 是合法逻辑符号，不在禁用范围，故不计入）
    ("[\\U0001F300-\\U0001FAFF\\u2600-\\u26FF\\u2700-\\u27BF]", "blocker", "emoji（foundation §7）"),
    # 玻璃拟态
    (r"backdrop-filter\s*:", "blocker", "玻璃拟态 backdrop-filter（foundation §7）"),
    # 循环动效（foundation §6：禁止循环）
    (r"animation[^;]*\binfinite\b", "warning", "循环动效 infinite（foundation §6）"),
]

# ---------------------------------------------------------------------------
# 已固化的机械检查
# ---------------------------------------------------------------------------

EXTERNAL_REF = re.compile(
    r"""(?:src|href)\s*=\s*["']          # 属性引用
        (\s*(?:https?://|//[^\s"']))     # http(s):// 或协议相对 //
        |url\(\s*["']?\s*(?:https?://|//)  # CSS url() 外链
        |@import\s+["']?\s*(?:https?://|//)  # CSS @import 外链
    """,
    re.VERBOSE,
)


def check_div_balance(html: str) -> list[dict]:
    """30x 质量门：div 开闭标签数量差必须为 0。"""
    opens = len(re.findall(r"<div\b", html))
    closes = len(re.findall(r"</div\s*>", html))
    if opens != closes:
        return [{
            "level": "blocker",
            "check": "div_balance",
            "message": f"<div> {opens} 个 vs </div> {closes} 个，数量差 {opens - closes}（不闭合会静默破坏分页）",
        }]
    return []


def check_self_contained(html: str) -> list[dict]:
    """输出契约：单文件零外部依赖。"""
    findings = []
    for m in EXTERNAL_REF.finditer(html):
        findings.append({
            "level": "blocker",
            "check": "self_contained",
            "message": f"检测到外部资源引用：{m.group(0)[:60]}…（须内嵌，零依赖）",
        })
    return findings


def check_canvas(html: str) -> list[dict]:
    """静态确认 1600×900 画布与溢出隐藏（无法替代逐页渲染目检，仅作初筛）。"""
    findings = []
    if not re.search(r"1600", html) or not re.search(r"900", html):
        findings.append({
            "level": "warning",
            "check": "canvas_16x9",
            "message": "未检出 1600×900 画布声明（可能使用缩放方案，需人工确认严格 16:9）",
        })
    if not re.search(r"overflow\s*:\s*hidden", html):
        findings.append({
            "level": "warning",
            "check": "canvas_16x9",
            "message": "未检出 overflow:hidden（可能产生纵向滚动，违反无滚动约束）",
        })
    return findings


def check_structure(html: str) -> list[dict]:
    """结构识别：.slide 页数、每页标题元素、DOCTYPE/title（对模板系 deck 有效）。"""
    findings = []
    parts = re.split(r'(<section[^>]*class="[^"]*\bslide\b[^>]*>)', html)
    tags = parts[1::2]
    slides = parts[2::2]
    if not slides:
        findings.append({
            "level": "warning",
            "check": "structure",
            "message": "未识别到 .slide 页结构（非 mbb-deck 模板产出？仅跳过页级检查）",
        })
        return findings
    for i, (tag, chunk) in enumerate(zip(tags, slides), 1):
        # 截到下一页边界，避免把整篇算进单页
        body = chunk.split("</section>")[0]
        # BD 固定页（bd-slide）为 pptx 机械还原，无 title-zone 结构，跳过标题门
        is_fixed = 'bd-slide' in tag
        if not is_fixed and not re.search(r"<h[1-3]\b|class=\"[^\"]*title", body):
            findings.append({
                "level": "warning",
                "check": "structure",
                "message": f"第 {i} 页未检出标题元素（action title 缺失 = 内容质量门 blocker，请人工复核）",
            })
    if "<!DOCTYPE html>" not in html:
        findings.append({"level": "warning", "check": "structure", "message": "缺少 <!DOCTYPE html>"})
    if not re.search(r"<title>[^<]+</title>", html):
        findings.append({"level": "warning", "check": "structure", "message": "缺少非空 <title>"})
    return findings


def check_banned_patterns(html: str) -> list[dict]:
    """禁用模式扫描（foundation §6/§7 可机械检测子集）。"""
    findings = []
    for pattern, level, desc in BANNED_PATTERNS:
        n = len(re.findall(pattern, html, re.IGNORECASE))
        if n:
            findings.append({
                "level": level,
                "check": "banned_pattern",
                "message": f"命中禁用模式「{desc}」× {n} 处",
            })
    return findings


def check_nav_interaction(html: str) -> list[dict]:
    """多页 deck 必须带可发现的翻页交互（控件 + 滚轮/触控）。

    2026-08-28 员工实测反馈"HTML 只有一页"：deck 实际 7 页俱在，但翻页仅绑定
    键盘方向键，鼠标滚轮与触控无响应、无可见控件--对非键盘用户等同单页死路。
    此后 #nav 控件与 wheel 监听成为多页 deck 的机械门。
    """
    slides = re.split(r'<section[^>]*class="[^"]*\bslide\b', html)[1:]
    if len(slides) <= 1:
        return []
    findings = []
    if 'id="nav"' not in html:
        findings.append({
            "level": "blocker",
            "check": "nav_interaction",
            "message": f"多页 deck（{len(slides)} 页）缺少 #nav 翻页控件：纯键盘导航不可发现，鼠标用户无法翻页",
        })
    elif "addEventListener('wheel'" not in html and 'addEventListener("wheel"' not in html:
        findings.append({
            "level": "warning",
            "check": "nav_interaction",
            "message": "未检出滚轮翻页监听（wheel），建议随 #nav 控件一并补齐",
        })
    return findings


def check_thickness(html: str) -> list[dict]:
    """厚圆角扫描：border-radius ≥ 24px 视为厚圆角卡片（foundation §7）。"""
    findings = []
    for m in re.finditer(r"border-radius\s*:\s*(\d+(?:\.\d+)?)px", html):
        if float(m.group(1)) >= 24:
            findings.append({
                "level": "warning",
                "check": "thick_radius",
                "message": f"border-radius {m.group(1)}px ≥ 24px（厚圆角卡片，foundation §7 禁用）",
            })
    return findings


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------

def run(path: Path) -> list[dict]:
    html = path.read_text(encoding="utf-8", errors="replace")
    findings = []
    findings += check_div_balance(html)
    findings += check_self_contained(html)
    findings += check_canvas(html)
    findings += check_structure(html)
    findings += check_nav_interaction(html)
    # BD 固定页（bd-slide）是 pptx 机械还原：源文件的圆角/渐变/配色不受
    # foundation §7 禁用清单约束（foundation §7 适用范围条款），剥除后再扫描
    dynamic_html = re.sub(
        r'<section[^>]*bd-slide[^>]*>.*?</section>', '', html, flags=re.S)
    findings += check_banned_patterns(dynamic_html)
    findings += check_thickness(dynamic_html)
    return findings


LEVEL_ORDER = {"blocker": 0, "warning": 1, "advisory": 2}


def main() -> int:
    parser = argparse.ArgumentParser(description="mbb-deck 机械质量校验")
    parser.add_argument("deck", type=Path, help="待校验的单文件 HTML deck")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出发现清单")
    args = parser.parse_args()

    if not args.deck.is_file():
        print(f"错误：文件不存在或不可读：{args.deck}", file=sys.stderr)
        return 2

    findings = sorted(run(args.deck), key=lambda f: LEVEL_ORDER.get(f["level"], 3))

    if args.json:
        print(json.dumps({"file": str(args.deck), "findings": findings}, ensure_ascii=False, indent=2))
    else:
        counts = {"blocker": 0, "warning": 0, "advisory": 0}
        for f in findings:
            counts[f["level"]] = counts.get(f["level"], 0) + 1
        print(f"check_deck · {args.deck}")
        print(f"  发现：blocker {counts['blocker']} · warning {counts['warning']} · advisory {counts['advisory']}")
        for f in findings:
            print(f"  [{f['level']:>7}] {f['check']}: {f['message']}")
        if not findings:
            print("  机械校验全部通过（语义与渲染质量由 qa-gates.md 六门负责）")

    return 1 if any(f["level"] == "blocker" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
