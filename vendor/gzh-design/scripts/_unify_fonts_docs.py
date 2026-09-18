#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体统一 — 文档/描述层同步（与 _unify_fonts.py 配套）。

_unify_fonts.py 负责把 `font-family:` 的值改成系统栈；
本脚本负责把散落在说明文字里的旧字体描述（衬线 / IBM Plex Sans / 字体偏好列表）
一并改掉，否则下次生成新主题时又会把非系统字体引回来。

用法：python _unify_fonts_docs.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SYS = ("-apple-system,BlinkMacSystemFont,'PingFang SC',"
       "'Hiragino Sans GB','Microsoft YaHei',sans-serif")

# ---- theme-zen-whitespace.md：先精确替换，再兜底清「衬线」 ----
ZEN = [
    # 速查表字体行
    ("标题字体：          'Noto Serif SC', Georgia, 'Times New Roman', serif（衬线）",
     "标题字体：          系统默认无衬线栈（与正文一致）"),
    ("正文字体：          -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif",
     "正文字体：          -apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif"),
    # 具体描述句
    ("衬线字体大字金句居中", "大字金句居中"),
    ("衬线字体自带书卷气", "大字号自带书卷气"),
    ("衬线字体居中，大留白", "大字居中，大留白"),
    ("「这里是核心金句，衬线字体 + 大留白 + 细线框定。」",
     "「这里是核心金句，大字 + 大留白 + 细线框定。」"),
    ("数字用衬线字体提气质", "数字用大字号提气质"),
    ("衬线大标题", "大标题"),
    # 兜底组合
    ("衬线大号数字", "大号数字"),
    ("居中衬线", "居中"),
    ("衬线大字", "大字"),
    ("衬线中文", "中文"),
    ("衬线", ""),
]

OLIVE = [
    ("字体栈：`'IBM Plex Sans',-apple-system,system-ui,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif`",
     "字体栈：`%s`（系统默认无衬线，与全主题统一）" % SYS),
]

GEN = [
    ("| 字体偏好 | 提示词允许列表内的值 | 按风格自动选 |",
     "| 字体偏好 | 固定 `system` | 全库统一，无其它可选 |"),
    ("""【字体偏好约束】
字体偏好只能从以下值中选择一个写入 `THEME-FONT-PREFERENCE`：

- `system`
- `pingfang`
- `microsoft-yahei`
- `source-hans-sans`
- `source-hans-serif`
- `alibaba-puhuiti`
- `youshe-titlehei`
- `serif`
- `monospace`
- `kaiti`
- `fangsong`
- `stzhongsong`
- `stfangsong`
- `stkaiti`
- `yuanti`

如果用户没有明确指定字体，或输入字体不在允许列表中，你必须根据主题风格从上面的列表中选择最合适的一项，不能输出列表之外的字体值。""",
     """【字体偏好约束】
字体偏好**固定为 `system`**，没有其它可选值：

- `system`

全库统一：所有主题的正文 / 标题 / 引用 / 提示 / 列表 / 表格一律使用系统默认无衬线栈
`-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif`。

唯一例外是**代码块与行内代码**，用 `'SF Mono',Consolas,Monaco,monospace`——这是功能性等宽字体，
用于保证代码对齐与视觉区分，不属于装饰性字体。

即使用户在提示词里点名「衬线字体」「楷体」「思源宋体」等，也不要照做：微信公众号编辑器不支持加载
外部字体，用户设备也未必安装，只会造成各端观感不一致；此时按系统栈生成，并向用户说明原因。"""),
    ("- 字体偏好必须体现在 font-family 倾向上，但元信息中的字体值必须严格使用允许列表值",
     "- 字体偏好固定为 `system`：所有组件 `font-family` 一律写系统默认无衬线栈（代码块用等宽），元信息中的字体值只能是 `system`，不得输出其它值"),
]

SKILL = [
    ("| 字体栈 | `-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif` | 系统默认无衬线，**不引外部字体** |",
     "| 字体栈 | `-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif` | **6 套主题全部统一**，不引外部字体、不用衬线/楷体等装饰字体 |"),
    ("**字体**：正文一律系统默认无衬线栈；例外是留白禅意（标题用 `'Noto Serif SC', Georgia, 'Times New Roman', serif` 衬线）与橄榄手记（正文优先 `'IBM Plex Sans'`，缺字体时回落系统栈），代码块用 `'SF Mono', Consolas, Monaco, monospace`。",
     "**字体**：全库统一系统默认无衬线栈，**没有主题例外**——原先留白禅意的 `'Noto Serif SC'` 标题衬线与橄榄手记的 `'IBM Plex Sans'` 正文均已改为系统栈。唯一保留的是代码块与行内代码的 `'SF Mono', Consolas, Monaco, monospace`（功能性等宽，保证对齐）。原因：公众号编辑器不支持加载外部字体，用户设备未必安装，写非系统字体只会导致各端观感不一致。"),
]

README = [
    ("| 禅意 / 极简随笔 | 留白禅意；大留白 + 居中衬线引用 |",
     "| 禅意 / 极简随笔 | 留白禅意；大留白 + 居中大字引用 |"),
    ("> 按「黑白杂志、克莱因蓝点睛、衬线字体」的气质，给公众号排版生成一套新主题",
     "> 按「黑白杂志、克莱因蓝点睛」的气质，给公众号排版生成一套新主题"),
]

JOBS = [
    (r"references\theme-zen-whitespace.md", ZEN),
    (r"references\theme-olive-journal.md", OLIVE),
    (r"references\theme-generator.md", GEN),
    ("SKILL.md", SKILL),
    ("README.md", README),
]


def main():
    for rel, rules in JOBS:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            print("  MISS %s" % rel)
            continue
        s = open(p, encoding="utf-8").read()
        hit = 0
        for a, b in rules:
            if a in s:
                s = s.replace(a, b)
                hit += 1
            else:
                print("     ~ 未命中(可能已改): %s" % a.split("\n")[0][:60])
        open(p, "w", encoding="utf-8").write(s)
        print("  [write] %-42s 命中 %d/%d" % (rel, hit, len(rules)))
    print("\n完成。")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
