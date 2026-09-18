# -*- coding: utf-8 -*-
"""把六套主题的新配色 + 删英文标签，同步到 gallery 预览页与 assets/theme-previews。

这两处不跟 references/ 走，要单独同步（老坑）。
只改 style 值与英文标签文本，不动结构。
"""
import os
import re

ROOT = r"C:\Users\Administrator\.workbuddy\skills\gonggao-tuiwen\vendor\gzh-design"

# 六个主题的色值映射（与 _recolor.py 一致）
COLOR_MAPS = {
    "moyu-green": {
        "#059669": "#0F766E", "#10B981": "#14B8A6", "#34D399": "#2DD4BF",
        "#6EE7B7": "#5EEAD4", "#A7F3D0": "#99F6E4", "#BBF7D0": "#CCFBF1",
        "#D1FAE5": "#F0FDFA", "#ECFDF5": "#F0FDFA",
        "#047857": "#115E59", "#065F46": "#134E4A", "#064E3B": "#134E4A",
    },
    "red-white": {
        "#DC2626": "#B91C1C", "#EF4444": "#DC2626", "#F87171": "#EF4444",
        "#FCA5A5": "#F87171", "#FECACA": "#FCA5A5", "#991B1B": "#8A1414",
    },
    "graphite-minimal": {
        "#52525B": "#475569", "#27272A": "#1E293B", "#3F3F46": "#334155",
        "#71717A": "#64748B", "#A1A1AA": "#94A3B8", "#E4E4E7": "#E2E8F0",
        "#F4F4F5": "#F1F5F9", "#FAFAFA": "#F8FAFC",
    },
    "zen-whitespace": {
        "#4A5D52": "#556B4F", "#3D5046": "#47593F", "#B5C8BC": "#BCC9B2",
        "#D6E4DC": "#DCE5D3", "#EEF3F0": "#F0F4EA",
    },
    "moyu-ticket": {
        "#059669": "#4F46E5", "#10B981": "#6366F1", "#34D399": "#818CF8",
        "#A7F3D0": "#C7D2FE", "#BBF7D0": "#DDD6FE", "#D1FAE5": "#E0E7FF",
        "#ECFDF5": "#EEF2FF", "#F0FDF4": "#EEF2FF",
        "#047857": "#4338CA", "#065F46": "#3730A3",
    },
    "olive-journal": {
        "#ed7b2f": "#A14E1E", "#b17816": "#8A5A12", "#d4c9b8": "#D6C8B4",
    },
}

# 英文徽章（含可能的外壳），整块删
BADGE_RES = [
    re.compile(r'\s*<span style="[^"]*">\s*<span leaf="">\s*('
               r'STEP 01|CASE 01|SKILL 1|VIDEO 01|CMD|PROMPT|CASE|DOODLE|GRADE|'
               r"VALID FOR ONE READ|ADMIT ONE [^<]*|THANKS FOR READING[^<]*|"
               r"PART 01|PART 02|PART ///|PART|NOTE|QUOTE|REFERENCE"
               r')\s*</span>\s*</span>', re.S),
    re.compile(r'\s*<p style="[^"]*letter-spacing:[^"]*"[^>]*>\s*<span leaf="">\s*('
               r"PART 01|PART 02|PART ///|PART|NOTE|QUOTE|REFERENCE|"
               r"THANKS FOR READING[^<]*|DOODLE|CASE"
               r')\s*</span>\s*</p>', re.S),
    re.compile(r'\s*<section style="font-size:11px;[^"]*letter-spacing:2px;?">\s*<span leaf="">\s*('
               r'GRADE|VALID FOR ONE READ|ADMIT ONE [^<]*'
               r')\s*</span>\s*</section>', re.S),
]


def process(path, theme, do_strip=True):
    s = open(path, encoding="utf-8").read()
    src = s
    ncolors = 0
    for old, new in COLOR_MAPS[theme].items():
        if old == new:
            continue
        for v, nv in ((old, new), (old.upper(), new.upper()), (old.lower(), new.lower())):
            c = s.count(v)
            if c:
                s = s.replace(v, nv)
                ncolors += c
    nb = 0
    if do_strip:
        for rx in BADGE_RES:
            s, k = rx.subn("", s)
            nb += k
    if s != src:
        open(path, "w", encoding="utf-8", newline="\n").write(s)
    return len(src), len(s), ncolors, nb


def main():
    jobs = []
    gal = os.path.join(ROOT, "docs", "gallery")
    for t in COLOR_MAPS:
        p = os.path.join(gal, t + ".html")
        if os.path.exists(p):
            jobs.append((p, t, True))
    prev = os.path.join(ROOT, "assets", "theme-previews")
    for t in COLOR_MAPS:
        p = os.path.join(prev, "theme-" + t + ".html")
        if os.path.exists(p):
            jobs.append((p, t, True))
    for p, t, st in jobs:
        a, b, nc, nb = process(p, t, st)
        print("%-58s %6d -> %6d  色%-4d 删标签%d" % (os.path.relpath(p, ROOT), a, b, nc, nb))


if __name__ == "__main__":
    main()
