---
name: antigravity-draw
version: 2.0.0
description: AntiGravity 與 OpenAI gpt-image-2.5-sunburst 生圖技能。當使用者說「openai 生圖」、「生圖」、「畫圖」、「產生圖片」時載入。
user-invocable: true
changelog:
  - version: 1.0.0
    date: 2026-06-07
    note: 初始版本，提供基礎生圖指引與提示詞結構化模版。
  - version: 2.0.0
    date: 2026-09-12
    note: 升級為 AntiGravity 雙軌版。整合路線 A（Google 內建生圖）與路線 B（OpenAI gpt-image-2 腳本 draw.py），簡化觸發詞為唯一專屬指令「openai 生圖」，支援自動開啟 Finder 預覽與參數引導。
  - version: 2.1.0
    date: 2026-09-20
    note: 升級 OpenAI 模型為 gpt-image-2.5-sunburst，預設品質提升為 medium。
---

# 🎨 生圖技能與 OpenAI 生圖（AntiGravity 雙軌版）

## 兩大生圖路線

| 路線 | 模式 | 觸發方式 / 特點 |
|---|---|---|
| **路線 A：內建生圖** | 免費 / 零設定 | 說「生圖」、「畫圖」時使用 AntiGravity 內建 `generate_image` 工具生成。 |
| **路線 B：OpenAI 生圖 (gpt-image-2.5-sunburst)** | OpenAI API 專屬 | 說「**openai 生圖**」或指名路線 B 時觸發，呼叫本地 `draw.py` 執行。 |

---

## 🧙‍♂️ 路線 B：OpenAI 生圖運作規範

### 1. 觸發詞與互動模式
- **唯一專屬觸發詞**：`openai 生圖`
- **情境一（直接帶需求）**：若使用者說「`openai 生圖：[提示詞/畫面描述]`」，直接解析參數並呼叫 `draw.py` 生圖。
- **情境二（僅啟動精靈）**：若使用者僅輸入「`openai 生圖`」，將主動以親切引導的方式詢問使用者以下要素：
  1. **畫面主題與內容**（你想畫什麼？）
  2. **尺寸比例**（預設 1:1 方形、16:9 橫幅、9:16 直式）
  3. **風格偏好**（扁平插畫、極簡科技、寫實攝影、水彩手繪等）
  4. **圖片用途或檔名**（例如投影片插圖、封面海報）

---

### 2. 腳本呼叫方式

#### 腳本位置
- 本地專案：`.agents/skills/antigravity-draw/draw.py`
- 全域路徑：`~/.claude/skills/draw/draw.py`

#### 執行指令範例
```bash
# 基本生圖（預設 medium 品質，存至 ./generated/）
python3 .agents/skills/antigravity-draw/draw.py "一隻穿西裝打領帶的龍蝦，扁平商務插畫風格" --name lobster

# 16:9 橫幅 (1536x1024)
python3 .agents/skills/antigravity-draw/draw.py "高科技會議室，未來感藍白光影" --size 1536x1024 --name meeting_room

# 直式 9:16 (1024x1536)
python3 .agents/skills/antigravity-draw/draw.py "手機桌布風格的日落海岸" --size 1024x1536 --name sunset

# 圖片修改模式 (--edit)
python3 .agents/skills/antigravity-draw/draw.py "將背景替換為星空" --edit ./generated/lobster_20260912.png --name lobster_space
```

---

### 3. 參數說明
- `prompt`（必填）：圖片描述
- `--size`：`1024x1024`（預設，正方形）/ `1536x1024`（橫幅）/ `1024x1536`（直式）
- `--quality`：`medium`（預設，平衡高畫質）/ `low` / `high` / `xhigh` / `max`
- `--n`：張數（預設 1，最多 8）
- `--name`：輸出的檔名前綴
- `--outdir`：指定輸出目錄（預設存至 `./slides/generated/` 或 `./generated/`）
- `--edit`：現有圖片路徑（改圖模式）
- `--mask`：局部修改遮罩圖片路徑

### 4. 金鑰設定
腳本會自動依序讀取：
1. Shell 環境變數 `OPENAI_API_KEY`
2. 當前目錄 `.env`
3. 使用者家目錄 `~/.openai.env`
