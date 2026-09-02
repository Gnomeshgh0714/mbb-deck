#!/usr/bin/env python3
"""拼装 BD 固定页 demo：把 7 个模板页拼进 base-deck 骨架，图片 base64 内嵌。
用法：python3 build_bd_demo.py [输出路径]
"""
import base64
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # skill 根
BD = os.path.join(HERE, "assets", "templates", "bd")
BASE_DECK = os.path.join(HERE, "assets", "base-deck.html")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(HERE), "BD固定页-试组装demo.html")

# 2026-09-02 起模板为 pptx 机械还原版；占位符集见 assets/templates/bd/README.md
PAGES = [
    ("toc.html", {"{{TOC_ITEM_1}}": "项目初步理解", "{{TOC_ITEM_2}}": "项目服务方案",
                  "{{TOC_ITEM_3}}": "公司及项目经验介绍"}),
    ("section.html", {"{{SECTION_NO}}": "01", "{{SECTION_TITLE}}": "项目初步理解"}),
    ("advantage.html", {"{{ADV_COUNT}}": "3", "{{CLIENT_NAME}}": "某客户集团",
                        "{{ADV_1_TITLE}}": "更懂国资要求",
                        "{{ADV_1_DESC}}": "作为中国成立最早、规模最大、实力最强的综合性国资咨询机构，备受高层领导关注和支持，国资改革话题经验丰富",
                        "{{ADV_2_TITLE}}": "更懂最佳实践",
                        "{{ADV_2_DESC}}": "持续导入来自全球顶级咨询公司的国际化团队成员，更具国际视野",
                        "{{ADV_3_TITLE}}": "安全可靠的长期陪伴服务",
                        "{{ADV_3_DESC}}": "团队依托国资优势及系统化服务升级，争取成为客户不可或缺的“外部智库”与紧密合作伙伴"}),
    ("company.html", {}), ("thinktank.html", {}), ("soe.html", {}), ("service.html", {}),
]

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def extract(template, placeholder_map):
    """取出 PAGE 样式块与拼装段，替换占位符与图片路径。"""
    css = re.search(r'<style id="bd-[^"]+-css">(.*?)</style>', template, re.S)
    seg = re.search(r'<!-- 拼装起点 -->(.*?)<!-- 拼装终点 -->', template, re.S)
    if not css or not seg:
        raise RuntimeError("模板缺少 PAGE 样式块或拼装段")
    html = seg.group(1)
    for k, v in placeholder_map.items():
        html = html.replace(k, v)

    def to_data_uri(m):
        src = m.group(1)
        p = os.path.join(BD, src)
        ext = os.path.splitext(src)[1].lower()
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return 'src="data:%s;base64,%s"' % (MIME.get(ext, "application/octet-stream"), b64)

    # 三种图片引用形式统一内嵌：<img src> / <svg><image href> / CSS background:url()
    def to_data_uri_css(m):
        src = m.group(1)
        p = os.path.join(BD, src)
        ext = os.path.splitext(src)[1].lower()
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return "url(data:%s;base64,%s)" % (MIME.get(ext, "application/octet-stream"), b64)
    html = re.sub(r'src="(img/[^"]+)"', to_data_uri, html)
    html = re.sub(r'href="(img/[^"]+)"', lambda m: to_data_uri(m), html)
    html = re.sub(r'url\((img/[^)]+)\)', to_data_uri_css, html)
    return css.group(1), html


def main():
    base = read(BASE_DECK)
    all_css, sections = [], []
    for fname, ph in PAGES:
        css, html = extract(read(os.path.join(BD, fname)), ph)
        all_css.append(css.strip())
        sections.append(html.strip())

    # 第一个 slide 激活
    sections[0] = sections[0].replace('<section class="slide', '<section class="slide active', 1)

    # 替换 base-deck 的示例 slide 区
    demo = base.replace("{{DECK_TITLE}}", "BD 固定页 · 试组装 Demo")
    demo = re.sub(
        r'<section class="slide active".*?</section>',
        "\n".join(sections) + "\n      ", demo, count=1, flags=re.S)
    # 注入页级样式
    demo = demo.replace("</head>", "<style>\n" + "\n".join(all_css) + "\n  </style>\n</head>")

    out = os.path.abspath(OUT)
    with open(out, "w", encoding="utf-8") as f:
        f.write(demo)
    print(f"OK -> {out}  ({os.path.getsize(out)/1024/1024:.2f}MB)")

    # 机械校验
    residue = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", demo)))
    print("占位符残留:", residue if residue else "无")
    imgs = len(re.findall(r'(src|href)="img/', demo)) + len(re.findall(r'url\(img/', demo))
    print("未内嵌图片引用:", imgs)


if __name__ == "__main__":
    main()
