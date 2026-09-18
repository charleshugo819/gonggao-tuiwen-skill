# 主题索引与选择决策表

本表是主题信息的**单一来源**。工作流第 1 步据此向用户展示选项，第 2 步据"组件库文件"列读取对应库，下划线标记时据"正文下划线 CSS"列取值。

每个主题的**英文标识**（用于产物命名 `{中文名}({标识}).html`、Agent 引用）= "组件库文件"列去掉 `theme-` 前缀与 `.md` 后缀。展示给用户仍用中文名。

## 已注册主题

| 主题 | 主色 | 适用场景 | 组件库文件 | 正文下划线 CSS |
|------|------|---------|-----------|---------------|
| 摸鱼绿 | `#0F766E` 青碧 | 教程、测评、清单、工具盘点（卡片丰富、信息密度高，默认推荐） | `references/theme-moyu-green.md` | `border-bottom:2px solid #99F6E4;font-weight:600;` |
| 红白色系 | `#B91C1C` 朱砂 | 深度分析、观点、力量感话题（经典编辑风，编号章节+引言卡+签名区，红色克制点睛） | `references/theme-red-white.md` | `border-bottom:2px solid #FCA5A5;font-weight:600;` |
| 石墨极简风 | `#475569` 石板灰蓝 | 设计、科技评论、专业观点、高端品牌（极简克制、留白理性、全灰阶） | `references/theme-graphite-minimal.md` | `border-bottom:2px solid #475569;font-weight:600;` |
| 留白禅意风 | `#556B4F` 橄榄墨绿 | 禅意冥想、极简生活、深度随笔、艺术留白（呼吸感最强） | `references/theme-zen-whitespace.md` | `border-bottom:1.5px solid #BCC9B2;font-weight:500;` |
| 摸鱼票据风 | `#4F46E5` 靛蓝 | 测评、工具对比、创意评测（票据/门票视觉隐喻，星级评分+编号+硬阴影卡片） | `references/theme-moyu-ticket.md` | `border-bottom:2px solid #C7D2FE;font-weight:600;` |
| 橄榄手记 | `#1e1f23` 墨黑（配砖红棕 `#A14E1E`） | 内刊手记、深度评测、案例复盘、系统性说明文档（编辑部内刊质感，分节形式多样，信息密度偏高） | `references/theme-olive-journal.md` | `border-bottom:2px solid #A14E1E;font-weight:600;` |
| 公告速读蓝 | `#2563EB` 正蓝 | 招聘公告、考试通知、政策解读、报名提醒（公告信息速览卡为核心，时间/人数/方式一眼可扫，官方可信） | `references/theme-notice-blue.md` | `border-bottom:2px solid #BFDBFE;font-weight:600;` |
| 考点科普绿 | `#059669` 正绿 | 考情科普、备考攻略、常见问题解答、知识梳理（编号要点块为骨架，结论先行，引流内嵌要点之间） | `references/theme-guide-green.md` | `border-bottom:2px solid #A7F3D0;font-weight:600;` |
| 榜单数据橙 | `#EA580C` 正橙 | 招录数据、竞争比分析、分数线汇总、排行榜单（榜单条目卡+数据表格，高位橙/低位灰对比鲜明） | `references/theme-rank-amber.md` | `border-bottom:2px solid #FED7AA;font-weight:600;` |

## 选择建议

- **用户选择制**：用户没指定主题时，把本表全部主题列给用户选（中文名 + 适用场景），不替用户定；最贴合题材的主题可标"（推荐）"放第一位。
- 全自动模式（用户明说"直接排"）才自动选：默认第一行主题，题材明显契合其它主题时选契合项并在交付时说明理由。
- 同一篇文章只用一套主题，不混搭。

## 下划线色值的权威性

正文关键词下划线一律用上表"正文下划线 CSS"列的值。组件库里可能有浅色下划线变体，那是可选样式；**正文关键词标记以本表为单一权威来源**，避免双轨。

## 新主题登记流程

1. 把主题组件库写入 `references/theme-{英文标识}.md`（格式要求见 SKILL.md「添加新主题的规范」）。
2. 在上表登记一行；首个/最常用主题放第一行作为默认推荐。
3. 跑 `python3 scripts/component_lint.py .` 确认 0 ERROR。

> 用户想要全新风格时，可走 `references/theme-generator.md` 的自定义主题生成流程：按偏好/参考图生成区块库（预览存 `assets/theme-previews/`），确认后转标准主题库并按上面流程登记。
