#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""产物页（画廊样例页 + 区块库预览）重排后的验收校验。

检查项：
  A 旧值残留（行高 / 字间距）
  B 字体（非系统栈且非等宽）
  C 段间距边界：章级正文段落=2.5em，组件内段落=margin:0 / margin:0 0 Npx，不允许其它值
  D 橄榄手记：章级正文段落的包裹盒 margin-top=2.5em
  E 等宽元素（代码块）行高保持 1.6，未被误改成 2.5
  F 字号层级必须落在对应主题组件库的层级集合内
  G 文字完整性：与重排前备份逐字比对（只允许 style 数值变化）
"""
import os
import re
import sys
import html
import collections

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAK = os.path.join(ROOT, "references", "_bak_typo", "gallery")
REF = os.path.join(ROOT, "references")

SYS_STACK = ("-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB',"
             "'Microsoft YaHei',sans-serif")
LEG_LH = {"1.5", "1.6", "1.7", "1.75", "1.8", "1.85", "1.9", "1.95"}
LEG_LS = {"0.2px", "0.3px", "0.5px", "0.8px", "1px", "1.2px", "1.5px"}

# (相对路径, 对照组件库或 None, gap 模式)
TARGETS = [
    ("docs/gallery/red-white.html", "theme-red-white.md", "flat"),
    ("docs/gallery/moyu-green.html", "theme-moyu-green.md", "flat"),
    ("docs/gallery/moyu-ticket.html", "theme-moyu-ticket.md", "flat"),
    ("docs/gallery/olive-journal.html", "theme-olive-journal.md", "olive"),
    ("docs/gallery/graphite-minimal.html", "theme-graphite-minimal.md", "flat"),
    ("docs/gallery/zen-whitespace.html", "theme-zen-whitespace.md", "flat"),
    ("assets/theme-previews/theme-mono-blue-editorial.html", None, "block"),
]

RE_LH = re.compile(r"line-height:\s*([\d.]+)")
RE_LS = re.compile(r"letter-spacing:\s*([\d.]+px)")
RE_FS = re.compile(r"font-size:\s*(\d+)px")
RE_FAM = re.compile(r"font-family:\s*([^;\"]+)")
RE_P = re.compile(r'<p style="([^"]*)"')


def strip_tags(s):
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    return re.sub(r"\s+", "", s)


def legacy_lh(text, window=160):
    """旧行高残留；等宽上下文（代码块）的 1.6 是合法例外，不计入。"""
    out = []
    for m in RE_LH.finditer(text):
        v = m.group(1)
        if v not in LEG_LH:
            continue
        if v == "1.6" and "monospace" in text[max(0, m.start() - window):m.start()].lower():
            continue
        out.append(v)
    return sorted(set(out))


def main():
    fails, warn = [], []
    for rel, ref, mode in TARGETS:
        p = os.path.join(ROOT, rel.replace("/", os.sep))
        t = open(p, encoding="utf-8").read()
        print("=" * 78)
        print(rel)

        lh_leg = legacy_lh(t)
        ls_leg = sorted(set(k for k in RE_LS.findall(t) if k in LEG_LS))
        print("  A 旧行高残留 %-16s 旧字距残留 %s（等宽代码块的 1.6 已豁免）"
              % (lh_leg or "无", ls_leg or "无"))
        if lh_leg or ls_leg:
            fails.append("%s: 旧值残留" % rel)

        bad_fam = sorted(set(f.strip() for f in RE_FAM.findall(t)
                             if f.strip() != SYS_STACK and "monospace" not in f.lower()))
        print("  B 非系统字体 %s" % (bad_fam or "无"))
        if bad_fam:
            fails.append("%s: 非系统字体 %s" % (rel, bad_fam))

        if mode in ("flat", "olive"):
            g25 = gz = other = 0
            others = []
            for m in RE_P.finditer(t):
                st = m.group(1)
                if not (re.search(r"text-align:\s*justify", st)
                        and re.search(r"font-size:\s*14px", st)):
                    continue
                if re.search(r"margin-bottom:\s*2\.5em", st):
                    g25 += 1
                elif re.search(r"(?:^|;)margin:\s*0(?:[;\s]|$)", st) or re.search(r"margin-bottom:\s*0(?:;|$)", st):
                    gz += 1
                else:
                    other += 1
                    mb = re.search(r"margin-bottom:\s*([^;]+)", st)
                    mg = re.search(r"(?:^|;)margin:\s*([^;]+)", st)
                    others.append("mb=%s margin=%s" % (mb.group(1) if mb else "-", mg.group(1) if mg else "-"))
            print("  C 正文段落：2.5em %-3d 组件内 %-3d 其它 %-3d" % (g25, gz, other))
            for o in others:
                print("       ! %s" % o)
            if other:
                warn.append("%s: %d 个正文段落段间距例外" % (rel, other))
            if g25 + gz == 0:
                fails.append("%s: 未识别到正文段落" % rel)

        if mode == "olive":
            wraps = collections.Counter(re.findall(r'<section style="margin-top:\s*([^"]+)"', t))
            body_wrap = len(re.findall(
                r'<section style="margin-top:\s*2\.5em;">\s*<section style="font-family:', t))
            print("  D 包裹盒 %s；正文段落包裹盒 %d 个" % (dict(wraps), body_wrap))
            if body_wrap == 0:
                fails.append("olive: 正文段落包裹盒未改为 2.5em")

        mono_lh = collections.Counter()
        for m in re.finditer(r'style="([^"]*monospace[^"]*)"', t):
            l = RE_LH.search(m.group(1))
            mono_lh[l.group(1) if l else "(none)"] += 1
        print("  E 等宽元素行高 %s" % dict(mono_lh))
        if any(v not in ("1.6", "0", "1", "(none)") for v in mono_lh):
            warn.append("%s: 等宽元素异常行高 %s" % (rel, dict(mono_lh)))

        gl = set(int(x) for x in RE_FS.findall(t))
        if ref:
            rl = set(int(x) for x in RE_FS.findall(open(os.path.join(REF, ref), encoding="utf-8").read()))
            print("  F 字号 %s" % sorted(gl))
            print("    组件库 %s%s" % (sorted(rl), "" if gl <= rl else "  ← 多出 %s" % sorted(gl - rl)))
            if not gl <= rl:
                warn.append("%s: 多出组件库没有的字号 %s" % (rel, sorted(gl - rl)))
        else:
            print("  F 字号 %s（区块库，不做层级比对）" % sorted(gl))

        old_p = os.path.join(BAK, os.path.basename(rel))
        if os.path.exists(old_p):
            cur, old = strip_tags(t), strip_tags(open(old_p, encoding="utf-8").read())
            same = cur == old
            print("  G 文字%s（%d 字）" % ("完全一致 ✓" if same else "有差异 ✗", len(cur)))
            if not same:
                fails.append("%s: 文字内容发生变化" % rel)
                for i, (a, b) in enumerate(zip(old, cur)):
                    if a != b:
                        print("        首处差异 @%d：备份「%s」→ 现行「%s」"
                              % (i, old[max(0, i - 25):i + 25], cur[max(0, i - 25):i + 25]))
                        break
                else:
                    print("        长度不同：备份 %d / 现行 %d" % (len(old), len(cur)))
        else:
            print("  G 无备份，跳过文字比对")

    print("=" * 78)
    print("FAIL %d 项 / WARN %d 项" % (len(fails), len(warn)))
    for f in fails:
        print("  ✗ " + f)
    for w in warn:
        print("  ! " + w)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
