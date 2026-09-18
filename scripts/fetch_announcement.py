#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
公告抓取器 —— 输入一个招考/招聘公告页面 URL，输出一份可直接开工的材料包。

产出（默认写到 ./公告素材/ 下）：
  1) 公告原文.html        原始页面存档
  2) 公告正文.txt         去标签后的正文纯文本（保留段落换行）
  3) attachments/         页面内所有附件（xlsx/xls/doc/docx/pdf/zip/rar）逐个下载
  4) 图片清单.txt         页面内图片 URL 列表（政府公告常用图片版职位表）
  5) 清单.json            机器可读汇总（供后续脚本/主代理消费）

用法：
  python fetch_announcement.py "<公告URL>" [--out 输出目录] [--download-images]

示例：
  python fetch_announcement.py "https://www.jinwan.gov.cn/zhjwrsj/gkmlpt/content/3/3940/post_3940103.html" --out "D:/公告分析/金湾卫健"

零第三方依赖，仅用标准库。
"""

import argparse
import html as html_mod
import json
import os
import re
import sys
import urllib.parse
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

ATT_EXT = (".xlsx", ".xls", ".xlsm", ".doc", ".docx", ".pdf", ".zip", ".rar", ".7z")
IMG_EXT = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")


# ---------------------------------------------------------------- 网络

def fetch(url, referer=None, timeout=60):
    """返回 (bytes, content_type)。"""
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "identity",
    })
    if referer:
        req.add_header("Referer", referer)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), (r.headers.get("Content-Type") or "")


def decode_bytes(raw, ctype=""):
    """按 Content-Type → <meta charset> → 常见中文编码的顺序尝试解码。"""
    cands = []
    m = re.search(r"charset=[\"']?([\w\-]+)", ctype or "", re.I)
    if m:
        cands.append(m.group(1))
    head = raw[:6000].decode("ascii", errors="ignore")
    m2 = re.search(r"<meta[^>]+charset=[\"']?([\w\-]+)", head, re.I)
    if m2:
        cands.append(m2.group(1))
    cands += ["utf-8", "gb18030", "gbk", "big5"]
    for c in cands:
        try:
            return raw.decode(c), c
        except Exception:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8(replace)"


# ---------------------------------------------------------------- 解析

def _match_block(page, start):
    """从 start 处的 <div ...> 开始，返回与其配对的整块 HTML。"""
    tag_end = page.find(">", start)
    if tag_end < 0:
        return None
    depth = 1
    pos = tag_end + 1
    for m in re.finditer(r"<(/?)div\b[^>]*>", page[pos:], re.I):
        if m.group(1):
            depth -= 1
            if depth == 0:
                return page[start:pos + m.end()]
        else:
            depth += 1
    return None


# 政务网站常见的正文容器（TRS 建站系统与主流 CMS 都覆盖）
_CONTENT_SELECTORS = [
    r'<div[^>]*class="[^"]*TRS_Editor[^"]*"[^>]*>',
    r'<div[^>]*id="zoom"[^>]*>',
    r'<div[^>]*id="(?:content|article|detail|artibody|zhuti)[^"]*"[^>]*>',
    r'<div[^>]*class="[^"]*(?:article[-_]?(?:content|body|con)?|content[-_]?(?:body|txt|con)?|'
    r'detail[-_]?content|news[-_]?content|view[-_]?content|zwxx|gonggao)[^"]*"[^>]*>',
]

# 导航/工具栏短行：完全匹配才丢弃，避免误伤正文
_UI_NOISE = {
    "无障碍", "长者助手", "我的收藏", "收藏", "打印", "分享", "关闭", "返回顶部",
    "首页", "高级搜索", "搜索", "搜索位置", "标题", "全文", "排序方式", "按时间",
    "按相关度", "文件状态", "不限", "现行有效", "已失效", "收起", "字号",
    "下载文字版", "下载图片版", "扫一扫", "分享到", "微信", "微博", "责任编辑",
    "网站地图", "联系我们", "主办单位", "承办单位", "技术支持", "上一页", "下一页",
    "索引号", "分类", "发布机构", "发文日期", "名称", "文号", "主题分类",
}


# 明显不是正文的容器标识（页头、导航、侧栏、分享条等）
_NEGATIVE_TAGS = re.compile(
    r"(header|footer|nav|menu|sidebar|breadcrumb|copyright|"
    r"share|comment|advert|banner|search|login|list|item)", re.I)


def _text_len(html_frag):
    return len(re.sub(r"\s", "", re.sub(r"<[^>]+>", "", html_frag)))


def extract_main_content(page):
    """定位正文容器；找不到则返回整页。

    政务网站常把正文层层包在 content-container > content-wrapper > content-box >
    article-content 里，外层还混着索引信息、面包屑、分享条。单看文字量外层反而更大，
    所以策略是：**取不包含其他候选的最内层块**（正文总在最深处），
    再加一道长度保护——若最内层明显短于最大块，说明切进了正文内部的子容器，回退取最长块。
    """
    items = []
    for pat in _CONTENT_SELECTORS:
        for m in re.finditer(pat, page, re.I):
            if _NEGATIVE_TAGS.search(m.group(0)):
                continue
            blk = _match_block(page, m.start())
            if not blk:
                continue
            n = _text_len(blk)
            if n >= 300:
                items.append((m.start(), m.start() + len(blk), n, blk))

    if not items:
        return page

    # 去重（不同模式可能命中同一容器）
    uniq = {}
    for s, e, n, blk in items:
        uniq[(s, e)] = (s, e, n, blk)
    items = list(uniq.values())

    # 只留「不包含其他候选」的最内层块
    innermost = []
    for i, (s, e, n, _) in enumerate(items):
        contains_other = False
        for j, (s2, e2, _, _) in enumerate(items):
            if i != j and s <= s2 and e2 <= e and (s2, e2) != (s, e):
                contains_other = True
                break
        if not contains_other:
            innermost.append(items[i])

    pool = innermost or items
    cand = max(pool, key=lambda x: x[2])
    if cand[2] < max(x[2] for x in items) * 0.5:
        cand = max(items, key=lambda x: x[2])
    return cand[3]


def html_to_text(page, drop_ui=True):
    """HTML → 保留段落结构的纯文本。优先只取正文容器。"""
    page = extract_main_content(page)
    h = re.sub(r"(?is)<(script|style|noscript|iframe)[^>]*>.*?</\1>", " ", page)
    h = re.sub(r"(?is)<!--.*?-->", " ", h)
    h = re.sub(r"(?i)<br\s*/?>", "\n", h)
    h = re.sub(r"(?i)</t[dh]>", " | ", h)
    h = re.sub(r"(?is)</(p|div|tr|li|h[1-6]|section|table|article)>", "\n", h)
    h = re.sub(r"(?s)<[^>]+>", "", h)
    h = html_mod.unescape(h)
    h = h.replace("\u3000", " ").replace("\xa0", " ")
    h = re.sub(r"[ \t]+", " ", h)
    lines = [ln.strip() for ln in h.split("\n")]
    out, blank = [], 0
    for ln in lines:
        if not ln or ln in ("|", "| |"):
            blank += 1
            if blank > 1:
                continue
            continue
        if drop_ui and ln in _UI_NOISE:
            continue
        blank = 0
        out.append(ln)
    return "\n".join(out)


def find_links(page, page_url):
    """返回 (附件URL列表, 图片URL列表)，均去重保序。"""
    atts, imgs = [], []
    for m in re.finditer(r"(?i)(href|src|data-src)\s*=\s*[\"']([^\"']+)[\"']", page):
        href = m.group(2).strip()
        if not href or href.startswith(("javascript:", "#", "mailto:", "data:")):
            continue
        low = href.lower().split("?")[0].split("#")[0]
        full = urllib.parse.urljoin(page_url, href)
        if low.endswith(ATT_EXT):
            atts.append(full)
        elif low.endswith(IMG_EXT):
            imgs.append(full)
    return _dedup(atts), _dedup(imgs)


def _dedup(seq):
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def pick_attachments(atts):
    """优先保留明显是公告附件的链接：路径含 attachment/upload/files，或文件名与页面同号。"""
    if not atts:
        return []
    keyed = [u for u in atts if re.search(r"(?i)(attachment|upload|files?|resource|/0/\d+/)", u)]
    return keyed if keyed else atts


# ---------------------------------------------------------------- 落盘

def safe_name(url):
    name = os.path.basename(urllib.parse.urlparse(url).path) or "download"
    name = urllib.parse.unquote(name)
    name = re.sub(r"[\\/:*?\"<>|]+", "_", name)
    return name.strip() or "download"


def download(url, dest_dir, referer=None):
    os.makedirs(dest_dir, exist_ok=True)
    path = os.path.join(dest_dir, safe_name(url))
    base, ext = os.path.splitext(path)
    i = 1
    while os.path.exists(path):
        path = "%s_%d%s" % (base, i, ext)
        i += 1
    raw, ctype = fetch(url, referer=referer)
    with open(path, "wb") as f:
        f.write(raw)
    return path, len(raw), ctype


def main():
    ap = argparse.ArgumentParser(description="抓取招考公告页面与附件")
    ap.add_argument("url", help="公告页面 URL")
    ap.add_argument("--out", default="公告素材", help="输出目录（默认 ./公告素材）")
    ap.add_argument("--download-images", action="store_true",
                    help="同时下载页面图片（图片版职位表时使用）")
    args = ap.parse_args()

    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)

    print("[1/4] 抓取页面: %s" % args.url)
    raw, ctype = fetch(args.url)
    page, enc = decode_bytes(raw, ctype)

    html_path = os.path.join(out_dir, "公告原文.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(page)

    text = html_to_text(page)
    text_path = os.path.join(out_dir, "公告正文.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)

    print("[2/4] 页面保存完成 | 编码=%s | 正文 %d 字" % (enc, len(re.sub(r"\s", "", text))))

    atts, imgs = find_links(page, args.url)
    atts = pick_attachments(atts)

    downloaded = []
    if atts:
        print("[3/4] 发现附件 %d 个，开始下载…" % len(atts))
        dest = os.path.join(out_dir, "attachments")
        for u in atts:
            try:
                p, size, ct = download(u, dest, referer=args.url)
                downloaded.append({"url": u, "path": p, "bytes": size, "content_type": ct})
                print("      OK  %s (%d bytes)" % (os.path.basename(p), size))
            except Exception as e:
                downloaded.append({"url": u, "path": None, "error": str(e)})
                print("      FAIL %s -> %s" % (u, e))
    else:
        print("[3/4] 未在页面中找到附件链接（可能由 JS 动态加载，见下）")

    img_path = os.path.join(out_dir, "图片清单.txt")
    if imgs:
        with open(img_path, "w", encoding="utf-8") as f:
            f.write("\n".join(imgs))
        if args.download_images:
            ddir = os.path.join(out_dir, "images")
            for u in imgs:
                try:
                    download(u, ddir, referer=args.url)
                except Exception:
                    pass
            print("[4/4] 已下载 %d 张图片到 images/" % len(imgs))
        else:
            print("[4/4] 页面图片 %d 张，已写入 图片清单.txt（加 --download-images 可下载）" % len(imgs))
    else:
        print("[4/4] 未发现页面图片")

    manifest = {
        "source_url": args.url,
        "out_dir": out_dir,
        "encoding": enc,
        "html": html_path,
        "text": text_path,
        "text_chars": len(re.sub(r"\s", "", text)),
        "attachments": downloaded,
        "images": imgs,
    }
    mpath = os.path.join(out_dir, "清单.json")
    with open(mpath, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print("\n===== 抓取完成 =====")
    print("输出目录 : %s" % out_dir)
    print("公告正文 : %s" % text_path)
    print("附件     : %d 个" % len([d for d in downloaded if d.get("path")]))
    for d in downloaded:
        if d.get("path"):
            print("   - %s" % os.path.basename(d["path"]))

    if manifest["text_chars"] < 200:
        print("\n!! 警告：正文不足 200 字，页面可能是 JS 动态渲染。")
        print("   处理方式：改用 WebFetch 工具直接请求该 URL 提取正文，附件链接从 WebFetch 结果中取。")
    if not atts and not imgs:
        print("\n!! 提示：未发现附件。公告可能把职位表内嵌在正文中，请人工核对 公告正文.txt。")


if __name__ == "__main__":
    main()
