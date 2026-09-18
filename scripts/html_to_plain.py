#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HTML → 纯文本提取器 —— 把公众号排版 HTML 还原成纯文字，用于「去 AI 味」检测与人工复读。

为什么需要它：排版 HTML 里塞满了 inline style、`<span leaf="">` 空标签和组件图标，
直接丢给文本检测脚本会被样式噪声和组件 emoji 干扰（emoji 会被误判为"标题 emoji 滥用"）。

用法：
  python html_to_plain.py <html文件> [--out 输出txt]
  python html_to_plain.py 排版.html --out html_plain.txt

零第三方依赖。
"""

import argparse
import html as html_mod
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def html_to_plain(page, drop_emoji=False):
    h = re.sub(r"(?is)<(script|style|noscript|head)[^>]*>.*?</\1>", " ", page)
    h = re.sub(r"(?is)<!--.*?-->", " ", h)
    h = re.sub(r"(?i)<br\s*/?>", "\n", h)
    # 表格：单元格用空格分隔，行末换行
    h = re.sub(r"(?i)</t[dh]>", " ", h)
    h = re.sub(r"(?i)</tr>", "\n", h)
    h = re.sub(r"(?is)</(p|div|section|li|h[1-6]|blockquote|article)>", "\n", h)
    h = re.sub(r"(?s)<[^>]+>", "", h)
    h = html_mod.unescape(h)
    h = h.replace("\u3000", " ").replace("\xa0", " ").replace("\u200b", "")
    if drop_emoji:
        h = re.sub(r"[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u2B00-\u2BFF]", "", h)
    h = re.sub(r"[ \t]+", " ", h)
    lines = [ln.strip() for ln in h.split("\n")]
    out = []
    for ln in lines:
        if ln:
            out.append(ln)
        elif out and out[-1] != "":
            out.append("")
    return "\n".join(out).strip() + "\n"


def main():
    ap = argparse.ArgumentParser(description="从排版 HTML 中抽取纯文本")
    ap.add_argument("html", help="HTML 文件路径")
    ap.add_argument("--out", default=None, help="输出 txt 路径（默认与 HTML 同目录同名 _plain.txt）")
    ap.add_argument("--drop-emoji", action="store_true",
                    help="顺带剔除 emoji（排版组件图标，供纯文本检测时使用）")
    args = ap.parse_args()

    path = os.path.abspath(args.html)
    if not os.path.exists(path):
        print("文件不存在：%s" % path)
        return
    page = open(path, encoding="utf-8", errors="replace").read()
    text = html_to_plain(page, drop_emoji=args.drop_emoji)

    out_path = args.out or (os.path.splitext(path)[0] + "_plain.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    cn = len(re.findall(r"[\u4e00-\u9fff]", text))
    print("输出: %s" % out_path)
    print("汉字数: %d | 总字符数: %d" % (cn, len(text)))
    print("\n" + "=" * 56)
    print(text[:2500])
    if len(text) > 2500:
        print("\n...（完整内容见 %s）" % out_path)


if __name__ == "__main__":
    main()
