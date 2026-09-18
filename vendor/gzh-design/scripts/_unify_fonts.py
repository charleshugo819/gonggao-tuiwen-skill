#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 gzh-design 全部主题/组件库/画廊页的 font-family 统一为系统默认无衬线栈。

规则（幂等，可反复运行）：
  - 任何 font-family 值 → 统一替换为 SYS 系统栈
  - 唯一例外：值里含 monospace 的（代码块 / 行内代码）保持等宽，因为这是
    功能性字体（对齐 + 视觉区分），不是装饰性字体选择。

用法：python _unify_fonts.py [--dry]
"""
import os
import re
import sys

SYS = ("-apple-system,BlinkMacSystemFont,'PingFang SC',"
       "'Hiragino Sans GB','Microsoft YaHei',sans-serif")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

TARGETS = [
    r"references\theme-olive-journal.md",
    r"references\theme-zen-whitespace.md",
    r"references\theme-red-white.md",
    r"references\theme-moyu-green.md",
    r"references\theme-moyu-ticket.md",
    r"references\theme-graphite-minimal.md",
    r"references\common-components.md",
    r"docs\gallery\olive-journal.html",
    r"docs\gallery\zen-whitespace.html",
    r"docs\gallery\red-white.html",
    r"docs\gallery\moyu-green.html",
    r"docs\gallery\moyu-ticket.html",
    r"docs\gallery\graphite-minimal.html",
    r"assets\theme-previews\theme-mono-blue-editorial.html",
]

RX = re.compile(r"(font-family\s*:\s*)([^;\"\n}]+)")


def convert(text):
    stats = {"sys": 0, "keep": 0}

    def sub(m):
        head, val = m.group(1), m.group(2)
        v = val.strip()
        if "monospace" in v.lower():
            stats["keep"] += 1
            return head + v
        if v == SYS:
            return head + v
        stats["sys"] += 1
        return head + SYS

    return RX.sub(sub, text), stats


def main():
    dry = "--dry" in sys.argv
    total_sys = total_keep = 0
    print("统一字体栈 -> %s\n" % SYS)
    for rel in TARGETS:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            print("  MISS %s" % rel)
            continue
        s = open(p, encoding="utf-8").read()
        new, st = convert(s)
        total_sys += st["sys"]
        total_keep += st["keep"]
        flag = "dry" if dry or new == s else "write"
        if new != s and not dry:
            open(p, "w", encoding="utf-8").write(new)
        print("  [%s] %-42s 改为系统栈 %-3d  保留等宽 %d"
              % (flag, rel, st["sys"], st["keep"]))
    print("\n合计：改为系统栈 %d 处，保留等宽 %d 处" % (total_sys, total_keep))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
