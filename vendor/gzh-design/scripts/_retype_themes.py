# -*- coding: utf-8 -*-
"""补漏：把仍沿用旧字号体系的主题文件统一到 14px / 2.5 / 2px。

与 _retype_themes.py 的区别：
  1. 正则容忍 `font-size: 19px`（冒号后带空格）的写法
  2. 覆盖说明文字里的旧值，不只是 style 属性内
  3. **幂等守卫**：文件已达标则跳过，不会二次降级

幂等判据：line-height 为 2.5 的占比 >= 50% 视为已处理。
"""
import os
import re
import sys
import collections

sys.stdout.reconfigure(encoding="utf-8")

REF = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "references")

# 各主题原正文字号基准
BASE = {
    "theme-red-white.md": 15,
    "theme-moyu-green.md": 14,
    "theme-moyu-ticket.md": 14,
    "theme-olive-journal.md": 14,
    "theme-graphite-minimal.md": 15,
    "theme-zen-whitespace.md": 15,
    "common-components.md": 15,
}
NEW_BODY = 14
FLOOR = 12          # 12px 以下不再等比缩小
MIN_TINY = 11       # 10px 及以下抬到 11px

# 行高：正文类 → 2.5；结构性/装饰性保持
LH_TEXT = {"1.8", "1.9", "1.85", "1.75", "1.7", "1.6", "1.5", "1.95"}
LH_KEEP_CTX = ("mono", "consolas")          # 代码块行距保持紧凑
# 字间距：中文文本 → 2px；3px/4px 是英文标签与装饰的刻意疏排
LS_TEXT = {"0.2px", "0.3px", "0.5px", "0.8px", "1px", "1.2px", "1.5px"}


def map_size(n, base):
    if n >= 20:
        return max(20, int(round(n * NEW_BODY / base)))
    if n >= 13:
        return max(FLOOR, int(round(n * NEW_BODY / base)))
    if n >= FLOOR:
        return n
    return MIN_TINY


def already_done(text):
    """幂等守卫：2.5 行高占比过半即视为已统一。"""
    all_lh = re.findall(r"line-height:\s*([\d.]+)", text)
    if not all_lh:
        return False
    return all_lh.count("2.5") / len(all_lh) >= 0.5


def rewrite(text, base):
    def fs(m):
        return "font-size:%s%dpx" % (m.group(1), map_size(int(m.group(2)), base))

    # font-size:  14px  /  font-size:14px  两种写法都吃到
    text = re.sub(r"font-size:(\s*)(\d+)px", fs, text)

    def lh(m):
        v = m.group(2)
        if v not in LH_TEXT:
            return m.group(0)
        if v == "1.6" and any(k in text[max(0, m.start() - 120):m.start()].lower() for k in LH_KEEP_CTX):
            return m.group(0)
        return "line-height:%s2.5" % m.group(1)

    text = re.sub(r"line-height:(\s*)([\d.]+)", lh, text)

    def ls(m):
        return "letter-spacing:%s2px" % m.group(1) if m.group(2) in LS_TEXT else m.group(0)

    text = re.sub(r"letter-spacing:(\s*)([\d.]+px)", ls, text)
    return text


def main():
    only = sys.argv[1:] or list(BASE)
    for fn in only:
        p = os.path.join(REF, fn)
        src = open(p, encoding="utf-8").read()
        if already_done(src):
            print("跳过（已达标）  %s" % fn)
            continue
        new = rewrite(src, BASE[fn])
        if new == src:
            print("无变化          %s" % fn)
            continue
        open(p, "w", encoding="utf-8").write(new)
        sizes = collections.Counter(re.findall(r"font-size:\s*(\d+)px", new))
        lh = collections.Counter(re.findall(r"line-height:\s*([\d.]+)", new))
        print("已重写          %-26s 基准 %dpx" % (fn, BASE[fn]))
        print("    字号:", dict(sorted(sizes.items(), key=lambda x: int(x[0]))))
        print("    行高:", dict(sorted(lh.items())))


if __name__ == "__main__":
    main()
