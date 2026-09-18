#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重排组件库之外的产物页，使其与当前全局排版参数同步。

覆盖两类文件（它们不在 references/ 里，_retype_themes.py 扫不到）：
  1. docs/gallery/*.html —— 「同一篇文章 × 6 套主题」的样例页
  2. assets/theme-previews/*.html —— 主题生成器产出的区块库预览

做法（不新造映射表，直接复用 _retype_themes 的同一套全局参数）：
  Pass A  字号 / 行高 / 字间距 —— 调 rt.rewrite()，与组件库同一函数、同一映射
  Pass B  段间距 —— 章级正文段落统一 2.5em；卡片内段落（margin:0）不动

段间距的三种结构（gap 模式）：
  flat   段落自带 margin-bottom:NNpx（红白/摸鱼绿/摸鱼票据/石墨/禅意）→ 改该值
  olive  段落自身 margin:0，间距来自外层包裹盒 <section style="margin-top:24px;"> → 改包裹盒
  none   区块库：每个 Block 的外边距是**组件间距**而非文章段间距，不动（只做 Pass A）

⚠️ 幂等守卫（务必保留）：map_size() 是相对缩放，同一份文本跑第二遍会把
   39→36、17→16 再降一轮。只要文件已达标（行高过半为 2.5）就整段跳过 Pass A。
   Pass B 写绝对值 2.5em，天然幂等。

用法：
  python _resync_previews.py              # 全部
  python _resync_previews.py --check      # 只体检不写入
  python _resync_previews.py red-white.html
"""
import os
import re
import sys
import collections
import importlib.util

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

_spec = importlib.util.spec_from_file_location("_retype_themes", os.path.join(HERE, "_retype_themes.py"))
rt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rt)

# 相对 skill 根的路径 -> (原始正文字号基准, gap 模式)
TARGETS = {
    "docs/gallery/red-white.html": (15, "flat"),
    "docs/gallery/moyu-green.html": (14, "flat"),
    "docs/gallery/moyu-ticket.html": (14, "flat"),
    "docs/gallery/olive-journal.html": (14, "olive"),
    "docs/gallery/graphite-minimal.html": (15, "flat"),
    "docs/gallery/zen-whitespace.html": (15, "flat"),
    "assets/theme-previews/theme-mono-blue-editorial.html": (15, "none"),
}

BODY = 14  # 缩放后的正文号，用于识别正文段落

RE_P = re.compile(r'<p style="([^"]*)"')
RE_GAP_NUM = re.compile(r"margin-bottom:(\s*)\d+px")
RE_OLIVE_WRAP = re.compile(
    r'<section style="margin-top:24px;?">'
    r'(\s*<section style="font-family:[^"]*">\s*<p style="([^"]*)")'
)


def is_body_para(style):
    """章级正文段落判据。

    必须容忍 `text-align: justify` / `font-size: 14px` 这种冒号后带空格的写法
    （留白禅意整套都是这种写法，早先用不带 \\s* 的正则整篇漏改过，这是同一个坑）。
    """
    return (re.search(r"text-align:\s*justify", style) is not None
            and re.search(r"font-size:\s*%dpx" % BODY, style) is not None)


def fix_gap_flat(text):
    """段落自带 margin-bottom 的主题：直接改该值。"""
    n = [0]

    def repl(m):
        st = m.group(1)
        if not is_body_para(st):
            return m.group(0)
        new, k = RE_GAP_NUM.subn(lambda x: "margin-bottom:%s2.5em" % x.group(1), st)
        if k:
            n[0] += 1
        return '<p style="%s"' % new

    return RE_P.sub(repl, text), n[0]


def fix_gap_olive(text):
    """橄榄手记：改包裹盒 margin-top，且只改「紧随其后是正文段落」的那种。"""
    n = [0]

    def repl(m):
        if is_body_para(m.group(2)):
            n[0] += 1
            return '<section style="margin-top:2.5em;">' + m.group(1)
        return m.group(0)

    return RE_OLIVE_WRAP.sub(repl, text), n[0]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check_only = "--check" in sys.argv
    files = args or list(TARGETS)

    for fn in files:
        if fn not in TARGETS:
            # 允许只给文件名
            cand = [k for k in TARGETS if k.endswith("/" + fn)]
            if len(cand) != 1:
                print("!! 未知目标 %s" % fn)
                continue
            fn = cand[0]
        p = os.path.join(ROOT, fn.replace("/", os.sep))
        base, mode = TARGETS[fn]
        src = open(p, encoding="utf-8").read()
        print("=" * 74)
        print("%s   基准 %dpx   gap=%s" % (fn, base, mode))

        lh_all = collections.Counter(re.findall(r"line-height:\s*([\d.]+)", src))
        ls_all = collections.Counter(re.findall(r"letter-spacing:\s*([\d.]+px)", src))
        n_lh = sum(v for k, v in lh_all.items() if k in rt.LH_TEXT)
        n_ls = sum(v for k, v in ls_all.items() if k in rt.LS_TEXT)

        if rt.already_done(src):
            new, n_lh, n_ls = src, 0, 0
            print("   Pass A 跳过（已达标，防叠加降级）")
        else:
            new = rt.rewrite(src, base)
            print("   Pass A 行高 →2.5 : %-3d 处" % n_lh)
            print("   Pass A 字距 →2px : %-3d 处" % n_ls)

        if mode == "olive":
            new, n_gap = fix_gap_olive(new)
            label = "包裹盒 margin-top"
        elif mode == "flat":
            new, n_gap = fix_gap_flat(new)
            label = "正文段落 margin-bottom"
        else:
            n_gap = 0
            label = "（区块库，不动组件外边距）"
        print("   Pass B 段间距(%s) : %-3d 处" % (label, n_gap))

        if check_only:
            print("   [--check] 未写入")
            continue
        if new == src:
            print("   无变化（已达标）")
            continue

        open(p, "w", encoding="utf-8").write(new)
        fs = collections.Counter(re.findall(r"font-size:\s*(\d+)px", new))
        lh = collections.Counter(re.findall(r"line-height:\s*([\d.]+)", new))
        ls = collections.Counter(re.findall(r"letter-spacing:\s*([\d.]+px)", new))
        print("   写入完成")
        print("     字号:", dict(sorted(fs.items(), key=lambda x: int(x[0]))))
        print("     行高:", dict(sorted(lh.items())))
        print("     字距:", dict(sorted(ls.items())))
    print("=" * 74)
    print("完成。")


if __name__ == "__main__":
    main()
