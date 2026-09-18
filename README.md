# 公告推文生成器 · gonggao-tuiwen

> 丢一条招考公告链接，自动产出两份公众号成稿：**参考排版版 HTML** + **纯草稿 Markdown**。

仓库地址：<https://github.com/charleshugo819/gonggao-tuiwen-skill>

---

## 它能做什么

给一个政府/事业单位的招考公告 URL，它会自动完成：

1. **抓取公告** —— 正文、附件、图片清单一次拿全
2. **解析职位表** —— `.xlsx` / `.docx` / `.doc` 全部转成可读文本（含合并单元格还原）
3. **检索考情** —— 搜同地区历年同类批次的笔试形式、时长、合格线
4. **按爆款结构写稿** —— 800–1500 字，正式直白，数据用表格承载
5. **去 AI 味** —— 清掉公文套话、句式重复、长段
6. **合规自检** —— 导流红线、绝对化用语、事实一致性
7. **产出两份版式** —— 排版 HTML（带预览页）+ 纯草稿 MD

适用于国省考、事业单位、医疗卫生、教师、国企等各类招考公告。

---

## 安装

**方式一：从 GitHub 克隆（推荐）**

```bash
git clone https://github.com/charleshugo819/gonggao-tuiwen-skill.git gonggao-tuiwen
mv gonggao-tuiwen ~/.workbuddy/skills/
```

注意第二步把目录名改成 `gonggao-tuiwen`，与 `SKILL.md` 里的 `name` 字段保持一致。

**方式二：手动放置**

把 `gonggao-tuiwen` 整个文件夹放到下面任一位置：

| 范围 | 路径 |
|---|---|
| 用户级（推荐，所有项目可用）| `~/.workbuddy/skills/` |
| 项目级（仅当前项目）| `<项目目录>/.workbuddy/skills/` |

放好后新开一轮对话即可被识别。

**无需安装任何 Python 包**——四个脚本全部基于标准库。有 `openpyxl` 时职位表解析更精确，没有也能跑（自动回退）。

---

## 依赖（全部已内置 / 可选）

**开箱即用**：排版引擎已内嵌在 `vendor/gzh-design/`，抓取解析脚本零第三方依赖，
克隆下来即可跑完整链路，**不需要另外装 anything**。

| 能力 | 来源 | 说明 |
|---|---|---|
| 公众号排版 | **内置** `vendor/gzh-design/` | 9 套主题组件库 + 校验/预览脚本，自足 |
| 去 AI 味检测 | 可选 `qu-aiwei-zh` | 无则用内置 `references/rewrite-rules.md` 人工复读 |
| 爆款结构参考 | 可选 `wechat-viral-article` | 无则用内置 `references/article-structure.md` |
| 合规自检 | 可选 `publish-safety-officer` | 无则用内置 `references/compliance.md` |

可选的三项装了效果更好，不装也能正常出稿。它们可在 WorkBuddy 推荐市场一键安装。

> **关于内置排版引擎**：`vendor/gzh-design/` 是上游 [gzh-design] 的快照，
> 不会自动跟随更新。上游有新主题/新规范时，按 `SKILL.md` 的
> 「同步上游 gzh-design 的更新」一节手动同步一次即可。

---

## 怎么用

直接发链接，一句话说需求即可：

```
https://www.xxx.gov.cn/xxx/post_3940103.html
按这个公告写一篇公众号推文
```

也可以补充要求：

```
<公告链接> 写成推文，用红白色系，控制在1200字左右
<公告链接> 只要草稿版，不用排版
```

**开始前会先问你选哪套模版**——选项固定为 **自研三套 + 红白色系**，最贴题的那套标"（推荐）"，你选定后它才开工，不先做再返工。

| 选项 | 主题 | 适合 |
|---|---|---|
| 1 | 公告速读蓝 `notice-blue` | 招聘公告、考试通知（招聘类默认推荐） |
| 2 | 考点科普绿 `guide-green` | 考情科普、备考攻略、答疑 |
| 3 | 榜单数据橙 `rank-amber` | 分数线、竞争比、排行榜 |
| 4 | 红白色系 `red-white` | 深度分析、观点、劝考 |

**点"其他"或说"还有别的吗"** → 再列出剩余 5 套：摸鱼绿 / 石墨极简风 / 留白禅意风 / 摸鱼票据风 / 橄榄手记（完整信息见 `vendor/gzh-design/references/theme-index.md`）。

**不想被问**：直接说"你定"或"直接排"，它就用推荐那套开工；你已经点名了模版它也不会再问。

---

## 产出长什么样

工作目录下会得到：

| 文件 | 用途 |
|---|---|
| `<标题>_排版_<主题>.html` | 排版成品，手动全选粘贴的兜底版 |
| `<标题>_排版_<主题>_预览.html` | **推荐用这个**——浏览器打开，点「复制到公众号」再粘贴 |
| `<标题>_草稿.md` | 不套任何模板的纯 Markdown 草稿 |

外加过程材料：`公告正文.txt`、`attachments/`、各附件的 `*_dump.txt`。

---

## 推文结构（固定三章）

```
前言（报名时间 + 报名方式）
  ↓ 推图位：领取岗位表
01 公告提要      —— 数据卡 / 用人单位 / 学历门槛 / 专业需求 / 执业资格
                    ↓ 推图位：领取岗位表
02 报名与考试安排 —— 时间表 / 报名确认 / 开考比例 / 笔试考情 / 面试 / 总成绩
03 报考资格      —— 学历证书 / 年龄口径 / 应届生类别 / 不得报考情形
  ↓ 推图位：备考资料
```

**顺序不是随意的**——它服从读者的决策链：是不是编制 → 招多少人 → 我够不够格 → 岗位在哪 → 怎么报 → 有什么坑。详见 `references/article-structure.md`。

推图位是留给运营自己补图的占位框。注意图上别写"关注领取""转发领取"，属诱导关注会被限流。**推图位文案一律指向内部**（领取岗位表 / 备考资料），不出现"源文公告"这类把人引向官方原文的表述。

---

## 目录结构

```
gonggao-tuiwen/
├── SKILL.md                      主流程（八步）
├── README.md                     本文件
├── scripts/
│   ├── fetch_announcement.py     抓公告正文 + 下载附件 + 导出图片清单
│   ├── parse_attachment.py       附件转文本（xlsx/docx/doc，零依赖）
│   ├── html_to_plain.py          排版 HTML 抽纯文本（供 AI 味检测）
│   └── count_words.py            正文字数统计 + 分节统计
├── examples/
│   └── 示例-成稿参考.md          真实公告的成品示例（看长什么样）
├── references/
│   ├── article-structure.md      推文结构模板与写作规范
│   ├── rewrite-rules.md          去 AI 味改写规则
│   ├── compliance.md             合规自检清单
│   └── pitfalls.md               实战踩坑记录
└── vendor/
    └── gzh-design/               内置排版引擎（自足，无需外部安装）
        ├── SKILL.md              排版规范（微信铁律、组件规范）
        ├── references/           9 套主题组件库 + 通用组件 + 主题索引
        └── scripts/              validate_gzh_html.py / wrap_preview.py / component_lint.py
```

---

## 脚本单独用也行

四个脚本都是独立的命令行工具，可以脱离 skill 直接跑：

```bash
python scripts/fetch_announcement.py "<公告URL>" --out "<工作目录>"
python scripts/parse_attachment.py "<工作目录>/attachments"
python scripts/count_words.py "<草稿.md>" --min 800 --max 1500
python scripts/html_to_plain.py "<排版.html>" --out html_plain.txt
```

Windows 上若系统没有 `python` 命令，用托管解释器全路径：

```
C:\Users\<用户名>\.workbuddy\binaries\python\versions\3.13.12\python.exe
```

---

## 已知限制

- **JS 动态渲染的公告页**抓不到正文（脚本会告警），改用 WebFetch 工具抓
- **图片版职位表**需要 `--download-images` 后由模型读图提取
- **老式 `.doc`** 二进制解析可能夹带噪声；最可靠的做法是先用 Word/WPS 转存 `.docx`
- 考情检索依赖公开网络信息，**查不到就跳过，不会编造**
