# 公众号排版组件库 —— 考点科普绿

> **使用说明**：本组件库为「考点科普绿」主题（备考科普干货风），所有组件使用**内联样式**，可直接复制粘贴到微信公众号编辑器。
>
> **设计风格**：绿白干净 + 结论先行。以"编号要点块"为骨架，把 N 个知识点逐条拆开讲透；每条要点内部先给结论卡再展开解释，读者扫一眼就能拿到答案。**引流卡内嵌在要点之间**——读者正处在那个需求点上，转化效率高于文末集中轰炸。适合考情科普、备考攻略、常见问题解答、知识梳理类文章。
>
> **公众号平台限制须知**：
> - ❌ 不支持 `<style>`/`<script>`、CSS class/id、`position:fixed/absolute`、`float`、`@media`/`@keyframes`、`display:grid`
> - ✅ 支持内联 `style`、`display:flex`（有限）、`linear-gradient`、`border-radius`、`box-shadow`、`<section>/<p>/<span>/<strong>/<img>` 等基础标签
>
> **WeChat 兼容铁律**（本主题组件全部已按此写好，改动时必须遵守）：
> - 所有"装饰性空元素"（渐变分割线、END 短线、清单方框）**必须在内部放 `<span leaf=""><br></span>` 占位**
> - **不要把 `font-size`/`border-bottom` 打在 `<strong>` 上**，也不要在同一个 `<p>` 里混多个不同 `font-size`；高亮样式统一挂在外层 `<span>` 上
> - 不用 `position:absolute` 做划线/高亮
> - 正文字号严格用 `14px`、行高 `2.5`、段间距 `margin-bottom:2.5em`（见 SKILL.md「全局排版参数」）；卡片 / 列表 / 表格 / 引用块自身的 `margin` 是组件留白，不跟随修改

---

## 设计变量速查表

```
主色调：       #059669（正绿）
主色调深：     #047857（深绿，实底块专用）
主色调浅：     #A7F3D0（浅绿，结构线/下划线）
主色调极浅：   #D1FAE5（淡绿，标签底）
主色调背景：   #F0FDF4（极淡绿底）
结论卡背景：   #ECFDF5（嫩绿底）
引流卡背景：   #FFFBEB（暖黄底，与主色形成对比）
引流卡边框：   #FDE68A
引流卡字色：   #92400E（深棕，强调"这是推荐"）
标记色：       #A7F3D0（下划线专用）
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

## 组件 2 顶部栏目条

```html
<section style="padding:20px 10px 0;text-align:center;">
  <p style="margin:0;font-size:12px;color:#6B7280;letter-spacing:2px;">
    <span leaf="">{{栏目名}} · 考情科普</span>
  </p>
</section>
```

---

## 组件 3 引言卡（浅绿底 + 导语药丸）

> **文案策略**：导语金句和公众号外标题是**两层**，视角要错开——外标题卖"为什么点开"，导语卡直接给判断。

```html
<section style="margin:18px 10px 26px;background:#F0FDF4;border-radius:12px;padding:24px 22px;border:1px solid #D1FAE5;overflow:hidden;">
  <p style="margin:0 0 12px;">
    <span style="display:inline-block;background:#059669;color:#FFFFFF;font-size:11px;font-weight:700;padding:3px 12px;border-radius:999px;letter-spacing:2px;"><span leaf="">导语</span></span>
  </p>
  <p style="margin:0;font-size:15px;font-weight:800;color:#065F46;line-height:2.0;">
    <span leaf="">{{导语金句：把本篇要解决的核心疑问，用一句有判断力的话讲清楚}}</span>
  </p>
</section>
```

---

## 组件 4 正文段落

> **关键规则**：每段主动识别 1~3 个关键短语，用**淡绿下划线**标记。

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
  <span style="border-bottom:2px solid #A7F3D0;font-weight:600;"><span leaf="">{{需要强调的关键短语}}</span></span>
  <span leaf="">{{后半句}}</span>
</p>
```

---

## 组件 5 序号药丸要点标题（本主题骨架）

> **这是本主题的核心结构**。每个要点用「绿色实底序号 + 要点标题」，紧接一段说明。要点编号按出现顺序 01/02/03…

```html
<p style="margin:30px 0 14px;font-size:15px;font-weight:800;color:#111827;line-height:1.6;">
  <span style="display:inline-block;background:#059669;color:#FFFFFF;font-size:13px;font-weight:900;border-radius:6px;padding:3px 11px;margin-right:9px;"><span leaf="">01</span></span>
  <span leaf="">{{要点标题}}</span>
</p>
<p style="margin:0 0 2.5em;font-size:14px;line-height:2.5;text-align:justify;">
  <span leaf="">{{要点说明。先给结论，再展开解释}}</span>
</p>
```

---

## 组件 6 结论卡（结论先行）

> 放在要点说明之后，把这条要点的答案"说死"。**每个要点最多一张**，不要每个段落都放。

```html
<section style="background:#ECFDF5;border-radius:10px;padding:15px 18px;margin-bottom:2.5em;border-left:4px solid #059669;">
  <p style="margin:0 0 6px;font-size:11px;color:#047857;font-weight:700;letter-spacing:2px;"><span leaf="">结论</span></p>
  <p style="margin:0;font-size:14px;font-weight:700;color:#065F46;line-height:2.2;">
    <span leaf="">{{结论：一句话把这条要点的答案说死}}</span>
  </p>
</section>
```

---

## 组件 7 嵌入式引流卡（本主题特色）

> **位置原则（重要）**：引流卡**不堆文末**，而是嵌在要点之间——讲完某个知识点、读者正在那个需求点上时顺势推出。一篇放 1~3 处，每处对应前一个要点的需求。
>
> 用暖黄底与绿色主色形成对比，视觉上"跳出来"但不像硬广。**价格和领取方式写清楚**。

```html
<section style="background:#FFFBEB;border-radius:10px;padding:15px 18px;margin-bottom:2.5em;border:1px solid #FDE68A;">
  <p style="margin:0 0 8px;font-size:13px;font-weight:800;color:#92400E;line-height:1.7;">
    <span leaf="">📘 {{资料名称}}</span>
  </p>
  <p style="margin:0 0 10px;font-size:12px;color:#78350F;line-height:2.0;">
    <span leaf="">{{资料说明，紧贴当前要点讲的需求}}</span>
  </p>
  <p style="margin:0;">
    <span style="display:inline-block;background:#F59E0B;color:#FFFFFF;font-size:12px;font-weight:700;padding:6px 18px;border-radius:6px;"><span leaf="">{{价格 + 领取方式}}</span></span>
  </p>
</section>
```

---

## 组件 8 正文高亮样式

> **优先级**：① 淡绿下划线（正文默认标记）→ ② 普通加粗为主、绿色加粗仅锚点 → ③ 浅绿底深绿字标签（每篇 2~4 个）

### 8a. 加粗强调

普通加粗（默认）：

```html
<strong><span leaf="">普通加粗强调</span></strong>
```

绿色加粗（仅限核心结论/关键数据等锚点，全文 ≤5 处）：

```html
<strong style="color:#059669;"><span leaf="">绿色加粗锚点</span></strong>
```

### 8b. 浅绿底深绿字标签（核心概念，每篇 2~4 个）

```html
<span style="background:#D1FAE5;color:#065F46;padding:2px 7px;border-radius:3px;font-weight:700;"><span leaf="">概念标签</span></span>
```

### 8c. 淡绿下划线（最常用，本风格基础标记）

```html
<span style="border-bottom:2px solid #A7F3D0;font-weight:600;"><span leaf="">淡绿下划线关键词</span></span>
```

### 8d. 行内代码

```html
<span style="background:#F3F4F6;color:#1F2937;padding:2px 6px;border-radius:4px;font-size:14px;font-weight:600;"><span leaf="">code</span></span>
```

---

## 组件 9 引用 / 提示 / 旁注块

### 9a. 绿色提示条（易错点 / 必须记住的规则）

```html
<section style="background:#ECFDF5;border-left:4px solid #059669;border-radius:0 8px 8px 0;padding:14px 18px;margin-bottom:24px;">
  <p style="margin:0 0 6px;">
    <span style="display:inline-block;background:#059669;color:#FFFFFF;font-size:11px;font-weight:700;padding:2px 10px;border-radius:4px;letter-spacing:1px;"><span leaf="">注意</span></span>
  </p>
  <p style="margin:0;font-size:13px;color:#1F2937;line-height:2.2;">
    <span leaf="">{{提示内容}}</span>
  </p>
</section>
```

类型小标签文字可换：`注意` / `重点` / `易错` / `划重点`。

### 9b. 灰色旁注块（口径解释、延伸说明）

```html
<section style="border-left:4px solid #D1D5DB;padding:13px 18px;margin-bottom:24px;background:#F9FAFB;border-radius:0 8px 8px 0;">
  <p style="margin:0;font-size:13px;color:#4B5563;line-height:2.2;text-align:justify;">
    <span leaf="">{{旁注内容}}</span>
  </p>
</section>
```

---

## 组件 10 双栏对照卡（A/B 对比）

> 用于"国考 vs 省考""面授 vs 网课"这类二选一对比。A 栏用主题绿突出、B 栏用中性灰收敛。

```html
<section style="display:flex;margin-bottom:2.5em;">
  <section style="flex:1;background:#ECFDF5;border-radius:10px;padding:15px 14px;margin-right:10px;border:1px solid #D1FAE5;">
    <p style="margin:0 0 6px;font-size:12px;color:#047857;font-weight:700;letter-spacing:1px;"><span leaf="">{{对比项 A}}</span></p>
    <p style="margin:0;font-size:13px;color:#1F2937;line-height:2.1;"><span leaf="">{{内容}}</span></p>
  </section>
  <section style="flex:1;background:#F9FAFB;border-radius:10px;padding:15px 14px;border:1px solid #E5E7EB;">
    <p style="margin:0 0 6px;font-size:12px;color:#6B7280;font-weight:700;letter-spacing:1px;"><span leaf="">{{对比项 B}}</span></p>
    <p style="margin:0;font-size:13px;color:#1F2937;line-height:2.1;"><span leaf="">{{内容}}</span></p>
  </section>
</section>
```

---

## 组件 11 数据组件

### 11a. 数据对比行（前后对比 / 高低对比）

```html
<section style="background:#F9FAFB;border-radius:10px;padding:16px 18px;margin-bottom:24px;">
  <section style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
    <p style="margin:0;font-size:13px;color:#4B5563;flex:1;"><span leaf="">{{对比项}}</span></p>
    <p style="margin:0;font-size:15px;font-weight:900;color:#047857;"><span leaf="">{{数值}}</span></p>
  </section>
  <section style="display:flex;align-items:center;justify-content:space-between;">
    <p style="margin:0;font-size:13px;color:#4B5563;flex:1;"><span leaf="">{{对比项}}</span></p>
    <p style="margin:0;font-size:15px;font-weight:900;color:#6B7280;"><span leaf="">{{数值}}</span></p>
  </section>
</section>
```

### 11b. 三列数据卡

```html
<section style="display:flex;margin-bottom:24px;padding:0;">
  <section style="flex:1;background:#F0FDF4;border-radius:10px;padding:16px 8px;margin-right:8px;text-align:center;border:1px solid #D1FAE5;">
    <p style="margin:0 0 4px;font-size:20px;font-weight:900;color:#047857;line-height:1;"><span leaf="">{{数字}}</span></p>
    <p style="margin:0;font-size:11px;color:#6B7280;"><span leaf="">{{说明}}</span></p>
  </section>
  <section style="flex:1;background:#F0FDF4;border-radius:10px;padding:16px 8px;margin-right:8px;text-align:center;border:1px solid #D1FAE5;">
    <p style="margin:0 0 4px;font-size:20px;font-weight:900;color:#047857;line-height:1;"><span leaf="">{{数字}}</span></p>
    <p style="margin:0;font-size:11px;color:#6B7280;"><span leaf="">{{说明}}</span></p>
  </section>
  <section style="flex:1;background:#F0FDF4;border-radius:10px;padding:16px 8px;text-align:center;border:1px solid #D1FAE5;">
    <p style="margin:0 0 4px;font-size:20px;font-weight:900;color:#047857;line-height:1;"><span leaf="">{{数字}}</span></p>
    <p style="margin:0;font-size:11px;color:#6B7280;"><span leaf="">{{说明}}</span></p>
  </section>
</section>
```

### 11c. 数据表格

```html
<section style="margin-bottom:24px;overflow-x:auto;">
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <thead>
      <tr>
        <th style="background:#059669;color:#fff;font-weight:700;padding:9px 12px;text-align:left;"><span leaf="">{{列标题}}</span></th>
        <th style="background:#059669;color:#fff;font-weight:700;padding:9px 12px;text-align:center;"><span leaf="">{{列标题}}</span></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:9px 12px;border-bottom:1px solid #D1FAE5;color:#1F2937;"><span leaf="">{{内容}}</span></td>
        <td style="padding:9px 12px;border-bottom:1px solid #D1FAE5;color:#1F2937;text-align:center;"><span leaf="">{{内容}}</span></td>
      </tr>
      <tr>
        <td style="padding:9px 12px;border-bottom:1px solid #D1FAE5;color:#1F2937;background:#F0FDF4;"><span leaf="">{{内容}}</span></td>
        <td style="padding:9px 12px;border-bottom:1px solid #D1FAE5;color:#1F2937;background:#F0FDF4;text-align:center;"><span leaf="">{{内容}}</span></td>
      </tr>
    </tbody>
  </table>
</section>
```

---

## 组件 12 列表组件

### 12a. 自查清单（方框勾选）

```html
<section style="background:#F9FAFB;border-radius:10px;padding:16px 18px;margin-bottom:24px;border:1px solid #E5E7EB;">
  <p style="margin:0 0 12px;font-size:12px;color:#6B7280;letter-spacing:2px;"><span leaf="">✅ 自查清单</span></p>
  <section style="display:flex;align-items:flex-start;margin-bottom:10px;">
    <span style="display:inline-block;width:16px;height:16px;border:2px solid #059669;border-radius:3px;flex-shrink:0;margin-top:4px;"><span leaf=""><br></span></span>
    <p style="margin:0 0 0 10px;font-size:13px;color:#4B5563;line-height:2.0;flex:1;"><span leaf="">{{清单项}}</span></p>
  </section>
</section>
```

最后一项去掉 `margin-bottom`。

### 12b. 药丸要点列表

```html
<section style="margin-bottom:18px;">
  <p style="margin:0 0 8px;">
    <span style="display:inline-block;background:#D1FAE5;color:#065F46;font-size:13px;font-weight:700;padding:3px 12px;border-radius:999px;"><span leaf="">{{要点标题}}</span></span>
  </p>
  <p style="margin:0;font-size:13px;color:#4B5563;line-height:2.2;text-align:justify;">
    <span leaf="">{{要点说明}}</span>
  </p>
</section>
```

---

## 组件 13 居中金句（收尾过渡）

```html
<p style="font-size:14px;margin:0 0 2.5em;text-align:center;color:#047857;font-weight:700;letter-spacing:2px;border-top:1px solid #D1FAE5;border-bottom:1px solid #D1FAE5;padding:16px 10px;line-height:2.0;">
  <span leaf="">{{居中金句}}</span>
</p>
```

---

## 组件 14 图片容器

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

## 组件 15 待补素材占位（居中板块）

```html
<section style="margin:0 0 24px;padding:28px 20px;border:1.5px dashed #DAD7D2;border-radius:14px;background:#FAFAF8;text-align:center;">
  <p style="margin:0 0 10px;font-size:24px;line-height:1;"><span leaf="">📊</span></p>
  <p style="margin:0;font-size:13px;font-weight:700;color:#9CA3AF;letter-spacing:2px;"><span leaf="">待补素材</span></p>
  <p style="margin:8px 0 0;font-size:12px;color:#B8B5B0;line-height:1.8;"><span leaf="">此处插入：{{素材说明}}</span></p>
</section>
```

---

## 组件 16 课程引流卡（文末版）

> 与组件 7 嵌入式引流卡的区别：组件 7 嵌在要点之间（暖黄底），本组件放在文末作为收束（绿色系，与主题一致）。

```html
<section style="background:#F0FDF4;border-radius:12px;padding:18px;margin-bottom:16px;border:1px solid #A7F3D0;">
  <p style="margin:0 0 10px;font-size:12px;color:#047857;font-weight:700;letter-spacing:2px;"><span leaf="">📚 课程推荐</span></p>
  <p style="margin:0 0 10px;font-size:14px;font-weight:800;color:#111827;line-height:1.7;"><span leaf="">{{课程名称}}</span></p>
  <p style="margin:0 0 10px;font-size:13px;color:#4B5563;line-height:2.0;"><span leaf="">{{课程说明，讲清楚适合谁、能解决什么问题}}</span></p>
  <p style="margin:0;">
    <span style="display:inline-block;background:#059669;color:#FFFFFF;font-size:13px;font-weight:700;padding:8px 22px;border-radius:8px;"><span leaf="">{{行动引导}}</span></span>
  </p>
</section>
```

---

## 组件 17 CTA 引导块（深绿实底）

```html
<section style="background:#047857;border-radius:12px;padding:20px;margin-bottom:24px;">
  <p style="margin:0 0 8px;font-size:15px;font-weight:800;color:#FFFFFF;line-height:1.7;">
    <span leaf="">{{引导文案：说明回复什么关键词能拿到什么}}</span>
  </p>
  <p style="margin:0;font-size:13px;color:#A7F3D0;line-height:1.9;">
    <span leaf="">{{补充说明}}</span>
  </p>
</section>
```

---

## 组件 18 分隔线（绿色渐变）

```html
<section style="padding:0 10px;margin-bottom:26px;">
  <section style="height:1px;background:linear-gradient(to right,transparent,#A7F3D0,#059669,#A7F3D0,transparent);margin:0;">
    <span leaf=""><br></span>
  </section>
</section>
```

---

## 组件 19 END 结尾分割线

```html
<section style="padding:0 10px;">
  <section style="text-align:center;margin:0 0 30px;">
    <section style="display:flex;align-items:center;justify-content:center;">
      <span style="height:2px;width:56px;background:linear-gradient(to right,transparent,#059669);margin-right:12px;"><span leaf=""><br></span></span>
      <span style="font-size:11px;color:#059669;letter-spacing:3px;font-weight:700;"><span leaf="">END</span></span>
      <span style="height:2px;width:56px;background:linear-gradient(to left,transparent,#059669);margin-left:12px;"><span leaf=""><br></span></span>
    </section>
  </section>
</section>
```

---

## 组件 20 尾部作者签名区

```html
<section style="padding:0 10px;">
  <p style="margin:0 0 2.5em;font-size:14px;line-height:2.5;text-align:justify;">
    <span leaf="">我是 {{作者名}}，{{一句话简介，如：陪你备考的同行者}}。</span>
  </p>
  <p style="margin:0 0 2.5em;font-size:14px;line-height:2.5;text-align:justify;">
    <span leaf="">如果你觉得今天这篇有收获，欢迎</span>
    <strong style="color:#059669;"><span leaf="">点赞、在看、转发</span></strong>
    <span leaf="">三连，我们下篇见。</span>
  </p>
</section>
```

---

## 完整文章模板骨架

```html
<section style="max-width:677px;margin:0 auto;background:#ffffff;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;color:#1F2937;line-height:1.75;letter-spacing:2px;overflow-x:hidden;">

  <!-- 1. 顶部栏目条（组件2） -->

  <!-- 2. 引言卡（组件3，浅绿底 + 导语药丸） -->

  <!-- 3. 开篇段落（组件4 正文 × 1~2，交代痛点、引出框架） -->

  <!-- 4. 要点 01（组件5 序号药丸要点标题 + 组件4 说明段落） -->
  <!--    → 组件6 结论卡（结论先行，每个要点最多一张） -->

  <!-- 5. 嵌入式引流卡（组件7，嵌在要点之间，1~3 处） -->

  <!-- 6. 要点 02 → … → 要点 N（重复 4、5 的节奏） -->
  <!--    章内可穿插：组件8 行内高亮 + 组件9 引用提示 + 组件10 双栏对照 + 组件11 数据 + 组件12 列表 -->

  <!-- 7. 居中金句（组件13，收束全文） -->

  <!-- 8. 文末课程引流卡（组件16）+ CTA 引导块（组件17） -->

  <!-- 9. 分隔线（组件18） + END 分割线（组件19） + 签名区（组件20） -->

</section>
```

**骨架铁律**：引言卡在最前；**引流卡必须内嵌在要点之间**（本主题核心手法，不要全堆文末）；一篇只有一个 END + 一个签名区；编号要点严格按出现顺序 01/02/03…

---

## 视觉层级（3 层递进）

| 层级 | 样式 | 用途 | 频率 |
|------|------|------|------|
| **锚点层** | 深绿实底块（CTA）/ 绿色加粗 8a / 结论卡 6 | 核心结论、CTA | 全文 ≤5 处 |
| **标记层** | 淡绿下划线 8c（默认）/ 浅绿底标签 8b | 概念、关键数据 | 每段 1~3 处 |
| **容器层** | 结论卡 6 / 引流卡 7 / 引用提示 9 / 对照 10 / 数据 11 / 列表 12 | 结构化信息 | 按需 |

**克制原则**：
- 深绿实底块（`bg:#047857`）全文 ≤2 处
- 绿色加粗全文 ≤5 处
- **结论卡每个要点最多一张**，不要每段都放（会失去"结论"的强调作用）
- 引流卡的暖黄底是全篇唯一的非绿色系，正是靠这个反差抓注意力，**不要给其它组件也用暖黄**

---

## 文章类型 → 组件组合配方

| 文章类型 | 核心组件组合 | 点缀组件 |
|---|---|---|
| 考情科普 | 序号药丸 5 + 正文 4 + 结论卡 6 | 嵌入式引流 7、数据表 11c、提示 9a |
| 备考攻略 | 序号药丸 5 + 正文 4 + 自查清单 12a | 药丸列表 12b、居中金句 13 |
| 常见问题解答 | 序号药丸 5 + 结论卡 6（逐条给答案） | 双栏对照 10、旁注 9b |
| 知识梳理 | 序号药丸 5 + 正文 4 + 数据卡 11b | 数据对比行 11a、双栏对照 10 |

所有类型共用固定结构：栏目条 2 + 引言卡 3 + 序号要点 5 + 居中金句 13 + END 19 + 签名 20。

---

## Markdown → 考点科普绿 映射规则

| Markdown 元素 | 对应组件 | 说明 |
|---|---|---|
| `# 标题` | 不使用 | 公众号文章标题在平台设置 |
| 文章开头 `> 引言金句` | 组件 3 引言卡 | 视角与外标题错开 |
| `## 章节标题` | 组件 5 序号药丸要点标题 | 编号 01/02/03… |
| `### 子标题` | 组件 5 序号药丸（降一级） | 无编号版：去掉序号药丸只留标题 |
| 普通段落 | 组件 4 正文段落 | 每段主动标 1~3 处淡绿下划线 8c |
| `**加粗文字**` | 组件 8a 普通加粗（默认）/ 绿色加粗（锚点 ≤5） | 普通加粗为主 |
| `==高亮文字==` | 组件 8b 浅绿底深绿字标签 | 核心概念 |
| `<u>下划线</u>` / `++文字++` | 组件 8c 淡绿下划线 | 次要强调 |
| 行内 `` `code` `` | 组件 8d 行内代码 | |
| `> 引用段落`（旁注） | 组件 9b 灰色旁注块 | |
| 核心结论 | 组件 6 结论卡 | 每个要点 ≤1 张 |
| 核心金句 | 组件 13 居中金句 | 收束全文 |
| A/B 对比 | 组件 10 双栏对照卡 | |
| 并列要点（短标题+说明） | 组件 12b 药丸要点列表 | |
| 自查项 | 组件 12a 自查清单 | |
| 数据展示 | 组件 11a/11b 数据组件 | 绿色大号数据 |
| Markdown 表格 | 组件 11c 数据表格 | 偶数行浅绿底 |
| 资料 / 课程推荐 | 组件 7 嵌入式引流卡 / 16 文末课程卡 | **嵌入式优先** |
| 待补素材 | 组件 15 待补素材占位 | 居中板块 |
| `![](图片)` | 组件 14 图片容器 | 圆角卡片 + 说明 |
| `1. 2. 3.` 编号列表 | 组件 5 序号药丸 | 绿底序号 |
| 文末 | 组件 18 分隔线 + 19 END + 20 签名 | |
