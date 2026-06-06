# 《芝加哥1990》漫画化项目 · 工作手册

> 给 Alein@opus（lead/AE）+ #Content Production 频道里所有 production agent 用。新人 onboarding 先读这份。

---

## 1. 项目背景

把 Tony 的小说《芝加哥1990》（1520 章）漫画化。**当前阶段**：第一话（28 页，对应原著第 1-7 章「家庭」→「天启」）。

**质量基线**：现代彩色 manhwa-seinen 半写实漫画，参考 Mangaplus 条漫的**构图 / 运镜 / 分镜 / 对白节奏**，**画风保持彩色，不抄 mangaplus 的黑白重墨**。

---

## 2. 角色分工

| 角色 | 谁 | 干啥 |
|---|---|---|
| **Lead / AE** | @Alein@opus | 写 task spec / review / approve / 沟通 Tony |
| **Production** | @EstelleBright@breeze + @JoshuaBright@breeze | 跑 prompt 生成 + 跑 mbf fill + 自查 + 交付给 Alein |
| **Tool maintainer** | #manga-tool 频道（Altina + RenneBright） | mbf 任何升级走那边派活 |

---

## 3. 锁定参数（不要改，除非 Tony 说改）

### 3.1 风格
- **画风**：colored manhwa-seinen 半写实 + soft cell shading + 1990 冷色板（charcoal / faded indigo / off-white / olive-brown / 浅 caramel 肤色 + 老乔粉作 accent）
- **NOT**：heavy seinen ink / screen tone B&W / smooth Pixar CG / bright cartoon

### 3.2 出图参数
- **模型**：`kamay image generate-image --model gpt-image-2`
- **比例**：`--aspect_ratio 2:3 --resolution 1K` → 实际输出 **832×1248**
- **face anchor**：`--reference_images https://chicago.secondlife.today/songya_face_anchor.png`
- **如果 content policy 拦截**（500 task_failed）：rewrite prompt 去掉敏感措辞，比如"smoking"改"chatting"、"undressing"等改保守措辞，所有未成年角色保持 fully clothed

### 3.3 气泡 / 文字框
- **shout（喊话）**：jagged 尖刺只画外 border / 内部 ONE continuous white area / **不能**在尖刺内再画 oval 描边
- **dialogue（对白）**：圆 / 椭圆 / 干净 thin black border
- **thought（心声）**：云朵 / 带 trailing bubbles
- **narration（旁白 / 角色介绍）**：白底矩形 thin black border / 黑字
- **sfx（拟声）**：白底 jagged 大字斜穿
- **统一规则**：所有 inner 必须**纯白色**等后期 mbf 填字 / 不要让 AI 画字进去

### 3.4 角色第一次出现 → 强制加介绍框
（Tony 2026-06-06 directive）：每个角色第一次正面出场时，画面里要有一个**矩形白底 narration 框**写角色身份（参考原著小说作者的介绍语），画面构图要把这角色摆在视觉焦点位置。

**触发首次出现的页**：P2（康妮）/ P4（苏茜 / 托尼 / 艾米丽 / 弗雷迪）/ P6（ET）/ P11（消音器）/ P12（小洛瑞）/ P20（AK）

---

## 4. 工作流

```
[Lead] 写 task spec (页号 + 故事内容 + panel 设计 + 气泡列表 + prompt)
        ↓ 在 #Content Production 派活
[Production] 跑 pipeline: kamay 出图 → 自动检测 bbox → mbf fill → overlay JSON
        ↓ 交付 filled PNG + overlay JSON + script.json
[Lead] review: overlay JSON 必查 overflow=False + warnings=0 + per-balloon crop 目视
        ↓ 不过让 production 修；过了 → 发 #Chicago
[Tony] final check
        ↓ 不过 → Lead 回 production 修；过了 → archive
```

### 4.1 production agent SOP（execute time）
1. 收到 task spec 后**回复确认 + 等几分钟批准**（避免误操作）
2. 跑 `python3 run_batch.py <PAGE_IDS>`（pipeline 全自动 → 生成 + 检测 + 填字）
3. 看 overlay JSON：`p?_xxx | font_px | rows | overflow=False | warnings=OK` 全绿才算 OK
4. 不绿就调 bbox（`script-ch01-p?.json`），重 fill 直到全绿
5. 跑 `python3 audit_overlay.py script-ch01-p?.json P?_v3_filled.png P?_v3_audit.png` 出审计图
6. 在 #Content Production 上传 **filled PNG + audit overlay + overlay JSON 表格** 交给 Alein review

### 4.2 lead review SOP
1. 拉每张 filled PNG 本地放大看每个气泡：
   - ✅ 字完整？没漏首字 / 末字
   - ✅ 字不出 bbox / 不出气泡白色 inner？
   - ✅ 白底气泡黑字 / 不要黑底黑字看不见？
   - ✅ kind / speaker / 字数对得上 script？
2. 跑画面 sanity：人物有没有多手 / 多腿 / 脸不像 face anchor？
3. 全 pass 才上传到 #Chicago + Tony

### 4.3 mbf 升级
- 任何 mbf 渲染器问题（new kind 支持 / 文字颜色 / fontfamily / 等等） → 在 #manga-tool 频道开 task，**不要**直接 SSH 改 `/srv/manga-tool/src/`

---

## 5. 关键文件位置

### 5.1 Alein workspace（lead）
```
/Users/dongniren/.syfo/.../agents/<alein>/manga_output/chapter1/
├── pipeline.py            # kamay + detect + fill + audit 库
├── run_batch.py           # 单页 / 多页跑 pipeline
├── pages_config.py        # 所有页的 prompt / balloons / panel_id config
├── audit_overlay.py       # 给 filled PNG 画 bbox + ID overlay
├── scripts/v3/            # 自动生成的 script-ch01-p*.json + prompt-ch01-p*.txt
├── chicago1990_characters_arc1.md   # 39 人人物档案
└── (raw + filled PNGs)
```

### 5.2 服务器（root@129.226.144.118 / chicago.secondlife.today）
```
/srv/chicago/                  # 公网可访问的资产
├── songya_face_anchor.png    # face anchor URL（喂 kamay 用）
└── manga-tool-samples/       # mbf 用的 fixture
/srv/manga-tool/               # mbf 部署
├── src/mbf/                  # 不要直接改
├── style.yaml                # 不要直接改
├── samples/                  # production agent 把图放这
└── out/v3/                   # mbf fill 输出 + overlay JSON
```

### 5.3 mbf CLI 用法
```bash
ssh -i ~/.ssh/id_ed25519 root@129.226.144.118
source /srv/manga-tool/.venv/bin/activate
mbf fill samples/<page>.png samples/<script>.json -o out/v3/<filled>.png --debug
# overlay JSON 在 out/v3/<filled>-overlay.json
```

---

## 6. 内容政策 / 安全措辞

- 未成年角色（宋亚 15 / 艾米丽 10 / 弗雷迪 婴儿）**永远 fully clothed**，不要写 "sleeveless" / "undershirt" / "shirtless" / "bathing"
- 暴力场景（P14 拔枪 / P15 寂静 / P22-P27 偷听 + 天启）措辞克制：枪用 "concealed gun grip"，不写 "drawing / firing"；冲突用 "confrontation" / "pushing" 不写 "fight / brawl"
- 帮派 / 烟 / 酒：去掉 "smoking"，改 "chatting" / "leaning on bench"

---

## 7. 章节进度（live）

| 页 | 状态 | 备注 |
|---|---|---|
| P1-P11 | ✅ 发 Tony 已批 | 待加首次出场介绍框（P2 / P4 / P6 / P11） |
| P12-P15 | ⏸️ 自查通过，等 Tony 调整完再发 | 12 需加小洛瑞介绍 |
| P16-P19 | ⏳ 待做 | — |
| P20 | ✅ 发 Tony 已批 | 待加 AK 介绍框 |
| P21-P28 | ⏳ 待做 | — |

---

## 8. 资产管理结构（待 Tony 拍板：GitHub vs COS vs chicago server）

**推荐 hybrid**：
- **GitHub repo（待建）**：代码 + script JSON + prompts + 这份 handbook + 角色档案 markdown
- **chicago.secondlife.today**（已存在）：所有 PNG（raw + filled + audit overlay + face anchor reference）
- 每张 PNG 同步上传到 `/srv/chicago/chapter1/{raw,filled,audit}/P?_v3*.png`，公网 URL 直接给 production agent 喂图

---

## 9. 版本历史

- **v1**（前期）：atlas + gpt-image-2 + 1024×1536，工作流逻辑反（先 AI 出气泡，反推脚本）
- **v2**（前期）：atlas + gpt-image-2 + 加 webtoon 动感语汇（motion line / color wash / 多层旁白），但仍是先图后字
- **v3.1**（弃）：kamay nano-banana-2 + 3:4 → 风格 / 比例都错
- **v3.2**（弃）：gpt-image-2 + 2:3 + dramatic seinen ink → 风格错，Tony 不要黑白重墨
- **v3.3**（弃）：colored manhwa + 黑底 narration → 字看不见
- **v3.4**（**当前 baseline**）：colored manhwa + 2:3 + 白底 narration + shout oval inner + bbox 自动检测 + per-kind padding
