#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
正文字数统计器 —— 按公众号口径统计草稿字数，并给出分章节字数。

口径说明：
  - 只统计中文汉字 + 英文单词，不把 Markdown 标记、空白、标点计入
  - 默认排除表格内容（表格承载的是查阅型信息，不计入"正文可读字数"）
  - 用 --include-tables 可把表格一并计入

用法：
  python count_words.py <md文件>
  python count_words.py 草稿.md --include-tables
  python count_words.py 草稿.md --min 800 --max 1500

零第三方依赖。
"""

import argparse
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CJK = re.compile(r"[\u4e00-\u9fff]")
EN_WORD = re.compile(r"[A-Za-z]{2,}")


def strip_markup(line):
    s = line
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)       # 图片
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)   # 链接留文字
    s = re.sub(r"`{1,3}", "", s)                     # 行内/围栏代码标记
    s = re.sub(r"^\s{0,3}#{1,6}\s*", "", s)          # 标题
    s = re.sub(r"^\s{0,3}>\s?", "", s)               # 引用
    s = re.sub(r"^\s{0,3}[-*+]\s+", "", s)           # 列表
    s = re.sub(r"^\s{0,3}\d+[.、)]\s+", "", s)        # 有序列表
    s = re.sub(r"[*_~]{1,3}", "", s)                 # 加粗/斜体/删除线
    return s


def count(text):
    cn = len(CJK.findall(text))
    en = len(EN_WORD.findall(text))
    return cn, en


def main():
    ap = argparse.ArgumentParser(description="统计公众号推文字数")
    ap.add_argument("md", help="Markdown 草稿路径")
    ap.add_argument("--include-tables", action="store_true", help="把表格内容也计入")
    ap.add_argument("--min", type=int, default=800, help="目标字数下限（默认 800）")
    ap.add_argument("--max", type=int, default=1500, help="目标字数上限（默认 1500）")
    args = ap.parse_args()

    path = os.path.abspath(args.md)
    if not os.path.exists(path):
        print("文件不存在：%s" % path)
        return
    raw = open(path, encoding="utf-8", errors="replace").read()

    body_lines, table_lines = [], []
    for ln in raw.split("\n"):
        if ln.strip().startswith("|"):
            table_lines.append(ln)
        else:
            body_lines.append(ln)

    body_txt = strip_markup("\n".join(body_lines))
    table_txt = strip_markup("\n".join(table_lines))
    body_cn, body_en = count(body_txt)
    tab_cn, tab_en = count(table_txt)

    total_cn = body_cn + tab_cn
    total_en = body_en + tab_en

    print("=" * 52)
    print("文件: %s" % os.path.basename(path))
    print("=" * 52)
    print("正文汉字数（不含表格）: %d  (+英文词 %d)" % (body_cn, body_en))
    print("表格汉字数            : %d" % tab_cn)
    print("全文合计              : %d  (+英文词 %d)" % (total_cn, total_en))
    if args.include_tables:
        print("按 --include-tables 口径计数: %d" % total_cn)

    judged = total_cn if args.include_tables else body_cn
    print("-" * 52)
    if judged < args.min:
        print("判定: 偏短（%d < %d），建议补充内容" % (judged, args.min))
    elif judged > args.max:
        print("判定: 偏长（%d > %d），建议压缩" % (judged, args.max))
    else:
        print("判定: 达标（%d 落在 %d-%d 区间内）" % (judged, args.min, args.max))

    # 分章节统计：level-1 显示「含子节」的合计，子节缩进列出
    sections = []
    for ln in raw.split("\n"):
        m = re.match(r"^\s{0,3}(#{1,6})\s+(.*)$", ln)
        if m:
            sections.append({"level": len(m.group(1)),
                             "title": strip_markup(m.group(2)).strip(),
                             "lines": []})
        elif sections:
            sections[-1]["lines"].append(ln)

    if sections:
        stats = []
        for s in sections:
            t = strip_markup("\n".join(l for l in s["lines"] if not l.strip().startswith("|")))
            c, _ = count(t)
            stats.append(c)

        # 自动判定层级：出现的最小标题级别为篇名，其下一级为章节
        levels = sorted({s["level"] for s in sections})
        base = levels[0]
        chap = base + 1 if (base + 1) in levels else base

        print("-" * 52)
        print("分节字数（章节含子节合计）:")
        i = 0
        while i < len(sections):
            s = sections[i]
            lv = s["level"]
            if lv < chap:
                print("  [篇名] %s  (%d 字)" % (s["title"][:22], stats[i]))
                i += 1
                continue
            if lv == chap:
                j = i + 1
                subtree = stats[i]
                kids = []
                while j < len(sections) and sections[j]["level"] > chap:
                    subtree += stats[j]
                    kids.append((sections[j], stats[j]))
                    j += 1
                print("  %-24s %4d 字" % (s["title"][:24], subtree))
                for k, kc in kids:
                    if kc > 0:
                        print("      %-20s %4d 字" % (k["title"][:20], kc))
                i = j
                continue
            print("  %-24s %4d 字" % (s["title"][:24], stats[i]))
            i += 1


if __name__ == "__main__":
    main()
