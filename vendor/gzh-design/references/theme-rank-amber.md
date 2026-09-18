# 公众号排版组件库 —— 榜单数据橙

> **使用说明**：本组件库为「榜单数据橙」主题（数据榜单解读风），所有组件使用**内联样式**，可直接复制粘贴到微信公众号编辑器。
>
> **设计风格**：橙白干净 + 数据说话。以"榜单条目卡"和"数据表格"为主体，把枯燥的数字做成有排名的阵列；**高位数据用橙色徽章、低位数据用灰色徽章**，同一篇文章里"谁热谁冷"一眼可辨。另有高低对照双栏卡与中央结论金句，便于从数据推出判断。适合招录数据、竞争比分析、分数线汇总、排行榜单类文章。
>
> **公众号平台限制须知**：
> - ❌ 不支持 `<style>`/`<script>`、CSS class/id、`position:fixed/absolute`、`float`、`@media`/`@keyframes`、`display:grid`
> - ✅ 支持内联 `style`、`display:flex`（有限）、`linear-gradient`、`border-radius`、`box-shadow`、`<section>/<p>/<span>/<strong>/<img>` 等基础标签
>
> **WeChat 兼容铁律**（本主题组件全部已按此写好，改动时必须遵守）：
> - 所有"装饰性空元素"（渐变分割线、END 短线、排名徽章内的占位）**必须在内部放 `<span leaf=""><br></span>` 占位**
> - **不要把 `font-size`/`border-bottom` 打在 `<strong>` 上**，也不要在同一个 `<p>` 里混多个不同 `font-size`；高亮样式统一挂在外层 `<span>` 上
> - 不用 `position:absolute` 做划线/高亮
> - 正文字号严格用 `14px`、行高 `2.5`、段间距 `margin-bottom:2.5em`（见 SKILL.md「全局排版参数」）；卡片 / 列表 / 表格 / 引用块自身的 `margin` 是组件留白，不跟随修改
> - **榜单条目卡用 flex 布局**，条目名与数值分列两端；数值列加 `white-space:nowrap` 防止换行错位

---

## 设计变量速查表

```
主色调：       #EA580C（正橙）
主色调深：     #C2410C（深橙，实底块专用）
主色调中：     #F97316（中橙，第2名徽章）
主色调浅：     #FB923C（浅橙，第3名徽章）
主色调极浅：   #FED7AA（淡橙，标签底/下划线）
主色调背景：   #FFF7ED（极淡橙底）
强调字色：     #9A3412（深棕橙，浅底上的文字）
低位灰：       #9CA3AF（低位徽章）
低位灰浅：     #B4B2A9
低位字色：     #4B5563（低位数值字色）
标记色：       #FED7AA（下划线专用）
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

## 组件 2 顶部数据标签条

```html
<section style="padding:20px 10px 0;text-align:center;">
  <p style="margin:0;font-size:12px;color:#6B7280;letter-spacing:2px;">
    <span leaf="">{{栏目名}} · 招录分析</span>
  </p>
</section>
```

---

## 组件 3 数据头图卡（核心数字前置）

> 把最反直觉的那个数据结论直接放到开头。左侧大数字是主角（橙色），右侧灰数字做对比。

```html
<section style="margin:18px 10px 26px;background:#ffffff;border-radius:12px;box-shadow:0 6px 26px -6px rgba(234,88,12,0.18);padding:26px 22px 22px;overflow:hidden;">
  <p style="margin:0 0 6px;font-size:11px;color:#EA580C;font-weight:700;letter-spacing:3px;">
    <span leaf="">DATA REPORT</span>
  </p>
  <p style="margin:0 0 16px;font-size:19px;font-weight:900;color:#111827;line-height:1.5;">
    <span leaf="">{{标题：把最反直觉的那个数据结论放这里}}</span>
  </p>
  <section style="display:flex;align-items:flex-end;">
    <section style="margin-right:20px;">
      <p style="margin:0;font-size:32px;font-weight:900;color:#EA580C;line-height:1;"><span leaf="">{{核心数字}}</span></p>
      <p style="margin:6px 0 0;font-size:11px;color:#6B7280;"><span leaf="">{{指标说明}}</span></p>
    </section>
    <section style="padding-bottom:4px;">
      <p style="margin:0;font-size:26px;font-weight:900;color:#9CA3AF;line-height:1;"><span leaf="">{{对比数字}}</span></p>
      <p style="margin:6px 0 0;font-size:11px;color:#6B7280;"><span leaf="">{{对比说明}}</span></p>
    </section>
  </section>
</section>
```

---

## 组件 4 正文段落

> **关键规则**：每段主动识别 1~3 个关键短语（优先标关键数据），用**淡橙下划线**标记。

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
  <span style="border-bottom:2px solid #FED7AA;font-weight:600;"><span leaf="">{{关键数据}}</span></span>
  <span leaf="">{{后半句}}</span>
</p>
```

---

## 组件 5 章节标题（橙色实底编号 + 标题）

> 橙色实底编号标签 + 英文小标签 + 中文大标题，底部橙色实线。第一章 `margin-top:16px`，后续章节 `margin-top:44px`。

```html
<section style="margin-top:44px;margin-bottom:24px;padding:0 10px;">
  <section style="display:flex;align-items:center;margin-bottom:18px;padding-bottom:14px;border-bottom:2px solid #EA580C;">
    <span style="display:inline-block;background:#EA580C;color:#FFFFFF;font-size:16px;font-weight:900;padding:4px 13px;border-radius:6px;margin-right:12px;line-height:1.3;"><span leaf="">01</span></span>
    <section>
      <p style="font-size:11px;color:#EA580C;font-weight:700;letter-spacing:3px;margin:0 2px 2px;text-transform:uppercase;">
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
<span style="display:inline-block;background:#EA580C;color:#FFFFFF;font-size:16px;font-weight:900;padding:4px 13px;border-radius:6px;margin-right:12px;line-height:1.3;"><span leaf="">∞</span></span>
```

---

## 组件 6 子标题（橙色左竖条）

```html
<p style="margin:26px 0 14px;padding-left:10px;border-left:3px solid #EA580C;font-size:14px;font-weight:800;color:#111827;line-height:1.4;">
  <span leaf="">{{子标题，如：平均竞争比较高的部门}}</span>
</p>
```

---

## 组件 7 榜单条目卡（本主题核心组件）

> **本主题的招牌结构**。条目名与数值分列两端，左侧排名徽章。
>
> **配色规则（关键）**：
> - **高位榜**：第 1 名 `#EA580C` → 第 2 名 `#F97316` → 第 3 名 `#FB923C`（橙系递浅），数值用 `#C2410C`，卡底 `#FFF7ED` + 边框 `#FED7AA`
> - **低位榜**：徽章用灰色 `#9CA3AF` / `#B4B2A9`，数值用 `#4B5563`，卡底 `#F9FAFB` + 边框 `#E5E7EB`
>
> 两榜视觉反差强烈，读者扫一眼就知道哪边热、哪边冷。

### 7a. 高位榜单条目（橙色系）

```html
<section style="display:flex;align-items:center;background:#FFF7ED;border-radius:10px;padding:13px 16px;margin-bottom:10px;border:1px solid #FED7AA;">
  <span style="display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;background:#EA580C;color:#FFFFFF;font-size:13px;font-weight:900;border-radius:7px;flex-shrink:0;"><span leaf="">1</span></span>
  <section style="flex:1;margin-left:12px;min-width:0;">
    <p style="margin:0;font-size:13px;font-weight:700;color:#111827;line-height:1.6;"><span leaf="">{{条目名称}}</span></p>
    <p style="margin:2px 0 0;font-size:11px;color:#6B7280;line-height:1.6;"><span leaf="">{{条目说明（如岗位数）}}</span></p>
  </section>
  <p style="margin:0 0 0 10px;font-size:15px;font-weight:900;color:#C2410C;white-space:nowrap;"><span leaf="">{{数值}}</span></p>
</section>
```

第 2 名徽章底改 `#F97316`，第 3 名改 `#FB923C`。

### 7b. 低位榜单条目（灰色系）

```html
<section style="display:flex;align-items:center;background:#F9FAFB;border-radius:10px;padding:13px 16px;margin-bottom:10px;border:1px solid #E5E7EB;">
  <span style="display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;background:#9CA3AF;color:#FFFFFF;font-size:13px;font-weight:900;border-radius:7px;flex-shrink:0;"><span leaf="">1</span></span>
  <section style="flex:1;margin-left:12px;min-width:0;">
    <p style="margin:0;font-size:13px;font-weight:700;color:#111827;line-height:1.6;"><span leaf="">{{条目名称}}</span></p>
    <p style="margin:2px 0 0;font-size:11px;color:#6B7280;line-height:1.6;"><span leaf="">{{条目说明}}</span></p>
  </section>
  <p style="margin:0 0 0 10px;font-size:15px;font-weight:900;color:#4B5563;white-space:nowrap;"><span leaf="">{{数值}}</span></p>
</section>
```

---

## 组件 8 正文高亮样式

> **优先级**：① 淡橙下划线（正文默认标记）→ ② 普通加粗为主、橙色加粗仅锚点 → ③ 浅橙底深棕字标签（每篇 2~4 个）

### 8a. 加粗强调

普通加粗（默认）：

```html
<strong><span leaf="">普通加粗强调</span></strong>
```

橙色加粗（仅限核心数据/关键结论等锚点，全文 ≤5 处）：

```html
<strong style="color:#EA580C;"><span leaf="">橙色加粗锚点</span></strong>
```

### 8b. 浅橙底深棕字标签（核心概念，每篇 2~4 个）

```html
<span style="background:#FED7AA;color:#9A3412;padding:2px 7px;border-radius:3px;font-weight:700;"><span leaf="">概念标签</span></span>
```

### 8c. 淡橙下划线（最常用，本风格基础标记）

```html
<span style="border-bottom:2px solid #FED7AA;font-weight:600;"><span leaf="">淡橙下划线关键词</span></span>
```

### 8d. 行内代码

```html
<span style="background:#F3F4F6;color:#1F2937;padding:2px 6px;border-radius:4px;font-size:14px;font-weight:600;"><span leaf="">code</span></span>
```

---

## 组件 9 引用 / 提示 / 旁注块

### 9a. 橙色警示条（重点关注）

> 用于点出榜单里最值得警惕或最反常识的一条。

```html
<section style="background:#FFF7ED;border-left:4px solid #EA580C;border-radius:0 8px 8px 0;padding:14px 18px;margin-bottom:24px;">
  <p style="margin:0 0 6px;">
    <span style="display:inline-block;background:#EA580C;color:#FFFFFF;font-size:11px;font-weight:700;padding:2px 10px;border-radius:4px;letter-spacing:1px;"><span leaf="">重点关注</span></span>
  </p>
  <p style="margin:0;font-size:13px;color:#1F2937;line-height:2.2;">
    <span leaf="">{{内容}}</span>
  </p>
</section>
```

类型小标签文字可换：`重点关注` / `数据提示` / `注意`。

### 9b. 中央结论金句（从数据推出判断）

> **本主题的重要组件**：数据本身不会说话，用它把整组数据推出来的那句判断立起来。放在数据呈现之后。

```html
<section style="background:#FFF7ED;border-radius:0 10px 10px 0;border-left:4px solid #EA580C;padding:18px 20px;margin-bottom:24px;">
  <p style="margin:0;font-size:15px;font-weight:800;color:#9A3412;line-height:2.0;">
    <span leaf="">「{{核心结论：把整组数据推出来的那句判断放这里}}」</span>
  </p>
</section>
```

### 9c. 灰色旁注块（指标口径、数据来源）

```html
<section style="border-left:4px solid #D1D5DB;padding:13px 18px;margin-bottom:24px;background:#F9FAFB;border-radius:0 8px 8px 0;">
  <p style="margin:0;font-size:13px;color:#4B5563;line-height:2.2;text-align:justify;">
    <span leaf="">{{旁注内容：指标口径、数据来源等}}</span>
  </p>
</section>
```

---

## 组件 10 数据组件

### 10a. 三列数据卡（总览指标）

```html
<section style="display:flex;margin-bottom:26px;padding:0;">
  <section style="flex:1;background:#FFF7ED;border-radius:10px;padding:16px 8px;margin-right:8px;text-align:center;border:1px solid #FED7AA;">
    <p style="margin:0 0 4px;font-size:22px;font-weight:900;color:#C2410C;line-height:1;"><span leaf="">{{数字}}</span></p>
    <p style="margin:0;font-size:11px;color:#6B7280;"><span leaf="">{{说明}}</span></p>
  </section>
  <section style="flex:1;background:#FFF7ED;border-radius:10px;padding:16px 8px;margin-right:8px;text-align:center;border:1px solid #FED7AA;">
    <p style="margin:0 0 4px;font-size:22px;font-weight:900;color:#C2410C;line-height:1;"><span leaf="">{{数字}}</span></p>
    <p style="margin:0;font-size:11px;color:#6B7280;"><span leaf="">{{说明}}</span></p>
  </section>
  <section style="flex:1;background:#FFF7ED;border-radius:10px;padding:16px 8px;text-align:center;border:1px solid #FED7AA;">
    <p style="margin:0 0 4px;font-size:22px;font-weight:900;color:#C2410C;line-height:1;"><span leaf="">{{数字}}</span></p>
    <p style="margin:0;font-size:11px;color:#6B7280;"><span leaf="">{{说明}}</span></p>
  </section>
</section>
```

### 10b. 两列高低对照卡（高位 vs 低位）

> 与组件 7 榜单卡呼应：左边橙色（高位）、右边灰色（低位），把"门槛最高"和"最友好"并排呈现。

```html
<section style="display:flex;margin-bottom:24px;padding:0;">
  <section style="flex:1;background:#FFF7ED;border-radius:10px;padding:16px 14px;margin-right:10px;text-align:center;border:1px solid #FED7AA;">
    <p style="margin:0 0 4px;font-size:11px;color:#C2410C;font-weight:700;letter-spacing:1px;"><span leaf="">高位</span></p>
    <p style="margin:0 0 4px;font-size:24px;font-weight:900;color:#C2410C;line-height:1;"><span leaf="">{{数值}}</span></p>
    <p style="margin:0;font-size:11px;color:#6B7280;"><span leaf="">{{说明}}</span></p>
  </section>
  <section style="flex:1;background:#F9FAFB;border-radius:10px;padding:16px 14px;text-align:center;border:1px solid #E5E7EB;">
    <p style="margin:0 0 4px;font-size:11px;color:#6B7280;font-weight:700;letter-spacing:1px;"><span leaf="">低位</span></p>
    <p style="margin:0 0 4px;font-size:24px;font-weight:900;color:#4B5563;line-height:1;"><span leaf="">{{数值}}</span></p>
    <p style="margin:0;font-size:11px;color:#6B7280;"><span leaf="">{{说明}}</span></p>
  </section>
</section>
```

### 10c. 数据表格（带高亮行）

> **数值列用橙色加粗**突出关键数据，偶数行浅橙底；低位数据用灰色字色区分。

```html
<section style="margin-bottom:24px;overflow-x:auto;">
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <thead>
      <tr>
        <th style="background:#EA580C;color:#fff;font-weight:700;padding:9px 12px;text-align:left;"><span leaf="">{{列标题}}</span></th>
        <th style="background:#EA580C;color:#fff;font-weight:700;padding:9px 12px;text-align:center;"><span leaf="">{{列标题}}</span></th>
        <th style="background:#EA580C;color:#fff;font-weight:700;padding:9px 12px;text-align:center;"><span leaf="">{{列标题}}</span></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:9px 12px;border-bottom:1px solid #FED7AA;color:#1F2937;"><span leaf="">{{内容}}</span></td>
        <td style="padding:9px 12px;border-bottom:1px solid #FED7AA;color:#1F2937;text-align:center;"><span leaf="">{{内容}}</span></td>
        <td style="padding:9px 12px;border-bottom:1px solid #FED7AA;color:#C2410C;font-weight:700;text-align:center;"><span leaf="">{{数值}}</span></td>
      </tr>
      <tr>
        <td style="padding:9px 12px;border-bottom:1px solid #FED7AA;color:#1F2937;background:#FFF7ED;"><span leaf="">{{内容}}</span></td>
        <td style="padding:9px 12px;border-bottom:1px solid #FED7AA;color:#1F2937;background:#FFF7ED;text-align:center;"><span leaf="">{{内容}}</span></td>
        <td style="padding:9px 12px;border-bottom:1px solid #FED7AA;color:#C2410C;font-weight:700;background:#FFF7ED;text-align:center;"><span leaf="">{{数值}}</span></td>
      </tr>
    </tbody>
  </table>
</section>
```

---

## 组件 11 列表组件

### 11a. 编号要点块

```html
<section style="margin-bottom:24px;">
  <section style="display:flex;align-items:flex-start;margin-bottom:14px;">
    <span style="display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;background:#EA580C;color:#FFFFFF;font-size:12px;font-weight:700;border-radius:50%;flex-shrink:0;margin-top:3px;"><span leaf="">1</span></span>
    <p style="margin:0 0 0 12px;font-size:14px;line-height:2.2;flex:1;text-align:justify;">
      <strong><span leaf="">{{要点标题}}</span></strong>
      <span leaf="">，{{要点说明}}</span>
    </p>
  </section>
</section>
```

### 11b. 药丸要点列表

```html
<section style="margin-bottom:18px;">
  <p style="margin:0 0 8px;">
    <span style="display:inline-block;background:#FED7AA;color:#9A3412;font-size:13px;font-weight:700;padding:3px 12px;border-radius:999px;"><span leaf="">{{要点标题}}</span></span>
  </p>
  <p style="margin:0;font-size:13px;color:#4B5563;line-height:2.2;text-align:justify;">
    <span leaf="">{{要点说明}}</span>
  </p>
</section>
```

### 11c. 排名标签胶囊组（琥珀色阶）

> 用同一色系的深浅表现层级，适合做"梯队"标签（如第一梯队/第二梯队/第三梯队）。

```html
<p style="text-align:center;margin:0 0 24px;">
  <span style="display:inline-block;background:#EA580C;color:#FFFFFF;font-size:12px;font-weight:700;padding:4px 12px;border-radius:6px;margin:0 4px 6px 0;"><span leaf="">{{标签}}</span></span>
  <span style="display:inline-block;background:#FB923C;color:#FFFFFF;font-size:12px;font-weight:700;padding:4px 12px;border-radius:6px;margin:0 4px 6px 0;"><span leaf="">{{标签}}</span></span>
  <span style="display:inline-block;background:#FED7AA;color:#9A3412;font-size:12px;font-weight:700;padding:4px 12px;border-radius:6px;margin:0 4px 6px 0;"><span leaf="">{{标签}}</span></span>
</p>
```

---

## 组件 12 图片容器

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

## 组件 13 待补素材占位（居中板块）

```html
<section style="margin:0 0 24px;padding:28px 20px;border:1.5px dashed #DAD7D2;border-radius:14px;background:#FAFAF8;text-align:center;">
  <p style="margin:0 0 10px;font-size:24px;line-height:1;"><span leaf="">📊</span></p>
  <p style="margin:0;font-size:13px;font-weight:700;color:#9CA3AF;letter-spacing:2px;"><span leaf="">待补素材</span></p>
  <p style="margin:8px 0 0;font-size:12px;color:#B8B5B0;line-height:1.8;"><span leaf="">此处插入：{{素材说明，如数据速览表 / 系统图标}}</span></p>
</section>
```

---

## 组件 14 资料推荐卡（数据查询类）

```html
<section style="background:#FFF7ED;border-radius:12px;padding:18px;margin-bottom:16px;border:1px solid #FED7AA;">
  <p style="margin:0 0 10px;font-size:12px;color:#C2410C;font-weight:700;letter-spacing:2px;"><span leaf="">📚 资料推荐</span></p>
  <p style="margin:0 0 10px;font-size:14px;font-weight:800;color:#111827;line-height:1.7;"><span leaf="">{{资料名称}}</span></p>
  <p style="margin:0 0 10px;font-size:13px;color:#4B5563;line-height:2.0;"><span leaf="">{{资料说明，讲清楚能查到什么数据}}</span></p>
  <p style="margin:0;">
    <span style="display:inline-block;background:#EA580C;color:#FFFFFF;font-size:13px;font-weight:700;padding:8px 22px;border-radius:8px;"><span leaf="">{{查询入口}}</span></span>
  </p>
</section>
```

---

## 组件 15 CTA 引导块（深橙实底）

```html
<section style="background:#C2410C;border-radius:12px;padding:20px;margin-bottom:24px;">
  <p style="margin:0 0 8px;font-size:15px;font-weight:800;color:#FFFFFF;line-height:1.7;">
    <span leaf="">{{引导文案：说明回复关键词能查到什么}}</span>
  </p>
  <p style="margin:0;font-size:13px;color:#FED7AA;line-height:1.9;">
    <span leaf="">{{补充说明}}</span>
  </p>
</section>
```

---

## 组件 16 服务标签胶囊组

```html
<p style="text-align:center;margin:0 0 24px;">
  <span style="display:inline-block;background:#FED7AA;color:#9A3412;font-size:12px;font-weight:700;padding:3px 11px;border-radius:4px;margin:0 4px 6px 0;"><span leaf="">{{服务项}}</span></span>
  <span style="display:inline-block;background:#FED7AA;color:#9A3412;font-size:12px;font-weight:700;padding:3px 11px;border-radius:4px;margin:0 4px 6px 0;"><span leaf="">{{服务项}}</span></span>
</p>
```

---

## 组件 17 分隔线（橙色渐变）

```html
<section style="padding:0 10px;margin-bottom:26px;">
  <section style="height:1px;background:linear-gradient(to right,transparent,#FED7AA,#EA580C,#FED7AA,transparent);margin:0;">
    <span leaf=""><br></span>
  </section>
</section>
```

---

## 组件 18 END 结尾分割线

```html
<section style="padding:0 10px;">
  <section style="text-align:center;margin:0 0 30px;">
    <section style="display:flex;align-items:center;justify-content:center;">
      <span style="height:2px;width:56px;background:linear-gradient(to right,transparent,#EA580C);margin-right:12px;"><span leaf=""><br></span></span>
      <span style="font-size:11px;color:#EA580C;letter-spacing:3px;font-weight:700;"><span leaf="">END</span></span>
      <span style="height:2px;width:56px;background:linear-gradient(to left,transparent,#EA580C);margin-left:12px;"><span leaf=""><br></span></span>
    </section>
  </section>
</section>
```

---

## 组件 19 尾部作者签名区

```html
<section style="padding:0 10px;">
  <p style="margin:0 0 2.5em;font-size:14px;line-height:2.5;text-align:justify;">
    <span leaf="">我是 {{作者名}}，{{一句话简介，如：用数据帮你看清考情}}。</span>
  </p>
  <p style="margin:0 0 2.5em;font-size:14px;line-height:2.5;text-align:justify;">
    <span leaf="">如果你觉得今天这篇有收获，欢迎</span>
    <strong style="color:#EA580C;"><span leaf="">点赞、在看、转发</span></strong>
    <span leaf="">三连，我们下篇见。</span>
  </p>
</section>
```

---

## 完整文章模板骨架

```html
<section style="max-width:677px;margin:0 auto;background:#ffffff;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;color:#1F2937;line-height:1.75;letter-spacing:2px;overflow-x:hidden;">

  <!-- 1. 顶部数据标签条（组件2） -->

  <!-- 2. 数据头图卡（组件3，核心数字前置） -->

  <!-- 3. 开篇段落（组件4 正文 × 1~2，抛出数据里最反直觉的地方） -->

  <!-- 4. 总览数据卡（组件10a 三列，把大盘指标先给到） -->

  <!-- 5. 第一章（组件5 章节标题，margin-top:16px） -->
  <!--    章内：组件6 子标题（高位榜 / 低位榜）+ 组件7 榜单条目卡 × N -->
  <!--          + 组件9a 警示条 + 组件4 正文 -->

  <!-- 6. 章节分割线（组件17）+ 第二章…第N章（组件5，margin-top:44px） -->
  <!--    数据表格（组件10c）+ 旁注（组件9c 讲口径）+ 中央结论金句（组件9b） -->

  <!-- 7. 结语章（组件5 变体：编号 ∞，英文 THE END） -->

  <!-- 8. 资料推荐卡（组件14）+ CTA 引导块（组件15）+ 服务标签（组件16） -->

  <!-- 9. 分隔线（组件17） + END 分割线（组件18） + 签名区（组件19） -->

</section>
```

**骨架铁律**：数据头图卡在最前（核心数字前置）；**高位榜与低位榜必须分列**（这是本主题的核心对比手法）；每章数据呈现后接中央结论金句 9b，把数据变成判断；一篇只有一个 END + 一个签名区。

---

## 视觉层级（3 层递进）

| 层级 | 样式 | 用途 | 频率 |
|------|------|------|------|
| **锚点层** | 数据头图大数字 / 深橙实底块（CTA）/ 橙色加粗 8a / 结论金句 9b | 核心数据、判断、CTA | 全文 ≤5 处 |
| **标记层** | 淡橙下划线 8c（默认）/ 浅橙底标签 8b | 关键数据、概念 | 每段 1~3 处 |
| **容器层** | 榜单卡 7 / 数据卡 10 / 警示 9a / 旁注 9c / 列表 11 | 数据阵列与结构化信息 | 按需 |

**克制原则**：
- 深橙实底块（`bg:#C2410C`）全文 ≤2 处
- 橙色加粗全文 ≤5 处
- **高低位配色不可混用**：高位榜只能橙系（`#EA580C`/`#F97316`/`#FB923C`），低位榜只能灰系（`#9CA3AF`/`#B4B2A9`）——这是本主题的核心视觉语言
- 榜单卡的数值列务必加 `white-space:nowrap`，否则数字换行会破坏对齐

---

## 文章类型 → 组件组合配方

| 文章类型 | 核心组件组合 | 点缀组件 |
|---|---|---|
| 招录数据 | 数据头图 3 + 章节 5 + 三列数据卡 10a + 数据表 10c | 榜单卡 7、旁注 9c、资料卡 14 |
| 竞争比分析 | 章节 5 + 榜单卡 7（高位/低位分列）+ 结论金句 9b | 警示条 9a、两列对照 10b |
| 分数线汇总 | 章节 5 + 数据表 10c + 两列对照 10b | 结论金句 9b、梯队标签 11c |
| 排行榜单 | 数据头图 3 + 榜单卡 7 × N + 梯队标签 11c | 结论金句 9b、资料卡 14 |

所有类型共用固定结构：标签条 2 + 数据头图卡 3 + 表格/榜单 + 中央结论金句 9b + END 18 + 签名 19。

---

## Markdown → 榜单数据橙 映射规则

| Markdown 元素 | 对应组件 | 说明 |
|---|---|---|
| `# 标题` | 不使用 | 公众号文章标题在平台设置 |
| 文章开头 `> 引言` | 组件 3 数据头图卡标题 | 把核心数据结论前置 |
| `## 章节标题` | 组件 5 章节标题 | 橙色编号 01/02…，末章 ∞ + THE END |
| `### 子标题` | 组件 6 橙色左竖条小标题 | 如"平均竞争比较高的部门" |
| 普通段落 | 组件 4 正文段落 | 每段主动标 1~3 处淡橙下划线 8c |
| `**加粗文字**` | 组件 8a 普通加粗（默认）/ 橙色加粗（锚点 ≤5） | 普通加粗为主 |
| `==高亮文字==` | 组件 8b 浅橙底深棕字标签 | 核心概念 |
| `<u>下划线</u>` / `++文字++` | 组件 8c 淡橙下划线 | 次要强调 |
| 行内 `` `code` `` | 组件 8d 行内代码 | |
| `> 引用段落`（结论） | 组件 9b 中央结论金句 | 数据 → 判断 |
| `> 引用段落`（旁注） | 组件 9c 灰色旁注块 | 口径解释 |
| **排名数据（部门/岗位/竞争比）** | **组件 7 榜单条目卡** | 本主题核心，高位/低位配色分列 |
| 大盘指标 | 组件 10a 三列数据卡 | |
| 高低对比 | 组件 10b 两列对照卡 | 橙 vs 灰 |
| 梯队/分层标签 | 组件 11c 排名标签胶囊组 | 琥珀色阶 |
| 并列要点（短标题+说明） | 组件 11b 药丸要点列表 | |
| `1. 2. 3.` 编号列表 | 组件 11a 编号要点块 | 橙色圆标 |
| Markdown 表格 | 组件 10c 数据表格 | 数值列橙字加粗、偶数行浅橙底 |
| 数据查询类推荐 | 组件 14 资料推荐卡 | |
| 待补素材 / 配图建议 | 组件 13 待补素材占位 | 居中板块 |
| `![](图片)` | 组件 12 图片容器 | 圆角卡片 + 说明 |
| 文末 | 组件 17 分隔线 + 18 END + 19 签名 | |
