# 踩坑记录（实战沉淀）

## 一、环境类

### bash 缺常用命令

本机 bash（Git Bash shim）**没有 `dirname`、`head`、`ls` 等命令**，管道会直接失败。

**对策**：
- 不要用 `cmd | head -20`，改用脚本内部截断输出，或用 Read 工具读文件
- 不要用 `mkdir -p`，脚本内用 `os.makedirs()`
- 搜索文件用 Glob/Grep 工具，不要用 `find`/`grep` 命令

### Python 必须用全路径

环境里可能没有 `python` / `python3` 命令名。统一用托管解释器全路径：

```
C:\Users\<用户名>\.workbuddy\binaries\python\versions\3.13.12\python.exe
```

### openpyxl 可能缺失

`parse_attachment.py` 已内置标准库回退，但精度略降（合并单元格还原不完整）。必要时：

```bash
"<python.exe>" -m pip install openpyxl -q
```

### 老式 .xls 解析不了（脚本只支持 .xlsx）

`parse_attachment.py` 走 openpyxl 通道，**只能读 `.xlsx`**；遇到 `.xls`（BIFF8 二进制）会输出空结果，
且本机可能连 `openpyxl` / `xlrd` / `pandas` 都没装。

**对策（零依赖，已验证可行）**：直接按 BIFF8 记录结构抽字符串。
`.xls` 里中文以 UTF-16LE 存在，扫 BIFF 记录（`struct.unpack_from("<HH", buf, i)` 取 `rec, ln`）
或兜底按 UTF-16LE 扫可读中文串，能还原岗位表全部字段（岗位代码 / 人数 / 岗位描述 / 专业要求 / 学历学位）。

更省事的两个办法：
1. **用 WPS/Excel 另存为 `.xlsx`** 再跑 `parse_attachment.py`（最稳）
2. **WebSearch 搜公告标题**——转载站常把附件表格转成网页文本，可直接核对字段

### python-docx 未安装

**不要依赖它**。本 skill 的 `parse_attachment.py` 用标准库 `zipfile` + `xml.etree` 解析 `.docx`，能保留段落与表格结构。自己写脚本时也照此处理。

---

## 二、工具类

### sheetagent 不能处理 Windows 路径

`mcp__sheetagent__resolve_local_excel` 要求路径以 `/` 开头，Windows 盘符路径（`D:\...`）会报 `INVALID_LOCAL_PATH`，URL 编码后同样失败。

**对策**：Windows 环境一律用 `parse_attachment.py`（openpyxl 通道）。

### 附件下载：用脚本内置 urllib，别用 curl

bash 环境不稳定时 `curl` 可能不可用。`fetch_announcement.py` 内置 urllib，且带 UA / Referer，能过多数政务站点的防盗链。

**若必须手工下载**，PowerShell 的 `Invoke-WebRequest` 比 curl 稳：

```powershell
Invoke-WebRequest -Uri "<附件URL>" -OutFile "<目标路径>"
```

---

## 三、抓取类

### 政务网站附件链接的典型形态

政府公告页附件通常在文末"相关附件"区，链接形如：

```
http://www.jinwan.gov.cn/zhjwrsj/attachment/0/442/442304/3940103.xlsx
```

特征：路径含 `attachment` / `upload` / `/0/<数字>/`。`fetch_announcement.py` 的 `pick_attachments()` 已按此优先筛选。

### 职位表可能是图片

部分公告把职位表做成图片贴在正文里，页面**没有任何附件链接**。此时：

1. `fetch_announcement.py` 会输出 `图片清单.txt`
2. 加 `--download-images` 下载
3. 用 **Read 工具逐张读图**（Read 支持图片，可直接识别表格内容）

### 页面 JS 动态渲染

正文抓下来不足 200 字就是这种情况。脚本会自动告警。

**对策**：改用 **WebFetch 工具**请求该 URL，让工具侧渲染并提取正文；附件链接从 WebFetch 返回的内容里找。

### 编码问题

政务网站编码混乱（UTF-8 / GB18030 / GBK 都有）。`fetch_announcement.py` 的 `decode_bytes()` 按 `Content-Type → <meta charset> → 常见中文编码` 逐级尝试，一般无需干预。老式 `.doc` 附件则需要 `utf-16-le` / `gb18030` 双解码再抽中文串（已在 `parse_attachment.py` 实现）。

### 聚合站（中公/华图等）拿不到附件 → 回政府源站

中公、华图这类转载页**通常不带附件**（正文里只有"点击查看>>>"文字，没有真实链接）。
转载页末尾的「文章来源」一行就是政府源站 URL：

```
文章来源：http://www.xinyi.gov.cn/zwgk/zlxx/content/post_1647367.html
```

用这个 URL 重跑 `fetch_announcement.py`，附件区（`attachment/upload/0/<数字>/`）就能抓到。

**顺带**：政府源站的正文比转载页更干净（无"进入阅读模式""猜你喜欢"噪声），信息也更新，**建议拿到源站 URL 后以源站为准**。

### 多个附件会覆盖 dump

`parse_attachment.py` 的 dump 文件名按附件主名生成。若页面附件**同名不同扩展**（典型：`1647367.xls` 和 `1647367.doc`），两份 dump 会**互相覆盖**，只剩最后一个。

**对策**：分批解析（先移走一个再跑），或先把附件改名（加 `_岗位表` / `_报名表` 后缀）再解析。

---

## 四、内容类

### .doc 解析结果可能乱序

老式二进制 `.doc` 的文本抽取可能夹带格式噪声或顺序错乱。察觉到异常时的处理顺序：

1. 提示用户用 Word/WPS 另存为 `.docx` 后重新解析（最可靠）
2. 用 **Read 工具**直接读取该 `.doc` 文件
3. 直接从公告正文里找信息（有些公告把关键内容写在正文而非附件）

### 职位表合并单元格

岗位表大量使用纵向合并（"招聘单位""招聘人数"跨多行）。**必须回填**，否则同一岗位的后续行会缺单位名，导致岗位数与人数统计出错。

`parse_attachment.py` 的策略：跨行的合并回填到每个单元格，仅同行的横向合并只保留首格（避免整行被重复文字灌满）。

### 岗位数 ≠ 招聘人数

一个岗位可能招多人（如"急诊科医师"招 2 人）。**两个数字要分别统计**，数据卡上分开呈现：`9个岗位 / 10人 / 5家单位`。

---

## 五、排版类

### 不要凭记忆手写排版 HTML

`gzh-design` 的组件库是单一来源，**必须 Read 对应主题的组件库文件**再取用 HTML。手写的样式粘贴到公众号编辑器后极易丢失。

### 推图位用通用库占位组件

所有主题共用的 `common-components.md` 里有居中虚线占位组件，推图位统一用它。

### 校验与预览必须都跑

```bash
python "<gzh-design>/scripts/validate_gzh_html.py" "<排版HTML>"
python "<gzh-design>/scripts/wrap_preview.py" "<排版HTML>"
```

前者检查 HTML 是否符合公众号粘贴要求（目标 0 ERROR），后者生成带「复制到公众号」按钮的预览页。

### 改一处要同步两版

排版 HTML 与草稿 MD 是两份独立文件，**任何改动都要同步**，否则交付的两版内容会不一致。改完后用 Grep 搜关键词确认两处都改了。
