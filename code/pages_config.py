"""Page configs for Chapter 1 P2-P19, P21-P28.

Each page = {
  page_id, title, prompt_body (panel layout + scene + balloon placement),
  balloons: [{balloon_id, kind, speaker, text}],
}

The pipeline:
1. Build full prompt = STYLE_PREAMBLE + prompt_body
2. Generate via kamay
3. Auto-detect white bboxes
4. Assign bboxes to balloons by user-provided ordering hint
5. Fill + audit
"""

PAGES = {
    "P2": {
        "title": "起床 4 panel · 楼下骂街继续",
        "prompt_body": """PAGE LAYOUT: 2x2 grid (4 panels of roughly equal size).

PANEL 1 (TOP-LEFT — bed close-up): Songya in bed, side profile awake, eyes open with sleepy furrowed brow. Bedsheet visible. Cold blue-gray dawn light from upper right window. Bedroom wall behind.
  BALLOONS:
  (a) Center: ONE LARGE JAGGED-OUTER OVAL-INNER SHOUT BALLOON entering from the bottom-left of the panel, the oval inner white area approximately 200x140 pixels, jagged spikes radiating outward, with tail extending downward through panel border. Pure white empty interior.

PANEL 2 (TOP-RIGHT — sitting up putting on sweater): Songya sitting up on the bed edge, pulling a dark blue thick wool sweater over his head, motion lines on shoulders. Bed messy behind him. Same blue-gray dawn lighting.
  BALLOONS:
  (a) Upper area: ONE MEDIUM CLOUD-SHAPED THOUGHT BUBBLE with small trailing bubbles toward his head, pure white empty interior, approximately 160x110 pixels.

PANEL 3 (BOTTOM-LEFT — cut to Connie shouting back at the stairs): Connie (heavyset Black-American woman early 30s, neon-coral tight 1980s short party dress, big gold hoop earrings, smudged makeup) mid-shout from the stair landing, mouth open wide. Slight camera tilt about 7 degrees.
  BALLOONS:
  (a) Center-right dominating panel: ONE EXTRA LARGE JAGGED-OUTER OVAL-INNER SHOUT BALLOON with tail pointing to Connie's mouth, the clean oval inner white area approximately 260x180 pixels. Pure white empty interior.

PANEL 4 (BOTTOM-RIGHT — Songya hidden smirk close-up): Tight half-profile close-up of Songya, corner of mouth curling into a small private smirk, eyes lowered with fond amused glint. Flat cool muted blue-gray color wash background simplified, no detail. His face occupies about 60% of panel.
  BALLOONS:
  (a) Upper-right: ONE SMALL CLOUD-SHAPED THOUGHT BUBBLE pure white empty, approximately 130x90 pixels.
  (b) Bottom-left: ONE SMALL HORIZONTAL WHITE NARRATION RECTANGLE thin black border, pure white empty interior, approximately 180x55 pixels.
""",
        "balloons": [
            # panel_id: 1=top-left, 2=top-right, 3=bottom-left, 4=bottom-right
            {"balloon_id": "p1_shout_aunt", "panel_id": 1, "kind": "shout", "speaker": "苏茜姨妈（楼下）", "text": "M-FXXX 的十七岁! 十七岁就 M-FXXX 学会像个碧池一样地夜不归宿了!"},
            {"balloon_id": "p2_thought_used_to_it", "panel_id": 2, "kind": "thought", "speaker": "宋亚（心声）", "text": "穿越过来已经十几天了。"},
            {"balloon_id": "p3_shout_connie", "panel_id": 3, "kind": "shout", "speaker": "康妮", "text": "Yeh, Yeh! 说到碧池，也不知道是谁十七岁的时候连孩子都生俩了!"},
            {"balloon_id": "p4_thought_blood", "panel_id": 4, "kind": "thought", "speaker": "宋亚（心声）", "text": "亲生的。"},
            {"balloon_id": "p4_narration_home", "panel_id": 4, "kind": "narration", "speaker": "旁白", "text": "这就是家。"},
        ],
    },
    "P3": {
        "title": "卫生间镜中身份 4 panel",
        "prompt_body": """PAGE LAYOUT: 2x2 grid (4 panels of roughly equal size).

PANEL 1 (TOP-LEFT — bathroom faucet close-up): Songya's hand twisting on a faucet handle, water rushing out. Tight close-up.
  BALLOONS:
  (a) Upper area: ONE LARGE JAGGED SOUND-EFFECT BLOCK approximately 180x130 pixels, pure white empty interior, thick rough black border, slanted diagonally about 25 degrees.

PANEL 2 (TOP-RIGHT — looking up at mirror): A medium half-body shot of Songya facing a small bathroom mirror, his face partly visible at three-quarter angle — match face anchor reference closely. Light caramel mixed-race skin, slightly Asian almond eyes, short curly black hair, slightly round youthful face. Neutral curious expression. Fully clothed in his dark long-sleeved sweater.
  BALLOONS: none in this panel.

PANEL 3 (BOTTOM-LEFT — touching cheek thoughtfully + narration): Songya pressing his cheek with his fingertips, eyes lowered, calm thoughtful expression. Fully clothed in his dark sweater.
  BALLOONS:
  (a) Upper-left: ONE TALL VERTICAL WHITE NARRATION RECTANGLE with thin black border, pure white empty interior, approximately 60x320 pixels.

PANEL 4 (BOTTOM-RIGHT — eye extreme close-up): Extreme close-up of Songya's eye (one eye only filling the panel), pupil reflecting a vague light spot. Used to drop into emotional inner monologue.
  BALLOONS:
  (a) Lower-right: ONE TALL VERTICAL WHITE NARRATION RECTANGLE with thin black border, pure white empty interior, approximately 55x300 pixels.
""",
        "balloons": [
            {"balloon_id": "p1_sfx_water", "panel_id": 1, "kind": "sfx", "speaker": "拟声", "text": "哗——"},
            {"balloon_id": "p3_narration_appraise", "panel_id": 3, "kind": "narration", "speaker": "旁白", "text": "按华国人的审美来算，这张脸长得还不赖。"},
            {"balloon_id": "p4_narration_transmigrate", "panel_id": 4, "kind": "narration", "speaker": "旁白", "text": "穿越者没带前世记忆。"},
        ],
    },
    "P4": {
        "title": "早餐桌家庭群像 5 panel",
        "prompt_body": """PAGE LAYOUT: Top half = ONE wide horizontal large panel spanning full page width (about 50% of page height). Bottom half = 2x2 grid of 4 smaller panels.

PANEL 1 (TOP WIDE — breakfast table ensemble): Wide establishing shot of a cluttered breakfast table in a small kitchen. From left to right: SUZIE (heavyset aunt, headscarf, bright patterned house robe, spatula in one hand holding baby FREDDIE in the other), TONY (slightly chubby, factory jacket, head tipped back about to spray whipped cream into his open mouth), CONNIE (in faded house robe — morning not yet dressed up — pouring oatmeal with eye roll), EMILY (10 year old twin braids, pouring milk), SONGYA (just sitting down). Morning warm amber kitchen light. Plates, cereal boxes, coffee mugs on table.
  BALLOONS: none in this panel.

PANEL 2 (BOTTOM-LEFT — Tony offering whipped cream): Medium close-up of Tony turning the whipped cream can toward Songya offering to spray it.
  BALLOONS:
  (a) Center: ONE SMALL ROUNDED OVAL SPEECH BALLOON, pure white empty interior, approximately 150x80 pixels, tail pointing to Tony's mouth.

PANEL 3 (BOTTOM-CENTER-LEFT — Songya declining with inner monologue): Medium shot of Songya politely shaking his head, slight tense expression.
  BALLOONS:
  (a) Upper-left: ONE SMALL ROUNDED OVAL SPEECH BALLOON pure white empty interior, approximately 110x70 pixels, tail to Songya's mouth.
  (b) Lower-right: ONE MEDIUM CLOUD-SHAPED THOUGHT BUBBLE pure white empty interior, approximately 220x110 pixels.

PANEL 4 (BOTTOM-CENTER-RIGHT — Tony's probing line): Medium close-up of Tony pointing the cream can casually toward Songya, slight scrutinizing expression.
  BALLOONS:
  (a) Center: ONE MEDIUM ROUNDED OVAL SPEECH BALLOON, pure white empty interior, approximately 230x100 pixels, tail to Tony's mouth.

PANEL 5 (BOTTOM-RIGHT — Connie's chaotic save): Medium shot of Connie pointing at Songya across the table with bemused expression, mouth open mid-shout.
  BALLOONS:
  (a) Center: ONE LARGE JAGGED-OUTER OVAL-INNER SHOUT BALLOON, pure white empty interior approximately 240x140 pixels, tail pointing to Connie's mouth.
""",
        "balloons": [
            # P4 layout: top wide panel (1) covers top ~50%, then 2x2 grid for panels 2-5
            # panel_id 1=top wide; 2=bottom-left-top; 3=bottom-left-bottom… simplify: map panels 2-5 to vertical strips
            # Quadrant mapping for layout 3 rows x 2 cols means panel 1 occupies rows 1+ cols 1-2; not quite. We use 4 sub-panels mapped to 2x2 in bottom half.
            # Better approach: tag panel_id 2,3,4,5 with explicit positions when needed. Use "panel_pos" hint as well.
            # P4 layout is 3x2 grid (top wide = grid panels 1,2 merged; bottom 2x2 = grid panels 3,4,5,6)
            {"balloon_id": "p2_tony_open", "panel_id": 3, "kind": "dialogue", "speaker": "托尼", "text": "张嘴。"},
            {"balloon_id": "p3_songya_no", "panel_id": 4, "kind": "dialogue", "speaker": "宋亚", "text": "不了。"},
            {"balloon_id": "p3_songya_thought", "panel_id": 4, "kind": "thought", "speaker": "宋亚（心声）", "text": "肥胖是我这一世要时刻警惕的敌人。"},
            {"balloon_id": "p4_tony_changed", "panel_id": 5, "kind": "dialogue", "speaker": "托尼", "text": "你最近变了很多，亚力。"},
            {"balloon_id": "p5_connie_save", "panel_id": 6, "kind": "shout", "speaker": "康妮", "text": "多简单的事! 为了女人呗! 你和谁搞上了?"},
        ],
    },
    "P5": {
        "title": "出门街景 3 panel",
        "prompt_body": """PAGE LAYOUT: Three vertically stacked horizontal panels of varied heights. Panel 1 takes top ~30% of page, Panel 2 takes middle ~45% of page (wide environmental shot), Panel 3 takes bottom ~25% of page.

PANEL 1 (TOP — four siblings stepping out the front door): Tony pushing open the door, with Emily wrapped in his arms shielding her from cold wind. Connie behind in heavy coat. Songya behind. Stoop and brick steps visible.
  BALLOONS: none in this panel.

PANEL 2 (MIDDLE WIDE — Chicago South Side street establishing shot): Wide angle of a dilapidated 1990 Chicago South Side residential street — small worn African flag near a doorway, gray dead winter grass, rusted iron fences, cold blue-gray February sky, leafless trees, tenement rowhouses in the distance, snow patches on pavement. No characters in this shot.
  BALLOONS: none in this panel.

PANEL 3 (BOTTOM — Songya's feet on cracked pavement + narration overlay): Tight close-up of Songya's worn off-white sneakers walking on cracked pavement with snow patches.
  BALLOONS:
  (a) Right side: ONE LARGE HORIZONTAL WHITE NARRATION RECTANGLE with thin black border, pure white empty interior, approximately 380x90 pixels.
""",
        "balloons": [
            {"balloon_id": "p3_narration_southside", "panel_id": 3, "kind": "narration", "speaker": "旁白", "text": "这里是芝加哥南城。我的新家。"},
        ],
    },
    "P7": {
        "title": "校车上 APLUS 命名 4 panel",
        "prompt_body": """PAGE LAYOUT: 2x2 grid (4 panels of roughly equal size).

PANEL 1 (TOP-LEFT — Songya seated, classmate calling): Songya just sitting down in the front row of a school bus, his face turned slightly toward the aisle. Another Black-American teenage boy classmate (different from Tony) leaning over from the seat behind, grinning and pointing at Songya casually. Olive-brown jacket. School bus interior — vinyl seats, window showing snowy street.
  BALLOONS:
  (a) Right side: ONE LARGE ROUNDED OVAL SPEECH BALLOON, pure white empty interior, approximately 220x130 pixels, tail pointing to classmate's mouth.

PANEL 2 (TOP-RIGHT — laughter close-up): Tight composite shot of three teenage faces (mixed-race / Black / Latino), all laughing or smirking with open mouths, eyes squinted. No identifying details, generic.
  BALLOONS: none.

PANEL 3 (BOTTOM-LEFT — Songya pretending to sleep + thought): Songya leaning back against the school bus seat, eyes closed, faking sleep with a slight frown. Window beside him showing fast-moving blurred snowy South Side street.
  BALLOONS:
  (a) Upper-left: ONE LARGE CLOUD-SHAPED THOUGHT BUBBLE with trailing bubbles, pure white empty interior, approximately 280x150 pixels.

PANEL 4 (BOTTOM-RIGHT — window blur + thought): Tight view of the school bus window with motion-blurred snowy rowhouses streaming past. Songya's faint reflection ghostly in glass.
  BALLOONS:
  (a) Center: ONE MEDIUM CLOUD-SHAPED THOUGHT BUBBLE pure white empty interior, approximately 220x130 pixels.
""",
        "balloons": [
            {"balloon_id": "p1_classmate_aplus", "panel_id": 1, "kind": "dialogue", "speaker": "同学", "text": "早啊，APLUS!"},
            {"balloon_id": "p3_songya_thought_a", "panel_id": 3, "kind": "thought", "speaker": "宋亚（心声）", "text": "就因为数学考个满分，外号就被改成了\"A+\"。"},
            {"balloon_id": "p4_songya_thought_b", "panel_id": 4, "kind": "thought", "speaker": "宋亚（心声）", "text": "华国谁会因为考个满分被孤立?"},
        ],
    },
    "P8": {
        "title": "教室+食堂 4 panel",
        "prompt_body": """PAGE LAYOUT: 2x2 grid (4 panels of roughly equal size).

PANEL 1 (TOP-LEFT — classroom poetry): A middle-aged white male teacher at the front of a classroom holding an open book, lecturing softly. Behind him a chalkboard. In the back-row of seats, a teenage couple (boy + girl, both fully clothed in school clothes, no inappropriate contact, just leaning shoulder-to-shoulder) sit together casually. Other students half-listening.
  BALLOONS:
  (a) Upper-left: ONE SMALL HORIZONTAL WHITE NARRATION RECTANGLE, pure white empty interior, thin black border, approximately 240x65 pixels.

PANEL 2 (TOP-RIGHT — bell ringing + teacher packing): A wall-mounted school bell ringing. In the foreground, the white teacher hastily picks up his briefcase and heads for the door. Other students moving for the exit.
  BALLOONS:
  (a) Center: ONE LARGE JAGGED SFX BLOCK approximately 230x130 pixels, pure white empty interior, slanted diagonally.

PANEL 3 (BOTTOM-LEFT — Malcolm X poster + cafeteria background): A Malcolm X poster on a brick cafeteria wall is the focal point — the poster shows Malcolm X's portrait. In the background, cafeteria tables blur out. An older Black janitor pushing a cart in the distance.
  BALLOONS:
  (a) Upper-left: ONE MEDIUM HORIZONTAL WHITE NARRATION RECTANGLE pure white empty interior, thin black border, approximately 280x80 pixels.

PANEL 4 (BOTTOM-RIGHT — Songya in lunch line + assistant principal at door): Songya holding a lunch tray, waiting in line. At the cafeteria entrance, an older heavyset white man in a suit (the assistant principal) stands with arms crossed watching.
  BALLOONS: none.
""",
        "balloons": [
            {"balloon_id": "p1_narration_poetry", "panel_id": 1, "kind": "narration", "speaker": "旁白", "text": "他正在讲狄金森。", "layout": (2, 2)},
            {"balloon_id": "p2_sfx_bell", "panel_id": 2, "kind": "sfx", "speaker": "拟声", "text": "叮——叮——"},
            {"balloon_id": "p3_narration_malcolm", "panel_id": 3, "kind": "narration", "speaker": "旁白", "text": "Malcolm X，27 年才平反。"},
        ],
    },
    "P9": {
        "title": "数学老师办公室 4 panel",
        "prompt_body": """PAGE LAYOUT: 2x2 grid (4 panels of roughly equal size).

PANEL 1 (TOP-LEFT — math teacher offering deal): An older Black-American female math teacher (warm grandma vibe, glasses on nose, hair in a small bun, knit cardigan, smiling encouragingly) sitting at her cluttered desk filled with papers. She looks up at Songya across the desk.
  BALLOONS:
  (a) Upper-right: ONE EXTRA LARGE ROUNDED OVAL SPEECH BALLOON pure white empty interior approximately 320x180 pixels, tail pointing to teacher's mouth.

PANEL 2 (TOP-RIGHT — Songya surprised reaction): Tight close-up of Songya's face — eyes wide, mouth slightly open in surprise, eyebrows raised — match face anchor reference. Light caramel mixed-race skin, short curly black hair, slightly Asian almond eyes. Office-poster background blurred.
  BALLOONS:
  (a) Center: ONE SMALL ROUNDED OVAL SPEECH BALLOON pure white empty interior approximately 160x90 pixels, tail to Songya's mouth.

PANEL 3 (BOTTOM-LEFT — thought + narration overlay): Songya's eyes lighting up calculating, profile shot.
  BALLOONS:
  (a) Right side: ONE MEDIUM HORIZONTAL WHITE NARRATION RECTANGLE pure white empty interior thin black border approximately 240x80 pixels.

PANEL 4 (BOTTOM-RIGHT — Songya enthusiastic response): Songya nodding firmly, determined look — match face anchor.
  BALLOONS:
  (a) Upper-right: ONE MEDIUM ROUNDED OVAL SPEECH BALLOON pure white empty interior approximately 230x100 pixels, tail to Songya's mouth.
""",
        "balloons": [
            {"balloon_id": "p1_teacher_offer", "panel_id": 1, "kind": "dialogue", "speaker": "数学老师", "text": "给个建议——如果你能通过我的九年级基础课程考试，我就把你转到数学高级班里去。"},
            {"balloon_id": "p2_songya_question", "panel_id": 2, "kind": "dialogue", "speaker": "宋亚", "text": "高级班?"},
            {"balloon_id": "p3_narration_credits", "panel_id": 3, "kind": "narration", "speaker": "旁白", "text": "高级班 = 更多学分。"},
            {"balloon_id": "p4_songya_yes", "panel_id": 4, "kind": "dialogue", "speaker": "宋亚", "text": "好的，我会尽力!"},
        ],
    },
    "P10": {
        "title": "走廊撞见音乐老师 4 panel",
        "prompt_body": """PAGE LAYOUT: 2x2 grid (4 panels of roughly equal size).

PANEL 1 (TOP-LEFT — music teacher accosting): A white middle-aged female music teacher, crisp short bob haircut, sharp-eyed, slightly stern expression, in a high school hallway with lockers behind. She points at Songya off-panel.
  BALLOONS:
  (a) Upper-right: ONE EXTRA LARGE ROUNDED OVAL SPEECH BALLOON pure white empty interior approximately 310x180 pixels, tail pointing to music teacher's mouth.

PANEL 2 (TOP-RIGHT — Songya forced fake smile): Tight close-up of Songya's face — eyes wide in dread, forced strained smile, sweat drops on brow. Match face anchor.
  BALLOONS:
  (a) Center: ONE MEDIUM CLOUD-SHAPED THOUGHT BUBBLE pure white empty interior approximately 220x110 pixels.

PANEL 3 (BOTTOM-LEFT — music teacher continuing): The music teacher again, slightly more amused now, gesturing dismissively. Same hallway background.
  BALLOONS:
  (a) Lower-right: ONE LARGE ROUNDED OVAL SPEECH BALLOON pure white empty interior approximately 270x140 pixels, tail to music teacher's mouth.

PANEL 4 (BOTTOM-RIGHT — Songya holding a tiny triangle with sad face): Songya holding a tiny silver triangle (the percussion instrument) with the small striking rod, with a comically tragic expression — slumped shoulders, sad eyes. Music room background out of focus.
  BALLOONS:
  (a) Upper-left: ONE SMALL ROUNDED OVAL SPEECH BALLOON pure white empty interior approximately 150x90 pixels, tail to Songya's mouth.
  (b) Lower-right: ONE SMALL ROUNDED OVAL SPEECH BALLOON pure white empty interior approximately 140x90 pixels, tail pointing toward an off-panel direction (the music teacher).
""",
        "balloons": [
            {"balloon_id": "p1_music_complaint", "panel_id": 1, "kind": "dialogue", "speaker": "音乐老师", "text": "亚历山大，是吧? 上周，你的小号在排练中数次出现明显的错误!"},
            {"balloon_id": "p2_songya_thought_dread", "panel_id": 2, "kind": "thought", "speaker": "宋亚（心声）", "text": "完了。"},
            {"balloon_id": "p3_music_demote", "panel_id": 3, "kind": "dialogue", "speaker": "音乐老师", "text": "下次合练你别吹小号了，撸铁去吧!"},
            {"balloon_id": "p4_songya_what", "panel_id": 4, "kind": "dialogue", "speaker": "宋亚", "text": "撸什么?"},
            {"balloon_id": "p4_music_triangle", "panel_id": 4, "kind": "dialogue", "speaker": "音乐老师", "text": "三角铁!"},
        ],
    },
    "P12": {
        "title": "篮球场初见小洛瑞 3 panel",
        "prompt_body": """PAGE LAYOUT: Three vertically stacked horizontal panels of roughly equal height (each about 33% of page).

PANEL 1 (TOP — Lil Lorry warming up): A small public basketball court enclosed by chain-link fence in a 1990 Chicago neighborhood, slightly run-down. LIL LORRY (16-ish Black-American boy, thin frame, baby face, neat dreadlocks, big over-ear headphones, denim shirt) casually bouncing a basketball at half-court with one hand, relaxed pose. Sunset late afternoon golden-warm light. Distant tenements behind.
  BALLOONS: none.

PANEL 2 (MIDDLE — fist bump intro fail): Medium shot of four boys at center court — LIL LORRY, TONY, SILENCER (broad-shouldered stern Black bodyguard type), and SONGYA (match face anchor). They are mid-greeting with elaborate fist-bump handshake choreography. Songya's fist is awkwardly held in mid-air, missing Lil Lorry's pattern. Lil Lorry's hand has already moved on. Songya looks confused.
  BALLOONS: none.

PANEL 3 (BOTTOM — Lil Lorry pats Songya): Medium close-up of Lil Lorry leaning toward Songya, his hand on Songya's shoulder, suppressing a laugh with a warm slight smile. Songya looks slightly embarrassed but relieved.
  BALLOONS:
  (a) Upper-right: ONE MEDIUM ROUNDED OVAL SPEECH BALLOON pure white empty interior approximately 240x110 pixels, tail pointing to Lil Lorry's mouth.
""",
        "balloons": [
            {"balloon_id": "p3_lorry_reassure", "panel_id": 3, "kind": "dialogue", "speaker": "小洛瑞", "text": "算了，不用在意那些。"},
        ],
    },
    "P13": {
        "title": "半场对位被虐 4 panel",
        "prompt_body": """PAGE LAYOUT: 2x2 grid (4 panels of roughly equal size).

PANEL 1 (TOP-LEFT — Lil Lorry crossover): LIL LORRY (thin baby-faced Black boy with neat dreadlocks and headphones around neck, denim shirt) doing a behind-the-back dribble crossover move on a half-court, SONGYA defending him awkwardly off-balance. Motion lines on Lorry's body. Sunset afternoon light.
  BALLOONS: none.

PANEL 2 (TOP-RIGHT — Songya falls, Lorry layup with tongue-out): SONGYA on the court ground in a sitting fall, looking up. LIL LORRY mid-layup at the basket with his tongue stuck out Michael Jordan style. Comic motion lines.
  BALLOONS: none.

PANEL 3 (BOTTOM-LEFT — three strangers approach): Three Black-American teenage boys (different from Lorry, more rough-looking, baggier clothes) walking onto the court from the side, the front one gesturing toward Lorry's group with a half-friendly half-challenging expression.
  BALLOONS:
  (a) Upper-right: ONE MEDIUM ROUNDED OVAL SPEECH BALLOON pure white empty interior approximately 200x110 pixels, tail pointing to front stranger's mouth.

PANEL 4 (BOTTOM-RIGHT — Lorry accepts, Songya and Tony sit out): Wider shot from the side: LIL LORRY nodding to the strangers, SONGYA and TONY stepping off court to a low concrete wall to sit, waterbottles in hand. Mild expressions.
  BALLOONS: none.
""",
        "balloons": [
            {"balloon_id": "p3_stranger_challenge", "panel_id": 3, "kind": "dialogue", "speaker": "陌生人", "text": "我们来?", "layout": (2, 2)},
        ],
    },
    "P14": {
        "title": "拔枪事件 大格 + 2 小格",
        "prompt_body": """PAGE LAYOUT: Top large panel ~60% of page height. Bottom row 2 panels side-by-side ~40% of page height.

PANEL 1 (TOP LARGE — escalating scuffle): A chaotic basketball-court scene depicted with overlapping action moments composited together (or as a single dense moment): LIL LORRY just stood up after being shoulder-checked to the ground by a rough-looking Black-American teen (the antagonist), confronting him; both pushing chest-to-chest; the antagonist's two companions stepping behind; in the upper background, TONY sprinting back from the parked Toyota AE86, his face determined, with a faint dark shape concealed behind his back. Motion lines on Tony's running. Late afternoon hard sunlight.
  BALLOONS: none.

PANEL 2 (BOTTOM-LEFT — Tony lifts shirt to reveal gun): Tight medium shot — TONY now standing in front of Lil Lorry as a shield, his hand pulling up the hem of his t-shirt to reveal a black pistol grip tucked into his waistband. Sharp shadow contrast. The gun grip dominates the visual focus.
  BALLOONS: none.

PANEL 3 (BOTTOM-RIGHT — Tony's face close-up, mid-shout): Extreme close-up of TONY's face, eyes narrow and predatory like Mike Tyson, mouth open shouting. The antagonist's blurred shoulder is in foreground.
  BALLOONS:
  (a) Center: ONE EXTRA LARGE JAGGED CLOUD-BURST SHOUT BALLOON with smooth white inner oval and OUTER jagged spike border only (no visible inner outline). Pure white empty interior approximately 320x180 pixels. Tail pointing toward Tony's mouth.
""",
        "balloons": [
            {"balloon_id": "p3_tony_threat", "panel_id": 4, "kind": "shout", "speaker": "托尼", "text": "你们想玩多大? NGer! em? 你们想玩多大?", "layout": (2, 2)},
        ],
    },
    "P15": {
        "title": "整页大格 · 7 秒寂静 splash",
        "prompt_body": """PAGE LAYOUT: ONE single full-page splash panel.

PANEL 1 (FULL PAGE SPLASH — frozen moment of 7-second silence): A frozen tableau on the basketball court: all the boys (LIL LORRY, TONY with his shirt-hem still raised showing the gun grip, SONGYA in the background, SILENCER nearby, the three antagonists) are stopped in mid-pose. The atmosphere reads as time-stopped silence. A muted cold blue-violet color wash dominates the whole page. Light snow-flake-like dot pattern overlay across the entire image gives a "static / frozen / silence" effect.

In the upper-LEFT corner, a small inset rectangular cutout shows an extreme close-up of the antagonist's face — a single vein visibly throbbing on his temple, his eyeball bloodshot red — this small inset rendered with normal warm color (no blue wash) for contrast.

BALLOONS:
  (a) Upper-right area: ONE LARGE HORIZONTAL WHITE NARRATION RECTANGLE with thin black border, pure white empty interior, approximately 400x100 pixels.
""",
        "balloons": [
            {"balloon_id": "p1_narration_count", "panel_id": 1, "kind": "narration", "speaker": "旁白", "text": "1, 2, 3, 4, 5, 6, 7。", "layout": (1, 1)},
        ],
    },
    "P11": {
        "title": "上车去打球 3 panel · 丰田86雄鹰",
        "prompt_body": """PAGE LAYOUT: Three vertically stacked horizontal panels of varied heights. Panel 1 takes top ~45% of page (large wide), Panel 2 takes middle ~30%, Panel 3 takes bottom ~25%.

PANEL 1 (TOP WIDE — Toyota 86 stopped at school gate, Tony + Songya boarding): A 1980s-style Toyota Trueno AE86 sports coupe (red and white two-tone, Eagle/Hawk styling) parked at the curb in front of a high school gate building. Tony in the foreground reaching for the passenger door, Songya behind him. A glimpse of the driver — SILENCER — through the windshield. Cold winter afternoon light.
  BALLOONS: none.

PANEL 2 (MIDDLE WIDE — interior of car, three in seats): Wide interior shot of the car: SILENCER driving (front, stern profile), TONY in the front passenger seat slumped relaxed, SONGYA in the back seat with athletic gear and football pads piled around him on the back bench. View through the rear windshield in background.
  BALLOONS: none.

PANEL 3 (BOTTOM WIDE — Silencer turns back, throat-cut gesture): Tight medium shot from passenger angle: SILENCER half-turned looking over his shoulder from the driver's seat. His right hand is raised drawing a finger across his own throat in a "throat-cut" gesture, lips pressed flat. His eyes are intense, slightly wet.
  BALLOONS:
  (a) Upper-right: ONE MEDIUM CLOUD-SHAPED THOUGHT BUBBLE pure white empty interior approximately 240x110 pixels.
""",
        "balloons": [
            # P11 layout is 3 vertical → panel_id 1,2,3 map directly in 3x1 grid
            {"balloon_id": "p3_songya_thought_cut", "panel_id": 3, "kind": "thought", "speaker": "宋亚（心声）", "text": "橄榄球队的护具。可季节都过了。"},
        ],
    },
    "P6": {
        "title": "校车站 ET 出场 4 panel",
        "prompt_body": """PAGE LAYOUT: 2x2 grid (4 panels of roughly equal size).

PANEL 1 (TOP-LEFT — bus stop wide shot with hanging teens): Wide shot of a graffitied bus stop bench area. Three or four teenage boys leaning around chatting, bare leafless trees behind, gray sidewalk. Cold winter morning light.
  BALLOONS: none in this panel.

PANEL 2 (TOP-RIGHT — ET leans in conspiratorially): ET (16-ish teenager, baseball cap pulled low, a hint of brightly patterned flower bandana visible under brim — careful close-up, do not show full bandana) leaning toward Tony grinning. Tony slightly turned, polite smile.
  BALLOONS:
  (a) Lower-right: ONE MEDIUM ROUNDED OVAL SPEECH BALLOON, pure white empty interior, approximately 240x130 pixels, tail to ET's mouth.

PANEL 3 (BOTTOM-LEFT — Tony delivers Emily to little kid bus + fist bump): Medium-wide shot of Tony bending down handing Emily into a yellow elementary school bus door. ET stepping back, the two boys mid fist-bump, Tony walking aside to chat.
  BALLOONS: none in this panel.

PANEL 4 (BOTTOM-RIGHT — close-up of ET's hat brim hinting at bandana + Songya's inner thought): Tight close-up of ET's lowered head from below — only the brim of his baseball cap visible with the bright flower-bandana fabric peeking under. Camera tilted about 10 degrees.
  BALLOONS:
  (a) Upper-left: ONE MEDIUM CLOUD-SHAPED THOUGHT BUBBLE pure white empty interior, approximately 200x110 pixels.
""",
        "balloons": [
            {"balloon_id": "p2_et_question", "panel_id": 2, "kind": "dialogue", "speaker": "ET", "text": "yooo, 托尼，你现在跟小洛瑞混了?"},
            {"balloon_id": "p4_songya_bandana_thought", "panel_id": 4, "kind": "thought", "speaker": "宋亚（心声）", "text": "花头巾，不是能随便戴上的东西。"},
        ],
    },
}
