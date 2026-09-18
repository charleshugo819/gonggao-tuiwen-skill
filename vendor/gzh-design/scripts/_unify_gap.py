#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一「段间距」为 2.5em（= 35px @ 14px 正文，与行高 2.5 同值）。

只改**正文段落组件**的间距，不动卡片/表格/列表等组件的内边距——
那些 margin 属于组件自身留白，不是段间距。

各主题机制不同：
  - 红白 / 摸鱼绿 / 摸鱼票据 / 石墨 / 禅意：段间距写在正文 <p> 的 margin-bottom 上
  - 橄榄手记：正文 <p> 自身 margin:0，间距来自外层 <section style="margin-top:24px;">
    的包裹盒，所以改的是那层包裹盒（只改「正文段落」「新旧对照段落」两个组件）

幂等：已经是 2.5em 的会跳过。

用法：python _unify_gap.py
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "references")

# (文件, 旧, 新) —— 直接字符串替换
RULES = [
    ("theme-red-white.md",
     "margin-bottom:20px;font-size:14px;line-height:2.5",
     "margin-bottom:2.5em;font-size:14px;line-height:2.5"),
    ("theme-moyu-green.md",
     "margin-bottom:16px;font-size:14px;line-height:2.5",
     "margin-bottom:2.5em;font-size:14px;line-height:2.5"),
    ("theme-moyu-green.md",
     "段间距较大时用 `margin-bottom:24px`。",
     "段间距统一 `margin-bottom:2.5em`（= 35px @14px，与行高同值）；确实需要更松时才用到 `3em`。"),
    ("theme-moyu-ticket.md",
     "font-size:14px;color:#555;line-height:2.5;margin-bottom:16px;text-align:justify;",
     "font-size:14px;color:#555;line-height:2.5;margin-bottom:2.5em;text-align:justify;"),
    ("theme-graphite-minimal.md",
     "margin-bottom:22px;font-size:14px;line-height:2.5",
     "margin-bottom:2.5em;font-size:14px;line-height:2.5"),
    ("theme-zen-whitespace.md",
     "margin-bottom: 26px;font-size: 14px;line-height: 2.5",
     "margin-bottom: 2.5em;font-size: 14px;line-height: 2.5"),
    ("theme-zen-whitespace.md",
     "段落间距：          26px+",
     "段落间距：          2.5em（35px，与行高同值）"),
    ("theme-zen-whitespace.md",
     "段落间距 26px+，字里行间充满呼吸感。",
     "段落间距 2.5em，字里行间充满呼吸感。"),
]

# 橄榄手记：按组件章节定位，只改该组件内的外层包裹盒
OLIVE_SECTIONS = [
    ("## 组件 10 正文段落 richtext-paragraph", "## 组件 11 行内代码段落 inline-code-paragraph"),
    ("## 组件 12 新旧对照段落 before-after-paragraph", "## 组件 13 无序列表 bullet-list-basic"),
]
OLIVE_OLD = '<section style="margin-top:24px;">'
OLIVE_NEW = '<section style="margin-top:2.5em;">'


def apply_rules():
    stats = {}
    for fn, old, new in RULES:
        p = os.path.join(REF, fn)
        s = open(p, encoding="utf-8").read()
        n = s.count(old)
        if n:
            s = s.replace(old, new)
            open(p, "w", encoding="utf-8").write(s)
        stats.setdefault(fn, []).append(("替换" if n else "已是/未命中", n))
        print("  %-30s x%-3d %s" % (fn, n, old[:58]))
    return stats


def apply_olive():
    p = os.path.join(REF, "theme-olive-journal.md")
    s = open(p, encoding="utf-8").read()
    total = 0
    for start, end in OLIVE_SECTIONS:
        i, j = s.find(start), s.find(end)
        if i < 0 or j < 0 or j <= i:
            print("  !! 橄榄手记 定位失败:", start[:30])
            continue
        chunk = s[i:j]
        n = chunk.count(OLIVE_OLD)
        chunk = chunk.replace(OLIVE_OLD, OLIVE_NEW)
        s = s[:i] + chunk + s[j:]
        total += n
        print("  %-46s x%d 包裹盒 → 2.5em" % (start[:44], n))
    open(p, "w", encoding="utf-8").write(s)
    return total


def main():
    print("直接替换（正文段落自身的 margin-bottom）")
    apply_rules()
    print("\n橄榄手记（改包裹盒 margin-top）")
    apply_olive()
    print("\n完成。段间距 = 2.5em（35px @14px）。")


if __name__ == "__main__":
    main()
