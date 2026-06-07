# Production SOP v2.7 — Chicago 1990 chapter render rules

> 升级原因：v2.6 + Tony 2026-06-07 16:30 catch 到 P10 漏 fill + P1 列"太大"。post-mortem 出 2 个新规则：history-binding 和 proactive chapter-sweep。

## R0-R6 保留（见 sop_v2.6）

## R7 NEW — history-binding aesthetic

之前 Tony 已接受过的视觉风格（包括 baked column 宽度 / font size 比例 / 整体节奏）= **binding reference**。新版不允许偏移 > 20% 没强 justification。

**踩坑（这条原因）**：2026-06-07 P1 v3 列宽改成 80px (vs OLD 60-62px → +30%) → Tony reject "明显太大"。
- v1.3.1 R3' min font 28 强制让我 over-correct 列宽 → 视觉破坏

**实操**：
- artwork prep 阶段：要改 baked column 尺寸 → 先查 history reference / 上次审过的版本（chicago_r1_style 里 `vertical_column_reference_width_px: 65`）
- mbf v1.3.2 R8 `aesthetic_proportion_gate` warn-level：列宽 > reference × 1.2 → 出 warning，production 二次确认
- production agent：交付前对比新 vs OLD 视觉，明显偏移要 flag 给 alein2

## R8 NEW — proactive chapter-sweep audit

每次交付**必须扫全 chapter**（不光当次改的 page）+ 算法 audit + alein2 抽审。

**踩坑（这条原因）**：2026-06-07 我 audit 时**只看 P1/P3/P12**（Tony 当时 catch 的 3 张），**没主动扫其他 25 张**。Tony 已 live 看到 P10 漏 fill 才告诉我。
- 心理上我想着 "chapter re-fill 时一起改"
- 但 Tony 的容错点 = "已经看到的页就该现在没问题"，不是"等下次 re-fill"

**实操**：
1. production agent 交付 ANY page → mandatory：用 mbf v1.3.x algorithm audit 跑整 chapter 28-page → 自动 grep `"pass":false` + `"warnings":` 不空
2. alein2 收到交付 → 必抽审 random 3-5 张 OTHER 页（不只当次改的）
3. 任一发现 issue → 不走交付，回炉先

## R3' tiering（v1.3.2 调整）

v1.3.1 R3' hard fail-fast at min_vertical_font_px=28 太严，会把 chapter 1 OLD narrow column 也 reject。

v1.3.2 改成：
- min 28px = soft recommendation（22-28 warn）
- min 22px = hard floor（<22 fail-fast）
- max_vertical_slot_ratio 1.30 保持 hard

理由：chapter 1 OLD baked column 60-62px wide → 17 字竖排 18px = 接受 + warn，不强制 over-correct 列宽。

## 总结踩坑清单（v2.6 → v2.7 增量）

8. v3 改 baked column 80px (vs OLD 60) → Tony "明显太大" — R7 缺失
9. 只 audit Tony 指出的 3 张 → 漏 P10 漏 fill — R8 缺失
10. R3' min font 28 hard fail 强迫 column 加宽 → 触发 R7 违反 — R3' tiering 修正

---

## v2.7 工具依赖

- mbf v1.3.2（R8 aesthetic gate + R3' tiering）
- chicago_r1_style.yaml 加 `vertical_column_reference_width_px: 65`

push 到 `/srv/chicago/handbook/docs/sop_v2.7.md` 后通知 Estelle/Joshua。
