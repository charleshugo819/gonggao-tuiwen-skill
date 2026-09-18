#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""产物页「陈旧排版值」扫描（字号 / 行高 / 字间距）。

分工：
  _scan_typo.py   扫 references/*.md —— 组件库本体
  _stale_scan.py  扫 **.html 产物页** —— docs/gallery 样例页、assets/theme-previews 区块库

豁免：等宽上下文（代码块）的 line-height:1.6 是全局例外，不算陈旧。

用法：python _stale_scan.py
"""
import os
import re
import sys
import collections

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "_bak_typo", "archive", "node_modules"}

LEG_LH = {"1.5", "1.6", "1.7", "1.75", "1.8", "1.85", "1.9", "1.95"}
LEG_LS = {"0.2px", "0.3px", "0.5px", "0.8px", "1px", "1.2px", "1.5px"}

# 页面外壳（不是文章排版）：画廊首页的 <style> 是浏览器端 CSS，不受公众号排版参数约束
SHELL_FILES = {"docs/gallery/index.html"}

RE_FS = re.compile(r"font-size:\s*(\d+)px")
RE_LH = re.compile(r"line-height:\s*([\d.]+)")
RE_LS = re.compile(r"letter-spacing:\s*([\d.]+px)")


def legacy_lh_count(text, window=160):
    """旧行高计数；等宽上下文（代码块）的 line-height:1.6 是全局例外，不计入。"""
    n = 0
    for m in RE_LH.finditer(text):
        v = m.group(1)
        if v not in LEG_LH:
            continue
        if v == "1.6" and "monospace" in text[max(0, m.start() - window):m.start()].lower():
            continue
        n += 1
    return n


def main():
    print("%-52s %-8s %-8s %s" % ("file", "旧行高", "旧字距", "字号分布"))
    print("-" * 110)
    hits = 0
    skipped = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in sorted(files):
            if not f.endswith(".html"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
            t = open(p, encoding="utf-8", errors="ignore").read()
            ls = collections.Counter(RE_LS.findall(t))
            fs = collections.Counter(RE_FS.findall(t))
            n_lh = legacy_lh_count(t)
            n_ls = sum(v for k, v in ls.items() if k in LEG_LS)
            if not (n_lh or n_ls):
                continue
            if rel in SHELL_FILES:
                skipped.append("%s（旧行高 %d / 旧字距 %d，页面外壳 CSS）" % (rel, n_lh, n_ls))
                continue
            hits += 1
            fsd = dict(sorted(fs.items(), key=lambda x: int(x[0])))
            print("%-52s %-8d %-8d %s" % (rel, n_lh, n_ls, fsd))
    print("-" * 110)
    print("含陈旧值的文件数：%d" % hits)
    for s in skipped:
        print("已忽略（非文章排版）：%s" % s)


if __name__ == "__main__":
    main()
