# 角色第一次出场介绍框 · 总表

> 用法：每个角色第一次正面出场的页 / 格，必须**配一个白底矩形 narration 框**（带 thin black border），内容是简洁版的角色身份。production agent 制作那页时照表写 narration 框的字。

> 介绍文字按 Tony 2026-06-06 directive：精简到 10-18 字，落在原著作者第一次描写的语气上。画面构图要把这角色摆在视觉焦点位置（C 位 / 大特写 / 高光等）。

> **Tony 2026-06-06 22:55 新规**：漫画段落末**不加句号**。问号 / 感叹号 / 破折号 / 省略号正常保留。本表已应用新规。

---

## 第一话出场顺序 + 介绍框规格

| 出场页 | 格 | 角色 | 视觉锁 | narration 框文字（≤18字，**无句号**）|
|---|---|---|---|---|
| **P1** | 整页 splash 旁白 | 宋亚 / Songya | 床上侧躺 | "我叫亚力山大·宋" + "穿越后第十四天"（已在 P1 用） |
| **P2** | 第 3 格 | 康妮 | 鲜艳荧光珊瑚紧身派对裙 + 大金圈耳环 / 横向身材 / 宿醉脸 | **"康妮 · 表姐 · 17 岁"** |
| **P4** | 顶部大格 | 苏茜姨妈 | 水桶身材 + 头巾 + 鲜艳家居袍 + 一手锅铲一手抱婴儿 | **"苏茜姨妈 · 5 个孩子的单亲妈妈"** |
| **P4** | 顶部大格 | 托尼 | 微胖肚 + 工厂大衣 + 仰头喷奶油 | **"托尼 · 表哥 · 校橄榄队 · 17"** |
| **P4** | 顶部大格 | 艾米丽 | 10 岁 / 双麻花辫 / 浅咖肤 / 倒牛奶 | **"艾米丽 · 妹妹 · 10 岁"** |
| **P4** | 顶部大格 | 弗雷迪 | 婴儿 / 黑白混血 / 蓝眼睛 / 苏茜怀里 | **"弗雷迪 · 苏茜的小儿子 · 不到 1 岁"** |
| **P6** | 第 2 格 | ET | 棒球帽压低 + 花头巾边角 + 凑近托尼 | **"ET · 站台上常见的脸"** |
| **P11** | 第 1 格 大格 | 消音器 / 穆特 | 高壮 + 黑 bomber 夹克 + 极沉默面容 + 丰田 86 雄鹰 | **"穆特 · 外号'消音器' · 17 · 沉默"** |
| **P12** | 第 1 格 | 小洛瑞 | 瘦 + baby face + 整齐脏辫 + 大耳机 + 牛仔衬衫 + 篮球 | **"小洛瑞 · 南城说唱新人 · 托尼儿时好友"** |
| **P20** | 第 1 格 | 消音器（reprise，西装造型） | 一身黑西装配墨镜守在 XX 舞蹈教室门口 | （消音器已在 P11 介绍过，**不再加框**） |
| **P20** | 第 2 格 | AK | 25 岁 / 白领黑西装 / 持文件夹 / 没艾尔随和 | **"AK · 老乔音乐的对接人 · 25"** |

> 第一话只需要这 9 个介绍框。其余配角（艾尔 / 老乔 / 巴勃罗 / 米拉 等）第一话不出场。

---

## 介绍框设计规则

### 视觉
- **形状**：白底矩形 + thin black border
- **大小**：约 200×60 像素（横版）或 110×220 像素（竖版），根据 panel 内空隙定
- **位置**：贴角放置（panel 左上 / 右下 / 等），不要遮住角色脸 + 不要遮住关键道具
- **不能**用 dark fill + 白字 (Tony 2026-06-06 directive)
- **不能**画得太"标签贴纸感" — 跟其他 narration 框 visually 保持一致

### 文字
- ≤18 字
- **不加句号**（Tony 22:55 新规，本规则适用所有 narration / dialogue / 介绍框）
- 用 ? / ! / 破折号 / 省略号正常保留
- 第一行写**名字 + 身份**，第二行（如有空间）写**关键标签 / 年龄**
- 例："康妮 · 表姐 · 17 岁"

### 画面配合
- 第一次出场的角色要在 panel 里占视觉焦点（C 位 / 大特写 / 高光 / 单独成格）
- 不要让多个新角色挤在同一格的边缘 — 如果一格有多人首登（如 P4 早餐桌 4 人同时首登），构图要让每个角色都有一个清晰的视觉锚点 + 各自的介绍框分布在角落

---

## 给 production agent 的执行清单

每次接到一页 task spec，先问自己：
1. **这页有谁是第一次出场？** 比对上表
2. **要不要加介绍框？** 是 → 在 prompt 里**多加一行**：'ALSO add a small WHITE NARRATION RECTANGLE in panel X corner Y, approximately AxB pixels' + 加到 balloons 列表里 (kind: narration, text: 表里的对应文字)
3. **构图要给这角色 C 位 / 高光吗？** 是 → 在 prompt 的 scene description 里说明 "X is the visual focus of this panel"
4. **写 text 时**：不加段落末句号（问号 / 感叹号 / 破折号 / 省略号保留）
5. 自查 overlay JSON 时确认介绍框的 bbox 和文字渲染都通过

---

## V2 anchor 库（live URLs）

每页生成时按需喂 kamay 的 `--reference_images URL1,URL2,URL3`：

| 角色 | Anchor URL |
|---|---|
| 宋亚 | https://chicago.secondlife.today/anchors/songya_v2_halfbody.png |
| 苏茜姨妈 | https://chicago.secondlife.today/anchors/suzie_anchor.png |
| 托尼 | https://chicago.secondlife.today/anchors/tony_anchor.png |
| 康妮 | https://chicago.secondlife.today/anchors/connie_anchor.png |
| 艾米丽 | https://chicago.secondlife.today/anchors/emily_anchor.png |
| ET | https://chicago.secondlife.today/anchors/et_anchor.png |
| 消音器 | https://chicago.secondlife.today/anchors/silencer_anchor.png |
| 小洛瑞 | https://chicago.secondlife.today/anchors/lil_lorry_anchor.png |
| AK | https://chicago.secondlife.today/anchors/ak_anchor.png |

所有 anchor 都是手绘 manhwa 风（半身 / 灰底纸感）+ 跟 Songya v2 风格统一。
