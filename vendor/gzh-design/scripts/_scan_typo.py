# -*- coding: utf-8 -*-
"""
排版参数体检工具。

扫描各主题文件的字号 / 行高 / 字间距，找出没统一到
14px / 2.5 / 2px 的残留；同时全库扫描 font-family，
找出非系统默认字体（代码块等宽除外）。

改完排版参数或字体后先跑这个，再跑 component_lint.py。

用法：python _scan_typo.py
"""
import os
import re
import sys
import collections

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "references")
FILES = [
    "theme-red-white.md", "theme-moyu-green.md", "theme-moyu-ticket.md",
    "theme-olive-journal.md", "theme-graphite-minimal.md", "theme-zen-whitespace.md",
    "common-components.md",
]

TARGET_SIZE = "14"
TARGET_LH = "2.5"
TARGET_LS = "2px"

SYS = ("-apple-system,BlinkMacSystemFont,'PingFang SC',"
       "'Hiragino Sans GB','Microsoft YaHei',sans-serif")

print("#" * 68)
print("# 一、字号 / 行高 / 字间距")
print("#" * 68)
for fn in FILES:
    p = os.path.join(REF, fn)
    s = open(p, encoding="utf-8").read()
    tight = len(re.findall(r"font-size:\d+px", s))          # 无空格写法
    loose = len(re.findall(r"font-size:\s+\d+px", s))       # 带空格写法
    lh = collections.Counter(re.findall(r"line-height:\s*([\d.]+)", s))
    ls = collections.Counter(re.findall(r"letter-spacing:\s*([\d.]+px)", s))
    sizes = collections.Counter(re.findall(r"font-size:\s*(\d+)px", s))
    # 15/16/17/18/21/22/24/26/30/39/45 都是合法的组件层级值（引言金句/章节标题/装饰），
    # 只有 9/10（低于可读下限）与 19/32（旧的正文基准残留）才算异常。
    legacy = {k: v for k, v in sizes.items() if k in ("9", "10", "19", "32")}
    print("=" * 68)
    print(fn)
    print("  font-size 无空格 %d 处 / 带空格 %d 处" % (tight, loose))
    print("  字号分布:", dict(sorted(sizes.items(), key=lambda x: int(x[0]))))
    print("  行高:", dict(sorted(lh.items())))
    print("  字间距:", dict(sorted(ls.items())))
    if legacy:
        print("  ⚠️ 疑似旧值残留:", legacy)
    if loose:
        print("  ⚠️ 带空格写法 %d 处——历史上正是这种写法导致整篇漏改，确认是否需要统一" % loose)

print()
print("#" * 68)
print("# 二、段间距（正文段落应为 2.5em；卡片内段落 margin:0 属正常）")
print("#" * 68)
for fn in FILES:
    s = open(os.path.join(REF, fn), encoding="utf-8").read()
    gap = collections.Counter()
    for m in re.finditer(r'<p style="([^"]*)"', s):
        st = m.group(1)
        if not re.search(r"font-size\s*:\s*14px", st):
            continue
        if not re.search(r"line-height\s*:\s*2\.5", st):
            continue
        mg = re.search(r"margin-bottom\s*:\s*([^;\"]+)", st)
        if mg:
            gap[mg.group(1).strip()] += 1
        else:
            mg2 = re.search(r"margin\s*:\s*([^;\"]+)", st)
            gap["margin:" + mg2.group(1).strip() if mg2 else "无 margin"] += 1
    print("  %-30s %s" % (fn, dict(gap)))
print("  说明：非 2.5em 的都属于卡片 / 列表 / 时间线内部的段落（块内间距），属正常；")
print("        橄榄手记的正文段落 <p> 自身 margin:0，段间距由外层包裹盒 margin-top:2.5em 提供。")

print()
print("#" * 68)
print("# 三、font-family 全库扫描（代码块 monospace 与系统栈为正常）")
print("#" * 68)
bad = 0
checked = 0
for root, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in (".git", "_bak_typo", "archive", "node_modules")]
    for f in sorted(files):
        if not f.endswith((".md", ".html")):
            continue
        fp = os.path.join(root, f)
        rel = os.path.relpath(fp, ROOT)
        try:
            t = open(fp, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for m in re.finditer(r'font-family\s*[:=]\s*"?([^;\"\n}]+)', t):
            v = m.group(1).strip()
            if "monospace" in v.lower():
                continue
            if re.search(r"[\u4e00-\u9fff]", v):
                # 说明文字里提到「font-family: 与」这类句子，不是真的字体声明
                continue
            checked += 1
            if v != SYS:
                bad += 1
                print("  ✗ %-44s %s" % (rel, v[:80]))
        # 字体名关键词只在组件库 / 画廊 / 预览资源里查；SKILL.md、README.md 等
        # 说明文档需要提到这些名字来解释「为什么不用」，属正常。
        if rel.startswith(("references", "docs", "assets")):
            for kw in ("IBM Plex", "Noto Serif", "Songti SC", "Source Han", "YouSheBiaoTiHei"):
                if kw in t:
                    bad += 1
                    print("  ✗ %-44s 文档残留字体名: %s" % (rel, kw))
print("  系统栈声明 %d 处，非系统字体残留 %d 处" % (checked - bad if checked >= bad else checked, bad))
if bad == 0:
    print("  ✅ 全部为系统默认字体（代码块等宽除外）")
