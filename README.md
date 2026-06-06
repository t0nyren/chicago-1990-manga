# Chicago 1990 Manga

漫画化 Tony 的小说《芝加哥1990》。

## 当前状态
**第一话 P1-P28**（对应原著第 1-7 章）— production in progress

## 重要文件
- `PROJECT_HANDBOOK.md` — 项目手册（必读）
- `docs/character_introductions.md` — 角色首次出场介绍框总表
- `docs/chapter1_storyboard_design.md` — 第一话分镜设计
- `docs/chicago1990_characters_arc1.md` — 39 人物档案
- `code/` — pipeline / 自动化脚本
- `pages/chapter1/scripts/` — script-ch01-p*.json
- `pages/chapter1/prompts/` — prompt-ch01-p*.txt

## 资产
图像不进 repo，存放于 `chicago.secondlife.today`：
- `https://chicago.secondlife.today/songya_face_anchor.png` — face anchor
- `https://chicago.secondlife.today/chapter1/{raw,filled,audit}/P?_v4*.png` — 各页 PNG（待整理）

## 工具链
- `kamay image generate-image --model gpt-image-2` 出图
- mbf（root@129.226.144.118:/srv/manga-tool/）填字
- pipeline.py 编排

## 角色分工
- @Alein@opus — lead / AE / review
- @EstelleBright@breeze + @JoshuaBright@breeze — production
- #manga-tool 频道（Altina + RenneBright） — 工具维护

