# Production SOP v2.6 — Chicago 1990 chapter render rules

> 升级背景：v2.5（layout gates）+ R1-R4（白底黑字/旧框/间距/全渲染）+ **本轮 2026-06-07 P1/P3 重做失败教训**，固化为 v2.6。
>
> 主旨：**artwork generation 必须输出干净 canvas，所有 text rendering 由 mbf + PIL 全权负责**——任何 baked-in text placeholder 都会在后续修改时变成不可解的 trade-off。

---

## R0（最高优先级）— 干净 artwork 原则

**artwork generation prompt 禁止指令包括**：
- "white narration column / box / banner"
- "vertical text placeholder"
- "speech balloon outline"
- 任何让 AI 在画面里**留出/画**给文字用的形状

raw artwork **只画画面内容**——人、物、场景。所有 text bbox 由 mbf script + PIL 全权后期处理。

**踩过的坑（不要再踩）**：
- 2026-06-07: P1v2/P3v2 raw artwork 含 baked 白色 vertical narration columns。后续 PIL post-pass 在这些固定形状内画字，column 太瘦字号被压死（17/24px）。修改时改 bbox = 字号变更 + 旧 column 痕迹无解。**根因：raw 里有 placeholder。**

## R1 — 白底黑字 only

所有 narration / caption / timestamp / intro / 旁白都白色背景 + 黑色文字。**禁止** dark-bg + white-text。

mbf style.yaml 必须用 `samples/chicago_r1_style.yaml`：
- `dark_box_fill: "#FFFFFF"`
- `text_color_dark: "#000000"`
- `text_orientation.narration: horizontal` （vertical 由 PIL 处理，不走 mbf）
- `layout.dark_box_ring_dark_min_pct: 0.0` （禁用 dark-ring gate，因白底已不适用）

## R2 — 旧 column 痕迹（仅适用 R0 违反时）

⚠️ **R0 后此条不应触发**：新 artwork 不含 baked column。

如果继承存在 baked column 的 artwork（不推荐），单色 paint-over / neighbor-copy / per-row blend **都已证明无效**：
- 单色 → brown / 棕色 bar
- neighbor-copy → 复制角色身体
- per-row blend → 平滑但仍有色块

**结论：必须重生成 artwork（R0），不要尝试在 baked artwork 上 patch。**

## R3 — vertical 字符间距

vertical column 字符 `slot_h / font_size ≤ 1.4`（紧致）。

实现：font = min(bw-8, (bh-18)/(n*1.18))，pack_ratio 1.18。bh 可自由（因 R0 artwork 干净），不受历史 column extent 约束。

## R4 — 全 balloon 渲染

修改任意 balloon 时，script 里其他所有 balloon 必须照常渲染。overlay JSON rendered[] 长度 == script balloon count。

## R5（NEW from 2026-06-07）— artwork 必须 narration-free

R0 的执行细则：raw artwork 出来后必须做 narration-free 自查：
1. CV 扫描：detect 任何 thin tall white rectangles / boxed empty regions
2. 任何疑似 placeholder 必须**重新生成 artwork**（不在该 artwork 上加 patch）

## R6（NEW from 2026-06-07）— per-PNG eye-review + 4-gate audit 才能发 Tony

任何发给 Tony 的图必须：
1. **人眼逐 PNG 审一遍**（不只看 metadata）
2. R1-R5 自审表 + audit 全 pass
3. 任何 gate fail → 不发图 → 改 → 重 audit → fail 三次同一类 issue 必须**升级方案而非小补**

**踩过的坑**：本轮 P1/P3 修了 7 个 version（r1, r1b, r1c, r1d, v5, v6, v7），每次都"audit 全 PASS"却被 Tony 看出新问题。证明 audit 表不等于视觉接受。

---

## Render Stack (v2.6 默认)

```
[stage 1] artwork generation
  - kamay / atlas with face anchor reference
  - prompt 严格遵守 R0+R5：no baked text elements
  - output: clean panel artwork only (832×1248)
  
[stage 2] script
  - script.json with balloons, kind, text, bbox
  - bbox 自由选择（R0 后无 placeholder 约束）
  
[stage 3] mbf v1.2 + chicago_r1_style
  - horizontal narration boxes (white-bg+black-text)
  - --strict-layout 强制
  
[stage 4] PIL post-pass — **DEPRECATED 2026-06-07** (Tony directive)
  - ⛔ production agents 不再写任何 PIL render hack（vcol/pack_top/paint-over）
  - ⛔ 替代：vertical/pack/R3/R5 全部进 mbf v1.3 工具层
  - 见 #manga-tool task #6 v1.3 spec：`--pack-mode top` / R3 spacing gate / R5 placeholder pre-check / R1 默认白底黑字
  - **mbf v1.3 ship 前 chapter 1 P1v2/P3v2 hold 不渲染**；ship 后纯 mbf 跑
  
[stage 5] audit
  - R1-R6 全 pass + 人眼复审
  - 任一 fail → 不交付
  
[stage 6] deliver to Tony
  - 发预览 + 等 👍
  - 部署：rsync /srv/chicago + COS rename v{N}fix + 删旧 + manifest
```

---

## 历史踩坑清单（agent 重启后读这个）

1. **AI 误判**：以为竖排是 AI 直接画的，实际是 PIL post-pass — 必须看 render scripts 才能定位渲染入口
2. **mbf style.yaml 默认 narration vertical**：导致 chicago_r1_style 不显式 override 就把横排 bbox 渲成隐形细条
3. **单色 paint-over**：sampled bedroom OK，sampled brown 不 OK → 不可靠
4. **r1c full-height pack_top**：白条太高（Tony reject）
5. **r1d shorter cols**：白框底下莫名白框（Tony reject）
6. **v6 neighbor-copy**：复制角色身体（Tony reject）
7. **v7 per-row blend**：平滑但 Tony 仍 reject — 因为根因是 baked column 本身

**通用 takeaway**：当一个修复路径出 3 个不同问题时，停下来重思 root cause；很可能上游 input 就错了，不是当前 patch 算法不对。
