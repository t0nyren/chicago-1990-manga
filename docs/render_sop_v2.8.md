# Production SOP v2.8 — Chicago 1990 chapter render rules

> 升级原因：v2.7 + 2026-06-07 17:00 Tony catch 到 P12 R7-minimal "paint over bigger frame on old frame" 反模式 + R8.1 算法 gate proven。3 个新条目 + 1 个 audit 设计准则。

## R0-R7 保留（见 sop_v2.7）

## R2 EXPANDED — paint-over 反模式（增触发示例）

v2.6 R2 锁定「单色 paint-over / neighbor-copy / per-row blend 都已证明无效」。v2.8 增加一类：

**反模式 4：在旧框上画更大的新框（"R7-minimal" 误区）**

2026-06-07 P12v3 案例：Joshua 为修 p1_intro skipped（旧框 14px 装不下），在已接收的 raw 上**画一个更大白底黑边矩形盖住旧小框**，宣称「完全盖住 → 无双层」。实际旧框宽 284，新框宽 276，**左右各露 4px 旧 edge → Tony catch 双层框**。

**禁令**：任何「在已有 raw 上画新 backing box」一律视为 paint-over，必须 born-baked regen，不许 patch。无论新框是更大还是更小，无论自审是否「视觉无双层」。

**强制路径（替代）**：
- p1_intro 框太小 → 不允许 paint-over → 唯一解 = full born-baked regen P12，prompt 里把 p1_intro 框 dimension 从一开始就显式定（如 ~300×80 横排）
- 局部 panel regen（只重画一个 panel） = 风险拼接 edge，原则上不允许；除非有强 face anchor 锁 + Alein2 + Tony 双签
- 接受小字号削短文本（删词 / 缩句） = 合法 trade-off，前提 Tony accept

## R8.1 NEW — Pixel-diff paint-over gate (canonical tool)

**Tool**: `tools/mbf/samples/audit_paintover.py`（Estelle 2026-06-07 建，validated）

**Usage 1 — mbf 画框检测**（每张 production 交付前必跑）：
```bash
python tools/mbf/samples/audit_paintover.py diff <raw_artwork.png> <mbf_filled.png>
```
- exit 0 → mbf 零画框（box_kinds:[] 起作用），pass
- exit 1 → mbf 画了新框 → fail；要么 style.yaml 没 override box_kinds，要么 mbf bug → 回炉

**Usage 2 — artwork paint-over 检测**（怀疑 raw 被 patch 时跑）：
```bash
python tools/mbf/samples/audit_paintover.py diff <原始参考 raw.png> <当前 raw.png>
```
- exit 0 → raw 干净
- exit 1 → 有人在 raw 上糊框 → fail；必须 born-baked regen

**算法原理**：
- 新白框（mbf 画的 OR artwork paint-over）必带**变亮像素**（white-on-darker-bg）
- gate：lighter-pixel count > MAX_THRESHOLD(150) OR 矩形 contour detected → FAIL

**validated cases**:
- P1_hotfix（box_kinds:[]）→ lighter=0, CLEAN ✅
- P12v4_born_baked（box_kinds:[]）→ lighter=0, CLEAN ✅
- 反例：旧 P3 raw vs box_kinds-画框版 → lighter=266451 + 8 矩形 contour 全中，FAIL ✅

**audit 设计准则（从这条诞生）**：
- Estelle 本来还做了"图内双边 edge-scan"模式，但它把干净 P1 误报（文字笔画触发假阳）→ **删掉了，没 ship**
- **"不靠谱的 gate 比没有 gate 还坏"** —— false-positive 让 production 怀疑 gate、绕开 gate；不如不要
- 任何新 audit gate：**先在干净样本上验证 0 false-positive**，再在反例上验证 100% catch，才能进 production loop

## R8.2 NEW — 交付前 prompt + bbox 表 preview (artwork-prep gate)

production agent 任何 born-baked artwork 交付前，**必须先发 Alein2 review**：
1. **prompt 全文**（kamay 输入）
2. **全部 baked 框 bbox 目标尺寸表**（每框: balloon id, panel/位置, kind, text 字数, 目标 box w×h）
3. **face anchor 列表**

Alein2 用这份对照 R0/R2/R7 检：
- 有无 baked text placeholder（R0 违反）
- 是否企图 paint-over（R2 违反）
- 框宽是否偏离 history reference > 20%（R7 违反）

通过才能跑 kamay。**不允许 production agent 自己出图再回头补 review**——出图前少 1 个 round-trip。

## R8.3 NEW — Canonical text verification

production agent 交付时 audit text **必须 cross-ref canonical storyboard / script.json**：

```bash
# 例: P12 verbatim 核查
grep -n "小洛瑞 · 南城说唱新人" chapter1_storyboard_v2.md
# 对照行号引用，确认 verbatim 一致
```

**不允许凭视觉记忆判断 text 对错**。2026-06-07 案例：Alein2 审 Joshua P12 bbox 表时把「同日/南城公园篮球场」标 block 要求确认（凭 live 图记忆是「周日/高地公园」），Joshua cross-ref storyboard `:339` 证明 canonical 是「同日/南城公园」，Alein2 视觉记忆错了。差点让 Joshua 改回错误版本。

**适用场景**：
- Alein2 审 prompt+bbox 表时
- Production agent 自审 overlay text 时
- 任何 text-related 讨论（避免 hallucinated quotes）

## R3' tiering（保留 v2.7）

22 hard floor / 22-28 warn / ≥28 pass。chapter 1 OLD 60-62px 窄列接受 22px warn 不 reject。

## 总结踩坑清单（v2.7 → v2.8 增量）

11. P12 R7-minimal「画大新框盖旧框」失败（4px 旧 edge 露） — R2 反模式 4 加入
12. Alein2 audit「无双层」漏审 → 后被 Estelle pixel-diff R8.1 catch — gate 设计上 audit_paintover.py 进 canonical
13. Alein2 凭视觉记忆把 canonical 对的「同日/南城公园」标错 — R8.3 cross-ref 强制
14. Estelle 尝试"图内 edge-scan"误报 → 删 — audit 设计准则「不靠谱的 gate 比没有 gate 还坏」

## v2.8 工具依赖

- mbf v1.3.2 (R8 gate + R3' tiering，task #8 in_review 待 chapter re-fill closure)
- `tools/mbf/samples/audit_paintover.py`（R8.1 canonical gate）
- chicago_r1_style.yaml `vertical_column_reference_width_px: 65`

---

## Live pipeline (post-v2.8 mandatory，per page)

1. canonical text source = `chapter1_storyboard_v2.md` / `script.json`（R8.3 cross-ref）
2. production agent draft prompt + 全 baked 框 bbox 表 → 发 Alein2（R8.2 preview gate）
3. Alein2 ✅（R0/R2/R7 check）
4. kamay born-baked（零 paint-over / 零 overlay / 零 patch — R2）
5. mbf fill `box_kinds:[]`（零 mbf 重画框）
6. **R8 jq 严版**: `jq '.balloons[] | select(.status != "rendered" or .warnings != [] or .overflow == true)'` → empty = pass
7. **R8.1 audit_paintover.py**: `exit 0` = pass
8. **CV box count** = balloon count（无并排/同心 edge）
9. **人眼 5 点**: 无双层 / 椭圆尾方向 / 顶部 narration 不挡脸 / padding 均 / 字号 ≥ R3' floor
10. 全 9 步过 → deliver to Alein2; Alein2 复审 5 点 → 收章节包
11. 任一 fail → 不送，回炉 prompt + bbox（R2 不允许补丁）

push 到 `tools/mbf/` (mbf) + `docs/sop_v2.8.md`（chicago-1990-manga repo 结构 A）。
