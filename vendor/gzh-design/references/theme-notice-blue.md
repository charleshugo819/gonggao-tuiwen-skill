# 公众号排版组件库 —— 公告速读蓝

> **使用说明**：本组件库为「公告速读蓝」主题（招聘公告速读风），所有组件使用**内联样式**，可直接复制粘贴到微信公众号编辑器。
>
> **设计风格**：蓝白干净 + 信息优先。以"公告信息速览卡"为核心视觉，把招聘人数、报名时间、报名方式等关键信息做成一眼可扫的网格；公告原文用浅灰底容器收纳，与速览信息形成层次。蓝色只在锚点与结构线出现，克制不喧哗。适合招聘公告、考试通知、政策解读、报名提醒类文章。
>
> **公众号平台限制须知**：
> - ❌ 不支持 `<style>`/`<script>`、CSS class/id、`position:fixed/absolute`、`float`、`@media`/`@keyframes`、`display:grid`
> - ✅ 支持内联 `style`、`display:flex`（有限）、`linear-gradient`、`border-radius`、`box-shadow`、`<section>/<p>/<span>/<strong>/<img>` 等基础标签
>
> **WeChat 兼容铁律**（本主题组件全部已按此写好，改动时必须遵守）：
> - 所有"装饰性空元素"（渐变分割线、END 短线、时间线圆点与竖线）**必须在内部放 `<span leaf=""><br></span>` 占位**，否则微信会剥掉样式
> - **不要把 `font-size`/`border-bottom` 打在 `<strong>` 上**，也不要在同一个 `<p>` 里混多个不同 `font-size`——微信编辑器会自动"纠正"导致样式被重写。正确做法：拆成多个 `<p>`，每个 `<p>` 只有一个字号；高亮样式统一挂在外层 `<span>` 上
> - 不用 `position:absolute` 做划线/高亮
> - 结构化区域（图片说明、作者署名）没有内容时**整块删掉**，不留空 section
> - 正文字号严格用 `14px`、行高 `2.5`、段间距 `margin-bottom:2.5em`（见 SKILL.md「全局排版参数」）；卡片 / 列表 / 表格 / 引用块自身的 `margin` 是组件留白，不跟随修改

---

## 设计变量速查表

```
主色调：       #2563EB（正蓝）
主色调深：     #1D4ED8（深蓝，实底块专用）
主色调浅：     #BFDBFE（浅蓝，结构线/下划线）
主色调极浅：   #DBEAFE（淡蓝，标签底）
主色调背景：   #EFF6FF（极淡蓝底）
标记色：       #BFDBFE（下划线专用）
标题色：       #111827（近黑）
正文色：       #1F2937（深灰）
辅助文字色：   #6B7280（中灰）
分割线色：     #E5E7EB
灰竖条：       #D1D5DB（灰底旁注左竖条）
正文字号：     14px（不可改）
行高：         2.5
段间距：       2.5em（=35px，写在正文段落 margin-bottom）
字间距：       2px
最大宽度：     677px
内容区边距：   0 10px（左右各 10px）
```

字体栈：`-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif`

---

## 组件 1 全局容器

```html
<section style="max-width:677px;margin:0 auto;background:#ffffff;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;color:#1F2937;line-height:1.75;letter-spacing:2px;overflow-x:hidden;">

  <!-- 所有组件放在这里 -->

</section>
```

---

## 组件 2 顶部公告标签条

> 放日期与"本文包含广告营销信息"合规声明。**合规声明不可省**（招聘/课程类内容必须标注）。

```html
<section style="padding:20px 10px 0;">
  <p style="margin:0;font-size:12px;color:#6B7280;letter-spacing:2px;text-align:center;">
    <span leaf="">{{日期}} · 招聘公告</span>
  </p>
  <p style="margin:10px 0 0;text-align:center;">
    <span style="display:inline-block;background:#DBEAFE;color:#1D4ED8;font-size:11px;font-weight:700;padding:3px 12px;border-radius:999px;letter-spacing:2px;"><span leaf="">本文包含广告营销信息</span></span>
  </p>
</section>
```

---

## 组件 3 公告主标题卡（白底蓝色光晕）

> **文案策略**：标题卡主标题写"人群词 + 利益点"（如「本科起报！」「报名开始！」），导语补一句这条公告跟谁有关、最需要知道什么。

```html
<section style="margin:18px 10px 26px;background:#ffffff;border-radius:12px;box-shadow:0 6px 26px -6px rgba(37,99,235,0.18);padding:26px 22px 22px;overflow:hidden;">
  <p style="margin:0 0 10px;font-size:11px;color:#2563EB;font-weight:700;letter-spacing:3px;">
    <span leaf="">RECRUITMENT</span>
  </p>
  <p style="margin:0;font-size:20px;font-weight:900;color:#111827;line-height:1.5;">
    <span leaf="">{{主标题}}</span>
  </p>
  <section style="height:1px;background:linear-gradient(to right,#2563EB,#BFDBFE,transparent);margin:16px 0 14px;">
    <span leaf=""><br></span>
  </section>
  <p style="margin:0;font-size:13px;color:#6B7280;line-height:1.8;">
    <span leaf="">{{一句话导语}}</span>
  </p>
</section>
```

---

## 组件 4 公告信息速览卡（本主题核心组件）

> 招聘/考试公告的最关键一块。**双列网格**放 4 项短信息（人数、对象、时间、考试），**深蓝实底块**放"报名方式"这类需要完整表述的长信息。读者 3 秒内能决策要不要往下看。

### 4a. 速览区外壳 + 双列信息格

```html
<section style="padding:0 10px;margin-bottom:26px;">
  <p style="margin:0 0 14px;font-size:12px;color:#6B7280;letter-spacing:2px;">
    <span leaf="">📋 公告重要信息</span>
  </p>

  <section style="display:flex;margin-bottom:10px;">
    <section style="flex:1;background:#EFF6FF;border-radius:10px;padding:14px 14px;margin-right:10px;border:1px solid #DBEAFE;">
      <p style="margin:0 0 4px;font-size:11px;color:#6B7280;letter-spacing:1px;"><span leaf="">招聘人数</span></p>
      <p style="margin:0;font-size:19px;font-weight:900;color:#1D4ED8;line-height:1.2;"><span leaf="">{{数字}}</span></p>
    </section>
    <section style="flex:1;background:#EFF6FF;border-radius:10px;padding:14px 14px;border:1px solid #DBEAFE;">
      <p style="margin:0 0 4px;font-size:11px;color:#6B7280;letter-spacing:1px;"><span leaf="">招聘对象</span></p>
      <p style="margin:0;font-size:15px;font-weight:800;color:#1D4ED8;line-height:1.4;"><span leaf="">{{对象}}</span></p>
    </section>
  </section>

  <section style="display:flex;margin-bottom:10px;">
    <section style="flex:1;background:#EFF6FF;border-radius:10px;padding:14px 14px;margin-right:10px;border:1px solid #DBEAFE;">
      <p style="margin:0 0 4px;font-size:11px;color:#6B7280;letter-spacing:1px;"><span leaf="">报名时间</span></p>
      <p style="margin:0;font-size:14px;font-weight:800;color:#1D4ED8;line-height:1.5;"><span leaf="">{{起}}</span></p>
      <p style="margin:2px 0 0;font-size:13px;font-weight:800;color:#1D4ED8;line-height:1.5;"><span leaf="">{{止}}</span></p>
    </section>
    <section style="flex:1;background:#EFF6FF;border-radius:10px;padding:14px 14px;border:1px solid #DBEAFE;">
      <p style="margin:0 0 4px;font-size:11px;color:#6B7280;letter-spacing:1px;"><span leaf="">笔试时间</span></p>
      <p style="margin:0;font-size:15px;font-weight:800;color:#1D4ED8;line-height:1.5;"><span leaf="">{{笔试}}</span></p>
    </section>
  </section>
```

### 4b. 长信息实底块（报名方式 / 关键操作）

```html
  <section style="background:#1D4ED8;border-radius:10px;padding:16px 18px;">
    <p style="margin:0 0 6px;font-size:11px;color:#BFDBFE;letter-spacing:2px;"><span leaf="">报名方式</span></p>
    <p style="margin:0;font-size:13px;color:#FFFFFF;line-height:1.8;">
      <span leaf="">{{完整表述}}</span>
    </p>
  </section>
</section>
```

> **注意**：深蓝实底块在一篇里**只用 1 处**（视觉焦点），其余长信息用速览卡的 4c 单列信息条。

### 4c. 单列信息条（长文本信息项）

```html
<section style="padding:0 10px;margin-bottom:26px;">
  <section style="background:#F9FAFB;border-radius:10px;padding:14px 16px;margin-bottom:10px;border-left:3px solid #2563EB;">
    <p style="margin:0 0 4px;font-size:12px;color:#2563EB;font-weight:700;letter-spacing:1px;"><span leaf="">{{信息项名}}</span></p>
    <p style="margin:0;font-size:13px;color:#1F2937;line-height:1.8;"><span leaf="">{{信息内容}}</span></p>
  </section>
</section>
```

---

## 组件 5 章节标题（蓝色实底编号 + 标题）

> 蓝色实底编号标签 + 英文小标签 + 中文大标题，底部蓝色实线。第一章 `margin-top:16px`，后续章节 `margin-top:44px`。

```html
<section style="margin-top:44px;margin-bottom:24px;padding:0 10px;">
  <section style="display:flex;align-items:center;margin-bottom:18px;padding-bottom:14px;border-bottom:2px solid #2563EB;">
    <span style="display:inline-block;background:#2563EB;color:#FFFFFF;font-size:16px;font-weight:900;padding:4px 13px;border-radius:6px;margin-right:12px;line-height:1.3;"><span leaf="">01</span></span>
    <section>
      <p style="font-size:11px;color:#2563EB;font-weight:700;letter-spacing:3px;margin:0 2px 2px;text-transform:uppercase;">
        <span leaf="">{{ENGLISH TAG}}</span>
      </p>
      <h3 style="font-size:18px;font-weight:800;color:#111827;margin:0;letter-spacing:1px;">
        <span leaf="">{{中文章节标题}}</span>
      </h3>
    </section>
  </section>
</section>
```

**结语章节变体**（编号用 `∞`，英文标签用 `THE END`）：

```html
<span style="display:inline-block;background:#2563EB;color:#FFFFFF;font-size:16px;font-weight:900;padding:4px 13px;border-radius:6px;margin-right:12px;line-height:1.3;"><span leaf="">∞</span></span>
```

---

## 组件 6 子标题（红色左竖条 → 蓝色左竖条）

> `###` 子标题用蓝色左竖条 + 深色标题，**不套用组件 5 的编号章节样式**。

```html
<p style="margin:26px 0 14px;padding-left:10px;border-left:3px solid #2563EB;font-size:14px;font-weight:800;color:#111827;line-height:1.4;">
  <span leaf="">{{子标题}}</span>
</p>
```

---

## 组件 7 正文段落

> **关键规则**：每段主动识别 1~3 个关键短语，用**淡蓝下划线（7d）**标记——这是本主题的基础标记。

### 基础段落

```html
<p style="margin:0 0 2.5em;font-size:14px;line-height:2.5;text-align:justify;">
  <span leaf="">{{正文内容}}</span>
</p>
```

### 带关键词下划线标记的段落（默认）

```html
<p style="margin:0 0 2.5em;font-size:14px;line-height:2.5;text-align:justify;">
  <span leaf="">{{前半句}}</span>
  <span style="border-bottom:2px solid #BFDBFE;font-weight:600;"><span leaf="">{{需要强调的关键短语}}</span></span>
  <span leaf="">{{后半句}}</span>
</p>
```

**标记原则**：每段选 1~3 个关键短语（4~15 字）加下划线，不要整段都标；优先标时间节点、数字、报名条件、关键结论。

---

## 组件 8 正文高亮样式

> **优先级**：① 淡蓝下划线（正文默认标记）→ ② 普通加粗为主、蓝色加粗仅锚点 → ③ 浅蓝底深蓝字标签（每篇 2~4 个）

### 8a. 加粗强调

普通加粗（默认，绝大部分加粗用这个）：

```html
<strong><span leaf="">普通加粗强调</span></strong>
```

蓝色加粗（仅限关键时间/条件/CTA 等锚点，全文 ≤5 处）：

```html
<strong style="color:#2563EB;"><span leaf="">蓝色加粗锚点</span></strong>
```

### 8b. 浅蓝底深蓝字标签（核心概念 / 关键条件，每篇 2~4 个）

```html
<span style="background:#DBEAFE;color:#1E40AF;padding:2px 7px;border-radius:3px;font-weight:700;"><span leaf="">关键条件标签</span></span>
```

### 8c. 淡蓝下划线（最常用，本风格基础标记）

```html
<span style="border-bottom:2px solid #BFDBFE;font-weight:600;"><span leaf="">淡蓝下划线关键词</span></span>
```

### 8d. 行内代码

```html
<span style="background:#F3F4F6;color:#1F2937;padding:2px 6px;border-radius:4px;font-size:14px;font-weight:600;"><span leaf="">code</span></span>
```

---

## 组件 9 引用 / 提示 / 旁注块（3 种变体）

### 9a. 蓝色提示条（重要提醒）

```html
<section style="background:#EFF6FF;border-left:4px solid #2563EB;border-radius:0 8px 8px 0;padding:14px 18px;margin-bottom:24px;">
  <p style="margin:0 0 6px;">
    <span style="display:inline-block;background:#2563EB;color:#FFFFFF;font-size:11px;font-weight:700;padding:2px 10px;border-radius:4px;letter-spacing:1px;"><span leaf="">提醒</span></span>
  </p>
  <p style="margin:0;font-size:13px;color:#1F2937;line-height:2.2;">
    <span leaf="">{{提示内容}}</span>
  </p>
</section>
```

类型小标签文字可换：`提醒` / `注意` / `重点` / `材料清单`。

### 9b. 蓝色引用块（含边框，放公告原文 / 政策条款）

```html
<section style="background:#EFF6FF;border-radius:10px;padding:16px 18px;margin-bottom:24px;border:1px solid #BFDBFE;">
  <p style="margin:0;font-size:13px;color:#1F2937;line-height:2.2;text-align:justify;">
    <span leaf="">{{引用内容}}</span>
  </p>
</section>
```

### 9c. 灰色旁注块（轻量补充、口径解释）

```html
<section style="border-left:4px solid #D1D5DB;padding:13px 18px;margin-bottom:24px;background:#F9FAFB;border-radius:0 8px 8px 0;">
  <p style="margin:0;font-size:13px;color:#4B5563;line-height:2.2;text-align:justify;">
    <span leaf="">{{旁注内容}}</span>
  </p>
</section>
```

---

## 组件 10 公告原文收纳容器

> 公告全文很长时用它收纳，浅灰底 + 虚线边框与速览卡区分层次。**这是本主题唯一允许 dashed 的场景**（表达"原文摘录"的容器语义）。

```html
<section style="background:#F9FAFB;border-radius:12px;padding:20px 18px;margin-bottom:24px;border:1px dashed #D1D5DB;">
  <p style="margin:0 0 12px;font-size:12px;color:#6B7280;letter-spacing:2px;">
    <span leaf="">📄 公告原文</span>
  </p>
  <p style="margin:0 0 1.6em;font-size:13px;color:#4B5563;line-height:2.2;text-align:justify;">
    <span leaf="">{{原文段落}}</span>
  </p>
</section>
```

---

## 组件 11 列表组件

### 11a. 编号要点块（红色圆标 → 蓝色圆标）

```html
<section style="margin-bottom:22px;">
  <section style="display:flex;align-items:flex-start;margin-bottom:14px;">
    <span style="display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;background:#2563EB;color:#FFFFFF;font-size:12px;font-weight:700;border-radius:50%;flex-shrink:0;margin-top:3px;"><span leaf="">1</span></span>
    <p style="margin:0 0 0 12px;font-size:14px;line-height:2.2;flex:1;text-align:justify;">
      <strong><span leaf="">{{要点标题}}</span></strong>
      <span leaf="">，{{要点说明}}</span>
    </p>
  </section>
</section>
```

### 11b. 药丸要点列表（短标题 + 说明）

```html
<section style="margin-bottom:18px;">
  <p style="margin:0 0 8px;">
    <span style="display:inline-block;background:#DBEAFE;color:#1E40AF;font-size:13px;font-weight:700;padding:3px 12px;border-radius:999px;"><span leaf="">{{要点标题}}</span></span>
  </p>
  <p style="margin:0;font-size:13px;color:#4B5563;line-height:2.2;text-align:justify;">
    <span leaf="">{{要点说明}}</span>
  </p>
</section>
```

### 11c. 时间线（报考流程 / 关键节点）

```html
<section style="display:flex;margin-bottom:24px;">
  <section style="display:flex;flex-direction:column;align-items:center;margin-right:16px;flex-shrink:0;">
    <section style="width:14px;height:14px;border-radius:50%;border:3px solid #2563EB;background:#fff;margin-top:4px;"><span leaf=""><br></span></section>
    <section style="width:2px;background:#DBEAFE;flex:1;margin-top:4px;min-height:48px;"><span leaf=""><br></span></section>
  </section>
  <section style="flex:1;padding-bottom:14px;">
    <p style="margin:0 0 6px;font-size:14px;font-weight:800;color:#111827;"><span leaf="">{{节点标题}}</span></p>
    <p style="margin:0;font-size:13px;color:#4B5563;line-height:2.2;text-align:justify;"><span leaf="">{{节点内容}}</span></p>
  </section>
</section>
```

最后一个节点去掉竖线段（`<section style="width:2px;...">` 那一行整块删掉）。

---

## 组件 12 数据组件

### 12a. 两列数据卡

```html
<section style="display:flex;margin-bottom:24px;padding:0;">
  <section style="flex:1;background:#EFF6FF;border-radius:10px;padding:18px 14px;margin-right:10px;text-align:center;border:1px solid #DBEAFE;">
    <p style="margin:0 0 4px;font-size:24px;font-weight:900;color:#1D4ED8;line-height:1;"><span leaf="">{{数字}}</span></p>
    <p style="margin:0;font-size:12px;color:#6B7280;"><span leaf="">{{说明}}</span></p>
  </section>
  <section style="flex:1;background:#EFF6FF;border-radius:10px;padding:18px 14px;text-align:center;border:1px solid #DBEAFE;">
    <p style="margin:0 0 4px;font-size:24px;font-weight:900;color:#1D4ED8;line-height:1;"><span leaf="">{{数字}}</span></p>
    <p style="margin:0;font-size:12px;color:#6B7280;"><span leaf="">{{说明}}</span></p>
  </section>
</section>
```

### 12b. 三列数据卡

```html
<section style="display:flex;margin-bottom:24px;padding:0;">
  <section style="flex:1;background:#EFF6FF;border-radius:10px;padding:16px 8px;margin-right:8px;text-align:center;border:1px solid #DBEAFE;">
    <p style="margin:0 0 4px;font-size:20px;font-weight:900;color:#1D4ED8;line-height:1;"><span leaf="">{{数字}}</span></p>
    <p style="margin:0;font-size:11px;color:#6B7280;"><span leaf="">{{说明}}</span></p>
  </section>
  <section style="flex:1;background:#EFF6FF;border-radius:10px;padding:16px 8px;margin-right:8px;text-align:center;border:1px solid #DBEAFE;">
    <p style="margin:0 0 4px;font-size:20px;font-weight:900;color:#1D4ED8;line-height:1;"><span leaf="">{{数字}}</span></p>
    <p style="margin:0;font-size:11px;color:#6B7280;"><span leaf="">{{说明}}</span></p>
  </section>
  <section style="flex:1;background:#EFF6FF;border-radius:10px;padding:16px 8px;text-align:center;border:1px solid #DBEAFE;">
    <p style="margin:0 0 4px;font-size:20px;font-weight:900;color:#1D4ED8;line-height:1;"><span leaf="">{{数字}}</span></p>
    <p style="margin:0;font-size:11px;color:#6B7280;"><span leaf="">{{说明}}</span></p>
  </section>
</section>
```

### 12c. 数据表格（真实数据表用）

```html
<section style="margin-bottom:24px;overflow-x:auto;">
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <thead>
      <tr>
        <th style="background:#2563EB;color:#fff;font-weight:700;padding:9px 12px;text-align:left;"><span leaf="">{{列标题}}</span></th>
        <th style="background:#2563EB;color:#fff;font-weight:700;padding:9px 12px;text-align:center;"><span leaf="">{{列标题}}</span></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:9px 12px;border-bottom:1px solid #DBEAFE;color:#1F2937;"><span leaf="">{{内容}}</span></td>
        <td style="padding:9px 12px;border-bottom:1px solid #DBEAFE;color:#1F2937;text-align:center;"><span leaf="">{{内容}}</span></td>
      </tr>
      <tr>
        <td style="padding:9px 12px;border-bottom:1px solid #DBEAFE;color:#1F2937;background:#EFF6FF;"><span leaf="">{{内容}}</span></td>
        <td style="padding:9px 12px;border-bottom:1px solid #DBEAFE;color:#1F2937;background:#EFF6FF;text-align:center;"><span leaf="">{{内容}}</span></td>
      </tr>
    </tbody>
  </table>
</section>
```

---

## 组件 13 图片容器

```html
<section style="background:#FFF;border-radius:12px;padding:6px;border:1px solid #E5E7EB;box-shadow:0 4px 12px -2px rgba(0,0,0,0.06);margin-bottom:10px;">
  <section style="margin:0;border-radius:8px;overflow:hidden;">
    <span leaf=""><img src="{{图片URL}}" style="max-width:100%;height:auto;display:block;margin:0 auto;"></span>
  </section>
</section>
```

带说明文字时，图片 `margin-bottom` 改 `8px`，其后加：

```html
<p style="font-size:12px;color:#9CA3AF;text-align:center;margin:0 0 24px;">
  <span leaf="">— {{图片说明}}</span>
</p>
```

---

## 组件 14 待补素材占位（居中板块）

> 文章里「配图建议」、待补截图 / 图表等占位，一律用这个**居中**板块。

```html
<section style="margin:0 0 24px;padding:28px 20px;border:1.5px dashed #DAD7D2;border-radius:14px;background:#FAFAF8;text-align:center;">
  <p style="margin:0 0 10px;font-size:24px;line-height:1;"><span leaf="">🖼</span></p>
  <p style="margin:0;font-size:13px;font-weight:700;color:#9CA3AF;letter-spacing:2px;"><span leaf="">待补素材</span></p>
  <p style="margin:8px 0 0;font-size:12px;color:#B8B5B0;line-height:1.8;"><span leaf="">此处插入：{{素材说明}}</span></p>
</section>
```

图标按素材类型换：🎬 视频/录屏、🖼 图片、📊 信息图、📎 附件。

---

## 组件 15 引流组件（公告类专用）

> **位置原则**：紧贴读者的需求点，不要全部堆到文末。公告类通常放在速览信息之后、原文收纳之前。

### 15a. 资料推荐卡

```html
<section style="background:#EFF6FF;border-radius:12px;padding:18px 18px;margin-bottom:16px;border:1px solid #BFDBFE;">
  <p style="margin:0 0 10px;font-size:12px;color:#1D4ED8;font-weight:700;letter-spacing:2px;">
    <span leaf="">📚 资料推荐</span>
  </p>
  <p style="margin:0 0 12px;font-size:14px;font-weight:800;color:#111827;line-height:1.6;">
    <span leaf="">{{资料名称}}</span>
  </p>
  <p style="margin:0 0 12px;font-size:13px;color:#4B5563;line-height:2.0;">
    <span leaf="">{{资料说明}}</span>
  </p>
  <p style="margin:0;">
    <span style="display:inline-block;background:#2563EB;color:#FFFFFF;font-size:13px;font-weight:700;padding:8px 22px;border-radius:8px;"><span leaf="">{{领取方式}}</span></span>
  </p>
</section>
```

### 15b. 双资料并排卡

```html
<section style="display:flex;margin-bottom:24px;">
  <section style="flex:1;background:#F9FAFB;border-radius:10px;padding:14px 12px;margin-right:10px;border:1px solid #E5E7EB;">
    <p style="margin:0 0 6px;font-size:13px;font-weight:800;color:#111827;line-height:1.5;"><span leaf="">{{资料名称}}</span></p>
    <p style="margin:0 0 8px;font-size:12px;color:#6B7280;line-height:1.8;"><span leaf="">{{资料说明}}</span></p>
    <p style="margin:0;font-size:14px;font-weight:900;color:#1D4ED8;"><span leaf="">{{价格}}</span></p>
  </section>
  <section style="flex:1;background:#F9FAFB;border-radius:10px;padding:14px 12px;border:1px solid #E5E7EB;">
    <p style="margin:0 0 6px;font-size:13px;font-weight:800;color:#111827;line-height:1.5;"><span leaf="">{{资料名称}}</span></p>
    <p style="margin:0 0 8px;font-size:12px;color:#6B7280;line-height:1.8;"><span leaf="">{{资料说明}}</span></p>
    <p style="margin:0;font-size:14px;font-weight:900;color:#1D4ED8;"><span leaf="">{{价格}}</span></p>
  </section>
</section>
```

### 15c. CTA 引导块（深蓝实底）

```html
<section style="background:#1D4ED8;border-radius:12px;padding:20px 20px;margin-bottom:24px;">
  <p style="margin:0 0 8px;font-size:15px;font-weight:800;color:#FFFFFF;line-height:1.7;">
    <span leaf="">{{引导文案}}</span>
  </p>
  <p style="margin:0;font-size:13px;color:#BFDBFE;line-height:1.9;">
    <span leaf="">{{补充说明}}</span>
  </p>
</section>
```

### 15d. 服务标签胶囊组

```html
<p style="text-align:center;margin:0 0 24px;">
  <span style="display:inline-block;background:#DBEAFE;color:#1E40AF;font-size:12px;font-weight:700;padding:3px 11px;border-radius:4px;margin:0 4px 6px 0;"><span leaf="">{{服务项}}</span></span>
  <span style="display:inline-block;background:#DBEAFE;color:#1E40AF;font-size:12px;font-weight:700;padding:3px 11px;border-radius:4px;margin:0 4px 6px 0;"><span leaf="">{{服务项}}</span></span>
</p>
```

---

## 组件 16 分隔线（蓝色渐变）

```html
<section style="padding:0 10px;margin-bottom:26px;">
  <section style="height:1px;background:linear-gradient(to right,transparent,#BFDBFE,#2563EB,#BFDBFE,transparent);margin:0;">
    <span leaf=""><br></span>
  </section>
</section>
```

---

## 组件 17 END 结尾分割线

```html
<section style="padding:0 10px;">
  <section style="text-align:center;margin:0 0 30px;">
    <section style="display:flex;align-items:center;justify-content:center;">
      <span style="height:2px;width:56px;background:linear-gradient(to right,transparent,#2563EB);margin-right:12px;"><span leaf=""><br></span></span>
      <span style="font-size:11px;color:#2563EB;letter-spacing:3px;font-weight:700;"><span leaf="">END</span></span>
      <span style="height:2px;width:56px;background:linear-gradient(to left,transparent,#2563EB);margin-left:12px;"><span leaf=""><br></span></span>
    </section>
  </section>
</section>
```

---

## 组件 18 尾部作者签名区

```html
<section style="padding:0 10px;">
  <p style="margin:0 0 2.5em;font-size:14px;line-height:2.5;text-align:justify;">
    <span leaf="">我是 {{作者名}}，{{一句话简介，如：专注广东公考公告解读}}。</span>
  </p>
  <p style="margin:0 0 2.5em;font-size:14px;line-height:2.5;text-align:justify;">
    <span leaf="">如果你觉得今天这篇有收获，欢迎</span>
    <strong style="color:#2563EB;"><span leaf="">点赞、在看、转发</span></strong>
    <span leaf="">三连，我们下篇见。</span>
  </p>
</section>
```

---

## 完整文章模板骨架

```html
<section style="max-width:677px;margin:0 auto;background:#ffffff;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;color:#1F2937;line-height:1.75;letter-spacing:2px;overflow-x:hidden;">

  <!-- 1. 顶部公告标签条（组件2，含广告合规声明） -->

  <!-- 2. 公告主标题卡（组件3，白底蓝色光晕） -->

  <!-- 3. 正文明白段（组件7 段落 × 1~2，放在主标题卡后） -->

  <!-- 4. 公告信息速览卡（组件4，本主题核心） -->
  <!-- 4a 双列信息格 → 4b 长信息实底块（仅1处）→ 4c 单列信息条 -->

  <!-- 5. 引流位（组件15a/15b：紧贴速览信息，读者需求最旺处） -->

  <!-- 6. 第一章（组件5 章节标题，margin-top:16px） -->
  <!--    章内：组件7 正文 + 6 子标题 + 8 行内高亮 + 9 引用提示 + 11 列表 + 12 数据 + 13 图片 -->

  <!-- 7. 章节分割线（组件16）+ 第二章…第N章（组件5，margin-top:44px） -->

  <!-- 8. 公告原文收纳容器（组件10，按需，可放在速览之后或文末） -->

  <!-- 9. 结语章（组件5 变体：编号 ∞，英文 THE END） -->

  <!-- 10. CTA 引导块（组件15c）+ 服务标签组（15d） -->

  <!-- 11. 分隔线（组件16） + END 分割线（组件17） + 签名区（组件18） -->

</section>
```

**骨架铁律**：主标题卡在最前；**速览卡必须在第一个章节之前**（这是本主题的核心价值）；引流不堆文末、至少一处前置；一篇只有一个 END + 一个签名区。

---

## 视觉层级（3 层递进）

| 层级 | 样式 | 用途 | 频率 |
|------|------|------|------|
| **锚点层** | 深蓝实底块（速览/CTA）/ 蓝色加粗 8a | 报名方式、关键条件、CTA | 全文 ≤5 处 |
| **标记层** | 淡蓝下划线 8c（默认）/ 浅蓝底标签 8b | 时间节点、数字、报名条件 | 每段 1~3 处 |
| **容器层** | 引用 9a-9c / 列表 11 / 数据 12 / 原文容器 10 | 结构化信息收纳 | 按需 |

**克制原则**：
- 深蓝实底块（`bg:#1D4ED8`）全文 ≤3 处（速览 1 处 + CTA 1 处为宜）
- 蓝色加粗全文 ≤5 处
- 渐变蓝仅出现在分隔线 16 和 END 线 17
- 四周虚线框仅用于「公告原文容器 10」与「待补素材占位 14」两处

---

## 文章类型 → 组件组合配方

| 文章类型 | 核心组件组合 | 点缀组件 |
|---|---|---|
| 招聘公告 | 速览卡 4 + 章节 5 + 编号要点 11a + 原文容器 10 | 时间线 11c、资料卡 15a、双资料卡 15b、CTA 15c |
| 考试通知 | 速览卡 4 + 时间线 11c + 提醒 9a + 原文容器 10 | 数据表 12c、CTA 15c |
| 政策解读 | 章节 5 + 正文 7 + 引用 9b + 旁注 9c | 数据卡 12a/12b、提示 9a |
| 报名提醒 | 速览卡 4 + 时间线 11c + 提示 9a | 服务标签 15d、CTA 15c |

所有类型共用固定结构：标签条 2 + 主标题卡 3 + 速览卡 4 + 编号章节 5 + END 17 + 签名 18。

---

## Markdown → 公告速读蓝 映射规则

| Markdown 元素 | 对应组件 | 说明 |
|---|---|---|
| `# 标题` | 不使用 | 公众号文章标题在平台设置 |
| 文章开头 `> 引言` | 组件 3 主标题卡导语 | 视角与外标题错开 |
| `## 章节标题` | 组件 5 章节标题 | 蓝色编号 01/02…，末章 ∞ + THE END |
| `### 子标题` | 组件 6 蓝色左竖条小标题 | 不套编号章节样式 |
| 普通段落 | 组件 7 正文段落 | 每段主动标 1~3 处淡蓝下划线 8c |
| `**加粗文字**` | 组件 8a 普通加粗（默认）/ 蓝色加粗（锚点 ≤5） | 普通加粗为主 |
| `==高亮文字==` | 组件 8b 浅蓝底深蓝字标签 | 核心概念 / 关键条件 |
| `<u>下划线</u>` / `++文字++` | 组件 8c 淡蓝下划线 | 次要强调 |
| 行内 `` `code` `` | 组件 8d 行内代码 | |
| `> 引用段落`（原文/条款） | 组件 9b 蓝色引用块 | |
| `> 引用段落`（旁注） | 组件 9c 灰色旁注块 | 轻量补充 |
| 招聘人数/时间/方式等关键信息 | **组件 4 速览卡** | 本主题核心，必须前置 |
| 报名流程 / 时间节点 | 组件 11c 时间线 | |
| 并列要点（短标题+说明） | 组件 11b 药丸要点列表 | |
| `1. 2. 3.` 编号列表 | 组件 11a 编号要点块 | 蓝色圆标 |
| 数据展示 | 组件 12a/12b 数据卡片组 | 蓝色大号数据 |
| Markdown 表格 | 组件 12c 数据表格 | 偶数行浅蓝底 |
| 公告全文 | 组件 10 原文收纳容器 | 浅底虚线框 |
| 配图建议 / 待补素材 | 组件 14 待补素材占位 | 居中板块 |
| `![](图片)` | 组件 13 图片容器 | 圆角卡片 + 说明 |
| 资料 / 课程推荐 | 组件 15a/15b 引流卡 | 前置，不堆文末 |
| 文末 | 组件 16 分隔线 + 17 END + 18 签名 | |
