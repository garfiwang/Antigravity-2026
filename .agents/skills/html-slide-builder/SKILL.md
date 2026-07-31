---
name: html-slide-builder
description: |
  給定任何教材（文字、課程大綱、PDF、講義、口述主題），自動生成適合 100 吋大螢幕投放、對 70 歲樂齡學員極致清晰的 Reveal.js HTML 互動簡報，並部署至 GitHub Pages。

  自動處理四大視覺/互動強化：
  1. AI 生成高對比背景底圖（draw 技能，data-background-image，保持低透明度以避干擾）
  2. 巨型扁平化圖標（draw 技能 + PIL 裁切去背，放大至 96-120px）
  3. 樂齡友善 Firebase 即時互動元件（大字版文字雲、大按鈕單選投票）
  4. 滑桿視覺化演示（clip-path 揭露，大控制項前後對比）

  當使用者說「幫我做 HTML 簡報」「把這份教材轉成互動簡報」「做 Reveal.js 簡報」「做成投影片」「做一份課程簡報」，或提供教材並要求轉成簡報格式時，務必使用此 Skill。即使使用者未明確說「互動」或「HTML」，只要目的是從教材產出可展示的簡報，也應觸發此 Skill。
---

# HTML 智慧簡報生成器 (100吋大螢幕 / 70歲樂齡極致高可讀性版)

教材 → 分析 → 確認大綱 → 生成 Reveal.js 簡報 → 強化（巨型底圖/圖標/互動/視覺化）→ GitHub Pages 部署

---

## 🎯 樂齡與大螢幕投放四大原則 (Senior Large-Screen Rules)

1. **字體巨大化 (Huge Typography)**
   - `h1` 主標題：`2.8em` – `3.2em`
   - `h2` 頁次標題：`2.1em` – `2.4em`
   - `h3` / 卡片標題：`1.0em` – `1.4em`
   - 內文與說明：`0.75em` – `0.9em`（**絕對禁止**使用 0.5em 或更小的微字）
   - 字重（Font Weight）：標題 800 (Extra Bold)、內文 600 (Semi-Bold)，行高 `1.6–1.8`。

2. **極高對比與純淨背景 (Ultra High Contrast)**
   - 主文字：純白 `#ffffff`，搭配高飽和鮮明強調色（`#ff6b35` 亮橘、`#40c4ff` 高對比藍、`#ffd740` 明亮黃）。
   - **嚴禁用灰字**（避免使用 `#888` / `#aaa` 等低對比顏色；次要文字最少需 `#e0e0e0`）。
   - 背景採純淨極深色 (`#0a0d14`)，底圖透明度降至 `0.10`–`0.15`，絕對不搶戲、不干擾文字識讀。

3. **單頁資訊極簡化 (Minimalist Single-Slide Content)**
   - **每頁最多 1–3 個核心重點/卡片**。若教材超過 3 個觀點，務必拆分為多頁。
   - 拒絕密集排版與長篇大論，每張卡片標題大、文字精簡至 1-2 句話。

4. **視覺元件巨型化 (Giant Visual Elements)**
   - 圖標 (Icons) 放大至 `96px` ~ `120px`（搭配亮藍/亮橘發光陰影）。
   - 互動按鈕、輸入框、滑桿一律放大，便於台下遠觀與手機輸入。

---

## 0. 讀取教材

接受任何形式的輸入：

- **文字 / Markdown**：直接分析
- **PDF**：用 Read 工具讀取（若有多頁先讀摘要頁）
- **口述主題**：自行根據標準教學邏輯設計（引言→概念→範例→互動→結論）

若教材資訊不足，不要詢問，直接用教學慣例補充。

---

## 1. 分析大綱，等使用者確認

分析完畢後輸出大綱表格，**等使用者確認後才繼續**：

```
## 📋 簡報大綱草稿（共 N 頁 - 100吋大螢幕大字版）

| 頁碼 | 標題 | 內容摘要 (單頁最多 3 重點) | 功能標記 |
|------|------|--------------------------|----------|
| 1    | 封面 | 課程名稱、講師 | [BG] |
| 2    | 破冰提問 | 大字版文字雲收集學員想法 | [INTERACT:wordcloud] |
| 3    | 三大核心 | 並列說明三個重點 (圖標 96px) | [ICON] |
| 4    | 前後對比 | A 方案 vs B 方案大字對照 | [VIZ] |
...

**功能標記說明**
- [BG] 暗色沉穩底圖（draw 技能，透明度 0.10-0.15）
- [ICON] 巨型扁平圖標（draw + PIL 去背，尺寸 96px~120px）
- [INTERACT:wordcloud] 大字 Firebase 即時文字雲
- [INTERACT:poll] 大字 Firebase 單選投票
- [VIZ] 滑桿視覺化演示（clip-path 大控制項）

請確認大綱，或說明要調整的地方。
```

### 功能標記的決策原則

| 標記 | 觸發條件 | 每份簡報目標數量 |
|------|----------|-----------------|
| [BG] | 封面、封底、章節轉換、高衝擊結論 | 3–5 頁 |
| [ICON] | 頁面有 2–3 個並列項目（絕對不超過 3 個） | 1–3 頁 |
| [INTERACT:wordcloud] | 開場破冰、先備知識調查、課尾反思 | 1 頁（通常第 2 頁） |
| [INTERACT:poll] | 概念確認、意見調查、前測/後測 | 0–1 頁 |
| [VIZ] | 「前後對比」「格式轉換」「A 到 B 的演進」 | 0–1 頁 |

---

## 2. 建立專案目錄與基礎 HTML

使用者確認後：

1. 建立專案目錄：`<當前工作目錄>/<簡報英文短名>/`
2. 建立 `images/` 子目錄
3. 生成 `index.html`（完整 Reveal.js 骨架）

讀取 `references/reveal-template.md` 獲得：1920x1080 完整 CSS 變數、樂齡大字元件樣式、Reveal.js 初始化程式碼。

**命名規則：**
- 專案目錄：kebab-case 英文（`ai-course`、`senior-health`）
- Firestore 集合：`<slug>_wordcloud`、`<slug>_poll`（避免不同簡報資料混用）

**高對比樂齡調色盤（所有簡報統一使用）：**
```
--accent:     #ff6b35   醒目亮橘（主強調）
--accent2:    #40c4ff   高對比天空藍（次標題與亮點）
--success:    #69f0ae   明亮翡翠綠（正面標記）
--warn:       #ffd740   鮮豔琥珀黃（提示/數字）
--bg-dark:    #0a0d14   超深純淨背景
--text-main:  #ffffff   滿分純白文字
--text-sub:   #e0e0e0   高可讀副文字 (絕不使用灰暗色)
```

---

## 3. 生成背景底圖 [BG]

對每個 [BG] 頁面呼叫 draw 技能或生圖工具，可平行執行：

### 方式 A（Antigravity 環境，推薦）：
直接使用內建的 `generate_image` 工具生成：
- `Prompt`: `<底圖 prompt>`
- `ImageName`: `<slide-slug>`
- 生成完成後，將產生的圖片複製/移動到 `<專案目錄>/images/` 資料夾中。

### 方式 B（Claude Code 環境 或 需要 API）：
```bash
python "/Users/garfiwang/.claude/skills/draw/draw.py" \
  "<底圖 prompt>" \
  --size 1536x1024 --quality low \
  --name <slide-slug> \
  --outdir "<專案目錄>/images"
```

**底圖 Prompt 設計原則：**
- 極深暗色系（ultra dark navy, deep space background, #0a0d14）
- 完全無文字
- 與主題相關但極致簡潔抽象（避開雜亂線條與微小顆粒）
- 高發光效果以襯托前景文字
- 例：樂齡課程封面 → `"deep navy space background, minimal glowing soft light trails, dark cinematic ambient art, no text"`

在 HTML section 加上：
```html
<section data-background-image="images/<slug>.png"
         data-background-opacity="0.12"
         data-background-size="cover">
```

透明度建議：封面 0.15；一般頁 0.10–0.12（堅守背景不干擾文字原則）。

---

## 4. 圖標系統 [ICON]

### 4-1 生成圖標總表

直接使用內建的 `generate_image` 工具生成：
- `Prompt`: `A clean icon sheet with exactly N flat neon icons in a single horizontal row on pure dark navy (#0a0d14) background. [逐一描述每個圖標，從左到右]. Each icon extremely large, bold, centered in equal column, no text.`
- `ImageName`: `icon_sheet`
- 將產生的圖片複製到 `<專案目錄>/images/`。

### 4-2 裁切 + 去背

裁切並調高解析度至 `384x384`（以確保在 100 吋大幕上顯現極度清晰）：

```python
from PIL import Image
from pathlib import Path

img = Image.open("images/icon_sheet.png").convert("RGBA")
w, h = img.size
n = <圖標數量>
icons = ["icon_a", "icon_b", ...]  # 對應名稱

for i, name in enumerate(icons):
    x0 = i * (w // n)
    x1 = (i + 1) * (w // n) if i < n-1 else w
    col_w = x1 - x0
    sq = min(col_w, h)
    cx, cy = x0 + col_w // 2, h // 2
    crop = img.crop((cx-sq//2, cy-sq//2, cx+sq//2, cy+sq//2))
    crop = crop.resize((384, 384), Image.LANCZOS)
    crop.save(f"images/{name}.png")
```

然後執行去背（`scripts/remove_bg.py`）。

### 4-3 嵌入 HTML

- 用 `<img src="images/icon_name.png">` 取代 emoji
- 圖標容器與尺寸：圖片高寬設定為 `96px` ~ `120px`
- adv-card 統一用 `border-top: 6px solid var(--accent2)`
- 圖標 img 加 `filter: drop-shadow(0 0 16px rgba(64,196,255,0.8))`

---

## 5. 樂齡大字互動元件 [INTERACT]

詳見 `references/firebase-config.md`，包含已針對大螢幕優化的文字雲和投票 HTML 程式碼片段。

**通用原則：**
- 互動 section 加 `id="slide-<slug>"`
- 使用 `Reveal.on('slidechanged', e => { if (e.currentSlide?.id === '...') { /* 重繪 */ }})`
- 輸入框與按鈕字體放大至 `18px` – `22px`
- 文字雲權重字體最小 `32px`，最大 `110px`

---

## 6. 視覺化演示 [VIZ]

clip-path 滑桿揭露效果，適合「前後對比」「A→B 演進」。

```html
<div style="position:relative; height:440px; border-radius:16px; overflow:hidden; border:2px solid rgba(255,255,255,0.2);">
  <div id="viz-before" style="position:absolute;inset:0;..."></div>
  <div id="viz-after" style="position:absolute;inset:0;clip-path:inset(0 100% 0 0);"></div>
  <div id="viz-divider" style="position:absolute;top:0;left:0;width:6px;height:100%;
    background:linear-gradient(to bottom,transparent,#40c4ff,transparent);
    box-shadow:0 0 16px #40c4ff;pointer-events:none;"></div>
</div>
<input id="viz-slider" type="range" min="0" max="100" value="0" style="width:100%; height:20px; margin-top:16px;">
<script>
document.getElementById('viz-slider').addEventListener('input', function() {
  const v = +this.value;
  document.getElementById('viz-after').style.clipPath = `inset(0 ${100-v}% 0 0)`;
  document.getElementById('viz-divider').style.left = v + '%';
});
</script>
```

---

## 7. 部署到 GitHub Pages

```bash
cd "<專案目錄>"
git init
git config user.email "<你的 GitHub email>"
git config user.name "<你的 GitHub 帳號>"
git add .
git commit -m "初始化 100吋大螢幕大字版簡報：<簡報名稱>"
gh repo create <帳號>/<repo-name> --public --source=. --push \
  --description "<簡報一句話描述>"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
gh api repos/<帳號>/<repo-name>/pages \
  --method POST -f "source[branch]=$BRANCH" -f "source[path]=/"
```

---

## 參考資源

| 檔案 | 用途 |
|------|------|
| `references/reveal-template.md` | 1920x1080 樂齡大字版 Reveal.js HTML 完整模板、CSS 元件庫 |
| `references/firebase-config.md` | 大字版文字雲、投票完整程式碼片段 |
| `scripts/remove_bg.py` | PIL 圖標去背腳本 |
