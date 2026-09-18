#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
附件解析器 —— 把公告附件（岗位表、报考指南、专业目录…）转成可直接阅读的文本。

支持格式：
  .xlsx/.xlsm  优先 openpyxl（有则用，含合并单元格还原）；无 openpyxl 时用标准库解析 sharedStrings
  .docx        标准库 zipfile + xml（无需 python-docx），保留段落与表格结构
  .doc         老式二进制 Word，多编码试解 + 中文串抽取
  .txt/.md/.csv 直接读取
  .pdf         不处理，提示改用 Read 工具按页读取

用法：
  python parse_attachment.py <文件或目录> [--out 输出txt路径]
  python parse_attachment.py "D:/公告素材/attachments"
  python parse_attachment.py "D:/公告素材/attachments/岗位表.xlsx" --out "岗位表_dump.txt"

零第三方依赖（openpyxl 存在时自动启用，用于更准确还原表格）。
"""

import argparse
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------- xlsx

def parse_xlsx(path):
    """尽量还原表格：含合并单元格回填 + 行列坐标。"""
    try:
        return _parse_xlsx_openpyxl(path)
    except ImportError:
        pass
    except Exception as e:
        head = "!! openpyxl 解析失败(%s)，回退标准库解析\n" % e
        return head + _parse_xlsx_stdlib(path)
    return _parse_xlsx_stdlib(path)


def _parse_xlsx_openpyxl(path):
    import openpyxl  # noqa: F401
    wb = openpyxl.load_workbook(path, data_only=True, read_only=False)
    out = []
    for ws in wb.worksheets:
        out.append("=== SHEET: %s  (rows=%d, cols=%d) ===" % (ws.title, ws.max_row, ws.max_column))
        # 还原合并单元格：跨行的合并需要回填（岗位表里"招聘单位""招聘人数"常纵向合并），
        # 仅同行的横向合并只保留首格，避免整行被重复文字灌满。
        fill = {}
        for rng in ws.merged_cells.ranges:
            if rng.max_row > rng.min_row:
                for r in range(rng.min_row, rng.max_row + 1):
                    for c in range(rng.min_col, rng.max_col + 1):
                        fill[(r, c)] = ws.cell(rng.min_row, rng.min_col).value
        for r in range(1, ws.max_row + 1):
            vals = []
            for c in range(1, ws.max_column + 1):
                v = ws.cell(r, c).value
                if v is None:
                    v = fill.get((r, c))
                s = "" if v is None else str(v).replace("\r", " ").replace("\n", " / ").strip()
                vals.append(s)
            line = " | ".join(vals).rstrip(" |")
            if line.strip(" |"):
                out.append("R%02d: %s" % (r, line))
        out.append("")
    return "\n".join(out)


def _parse_xlsx_stdlib(path):
    """无 openpyxl 时的兜底：直接读 xl/sharedStrings.xml 与 sheet xml。"""
    import zipfile
    from xml.etree import ElementTree as ET
    NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("%ssi" % NS):
                shared.append("".join(t.text or "" for t in si.iter("%st" % NS)))
        sheets = sorted(n for n in z.namelist()
                        if re.match(r"xl/worksheets/sheet\d+\.xml$", n))
        out = []
        for sn in sheets:
            out.append("=== SHEET: %s ===" % sn)
            root = ET.fromstring(z.read(sn))
            for row in root.iter("%srow" % NS):
                vals = []
                for c in row.findall("%sc" % NS):
                    ref = c.get("r") or ""
                    col = re.sub(r"\d", "", ref)
                    t = c.get("t")
                    v = c.find("%sv" % NS)
                    txt = v.text if v is not None and v.text else ""
                    if t == "s" and txt.isdigit():
                        idx = int(txt)
                        txt = shared[idx] if 0 <= idx < len(shared) else txt
                    elif t == "inlineStr":
                        is_el = c.find("%sis" % NS)
                        txt = "".join(x.text or "" for x in is_el.iter("%st" % NS)) if is_el is not None else ""
                    vals.append("%s:%s" % (col, txt.replace("\n", " / ").strip()) if txt else "")
                line = " | ".join(x for x in vals if x)
                if line:
                    out.append(line)
            out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- docx

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def parse_docx(path):
    """标准库解析 docx：按 body 顺序输出段落与表格。"""
    import zipfile
    from xml.etree import ElementTree as ET
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n == "word/document.xml"]
        if not names:
            return "!! 不是有效的 .docx（缺少 word/document.xml）"
        root = ET.fromstring(z.read("word/document.xml"))
    body = root.find("%sbody" % W)
    if body is None:
        return "!! docx 结构异常"

    out = []

    def para_text(p):
        buf = []
        for node in p.iter():
            tag = node.tag
            if tag == "%st" % W:
                buf.append(node.text or "")
            elif tag == "%stab" % W:
                buf.append(" ")
            elif tag == "%sbr" % W:
                buf.append("\n")
        return "".join(buf).strip()

    def walk(el, depth=0):
        for child in el:
            tag = child.tag
            if tag == "%sp" % W:
                s = para_text(child)
                if s:
                    out.append(s)
            elif tag == "%stbl" % W:
                out.append("[表格]")
                for tr in child.findall("%str" % W):
                    cells = []
                    for tc in tr.findall("%stc" % W):
                        txt = " ".join(para_text(p) for p in tc.iter("%sp" % W)).strip()
                        cells.append(re.sub(r"\s+", " ", txt))
                    line = " | ".join(cells).strip(" |")
                    if line:
                        out.append("  " + line)
                out.append("[/表格]")
            elif tag == "%ssdt" % W:
                walk(child, depth + 1)

    walk(body)
    return "\n".join(out)


# ---------------------------------------------------------------- doc (legacy)

# 常见汉字与中文标点，用于判定解码结果是否为「真中文」而非 UTF-16 误读产生的乱码
_COMMON_CN = set(
    "的一是不了在人有我他这个上们来到时大地为子中你说生国年着就那和要她出也得里后自以会家可"
    "下而过天去能对小多然于心学么之都好看起发当没成只如事把还用第样道想作种开美总从无情己面"
    "最女但现些所同日手又行意动方期它头经长儿回位分爱老因很给名法间知世什两次使身者被高已亲"
    "其进此话常与活正感无应当报名考试岗位学历专业资格条件要求材料时间人员招聘单位笔试面试"
    "成绩合格公告规定情形相关证明社保医保户籍年龄周岁以上以下"
)
_CN_PUNCT = set("，。、；：？！“”‘’（）《》—…％·")


def _decode_candidates(data):
    """按编码逐项解码，返回 [(编码, 片段列表, 质量分)]，按质量分降序。"""
    pat = re.compile(r"[\u4e00-\u9fff][\u4e00-\u9fff0-9A-Za-z（）()、，。；：？！\-—…《》%/.\s]{4,600}")
    noise = re.compile(r"(Microsoft|Word|Times New Roman|Arial|Calibri|Normal\.?dot|MSWordDoc|"
                       r"Root Entry|SummaryInformation|DocumentSummary|SimSun|宋体|仿宋|黑体|"
                       r"默认段落字体|正文文本缩进|普通\(网站\)|皑|崀|鬀|鰀|鸀|騀)")
    results = []
    for enc in ("gb18030", "utf-16-le", "utf-8"):
        try:
            txt = data.decode(enc, errors="ignore")
        except Exception:
            continue
        segs, seen = [], set()
        for m in pat.findall(txt):
            s = re.sub(r"\s+", "", m).strip()
            if len(s) < 6 or s in seen or noise.search(s):
                continue
            # 单片段质量闸：常见汉字+中文标点占比过低视为乱码
            good = sum(1 for ch in s if ch in _COMMON_CN or ch in _CN_PUNCT)
            if good / len(s) < 0.22:
                continue
            seen.add(s)
            segs.append(s)
        if not segs:
            continue
        joined = "".join(segs)
        good = sum(1 for ch in joined if ch in _COMMON_CN or ch in _CN_PUNCT)
        results.append((enc, segs, good / max(1, len(joined)), len(joined)))
    results.sort(key=lambda x: (round(x[2], 2), x[3]), reverse=True)
    return results


def parse_doc(path):
    """老式 .doc：多编码试解，按「真中文占比」择优，避免 UTF-16 误读产生的乱码污染。"""
    data = open(path, "rb").read()
    cands = _decode_candidates(data)
    header = ("!! 老式 .doc 为二进制格式，以下为文本抽取结果，可能有顺序错乱或噪声。\n"
              "   若结果明显不全，请改用 Word/WPS 打开后另存为 .docx 再解析，或用 Read 工具导入。\n")
    if not cands:
        return header + "\n（未抽取到可读中文内容）\n"
    enc, segs, score, _ = cands[0]
    header += "   已按 %s 解码（可读度 %.0f%%）\n\n" % (enc, score * 100)
    return header + "\n".join(segs)


# ---------------------------------------------------------------- 入口

def parse_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xlsm", ".xltx", ".xltm"):
        return parse_xlsx(path)
    if ext == ".xls":
        return ("!! .xls 为老式二进制格式，建议用 WPS/Excel 另存为 .xlsx 后重新解析，"
                "或直接由 Read 工具读取。\n")
    if ext == ".docx":
        return parse_docx(path)
    if ext == ".doc":
        return parse_doc(path)
    if ext in (".txt", ".md", ".csv", ".json"):
        for enc in ("utf-8-sig", "utf-8", "gb18030"):
            try:
                return open(path, encoding=enc).read()
            except Exception:
                continue
        return open(path, encoding="utf-8", errors="replace").read()
    if ext == ".pdf":
        return ("!! PDF 不在此脚本处理范围内。请改用 Read 工具按页读取该 PDF"
                "（Read 支持 PDF，能同时拿到文本与版面视觉信息）。\n")
    return "!! 暂不支持的扩展名：%s\n" % ext


def normalize(text):
    """全角空格/零宽字符清理，压缩连续空行。"""
    text = text.replace("\u3000", " ").replace("\u200b", "")
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main():
    ap = argparse.ArgumentParser(description="把公告附件解析为可读文本")
    ap.add_argument("target", help="附件文件路径，或包含多个附件的目录")
    ap.add_argument("--out", default=None, help="输出 txt 路径；目录模式则作为输出目录")
    args = ap.parse_args()

    target = os.path.abspath(args.target)

    if os.path.isdir(target):
        files = sorted(
            os.path.join(target, f) for f in os.listdir(target)
            if os.path.splitext(f)[1].lower() in
            (".xlsx", ".xlsm", ".xls", ".docx", ".doc", ".txt", ".csv", ".pdf")
        )
        if not files:
            print("目录中没有可解析的附件：%s" % target)
            return
        out_dir = os.path.abspath(args.out) if args.out else target
        os.makedirs(out_dir, exist_ok=True)
        for fp in files:
            txt = normalize(parse_file(fp))
            base = os.path.splitext(os.path.basename(fp))[0]
            out_path = os.path.join(out_dir, base + "_dump.txt")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(txt)
            print("=" * 60)
            print("文件: %s" % os.path.basename(fp))
            print("输出: %s  (%d 字符)" % (out_path, len(txt)))
            print("-" * 60)
            print(txt[:3000])
            if len(txt) > 3000:
                print("...（完整内容见 %s）" % out_path)
            print()
    else:
        if not os.path.exists(target):
            print("文件不存在：%s" % target)
            return
        txt = normalize(parse_file(target))
        if args.out:
            out_path = os.path.abspath(args.out)
            os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(txt)
            print("输出: %s  (%d 字符)" % (out_path, len(txt)))
        print(txt)


if __name__ == "__main__":
    main()
