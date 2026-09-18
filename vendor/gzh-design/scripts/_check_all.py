#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一次性跑完全部验收：组件库 → 产物页 → 微信合规。"""
import os
import re
import sys
import subprocess

sys.stdout.reconfigure(encoding="utf-8")
PY = sys.executable
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "scripts")


def run(script, *args):
    r = subprocess.run([PY, os.path.join(S, script)] + list(args),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout


print("#" * 78)
print("# 1) 组件库排版体检 _scan_typo.py")
out = run("_scan_typo.py")
for l in out.split("\n"):
    if any(k in l for k in ("系统栈声明", "非系统字体", "✅", "⚠️")):
        print("   " + l.strip()[:140])

print()
print("#" * 78)
print("# 2) 组件库反模式 component_lint.py")
for l in run("component_lint.py", ROOT).split("\n"):
    if "汇总" in l:
        print("   " + l.strip())

print()
print("#" * 78)
print("# 3) 产物页旧值体检 _stale_scan.py")
for l in run("_stale_scan.py").split("\n"):
    if l.strip() and ("含陈旧值" in l or "已忽略" in l or l.startswith("file") or "---" in l):
        print("   " + l.strip()[:150])

print()
print("#" * 78)
print("# 4) 产物页逐项验收 _verify_previews.py")
out = run("_verify_previews.py")
for l in out.split("\n"):
    if "FAIL" in l or l.strip().startswith("✗") or l.strip().startswith("!"):
        print("   " + l.strip()[:150])

print()
print("#" * 78)
print("# 5) 产物页微信合规 validate_gzh_html.py")
V = os.path.join(S, "validate_gzh_html.py")
F = ["docs/gallery/red-white.html", "docs/gallery/moyu-green.html",
     "docs/gallery/moyu-ticket.html", "docs/gallery/olive-journal.html",
     "docs/gallery/graphite-minimal.html", "docs/gallery/zen-whitespace.html",
     "assets/theme-previews/theme-mono-blue-editorial.html"]
for f in F:
    p = os.path.join(ROOT, f.replace("/", os.sep))
    r = subprocess.run([PY, V, p], capture_output=True, text=True, encoding="utf-8", errors="replace")
    tag = "完全合规" if "完全合规" in r.stdout else "有 ERROR"
    extra = ""
    if tag != "完全合规":
        m = re.search(r"•\s*([^\n]+)", r.stdout)
        extra = "  ← " + (m.group(1).strip() if m else "")
    print("   %-52s %s%s" % (f, tag, extra))

print()
print("#" * 78)
print("# 6) 幂等复跑 _resync_previews.py（应全部 无变化）")
out = run("_resync_previews.py")
changed = 0
for l in out.split("\n"):
    if "写入完成" in l:
        changed += 1
print("   本次实际写入的文件数：%d（应为 0，证明可反复跑不叠加降级）" % changed)
