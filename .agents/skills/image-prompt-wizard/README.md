# 🎨 Image Prompt Wizard｜AI 圖片 Prompt 生成嚮導

> 版本：v1.0.0｜適用平台：Midjourney、DALL-E 3、Stable Diffusion、Firefly、Leonardo AI

透過對話引導，幫你產出高品質的 AI 繪圖英文 Prompt，無需任何繪圖專業知識。

---

## 功能亮點

- **三種模式**：快速（3～4 題）/ 深度（6～8 題）/ 一句話生圖
- **結構化 Prompt**：主體 → 風格 → 色調 → 構圖 → 光線 → 品質強化詞
- **雙語輸出**：英文 Prompt ＋ 中文設計邏輯說明
- **平台通用**：輸出格式相容所有主流 AI 繪圖工具

---

## 安裝方式

```bash
# 在 Claude Code 中安裝此技能
claude skills add garfiwang/claude-skills --path 01-content-creation/image-prompt-wizard
```

安裝後，在 Claude Code 對話中輸入以下任一關鍵字即可觸發：

> `圖片提示詞` / `image prompt` / `生成圖片 Prompt` / `啟動 Prompt 生成器` / `幫我生圖片提示詞`

---

## 使用流程

### 模式 1：🚀 快速模式（推薦新手）

依序回答 3～4 個引導問題：

| 問題 | 範例答案 |
|---|---|
| 圖片用途 | FB 貼文封面 |
| 主角/場景 | 一位穿西裝的中年男性，站在辦公室落地窗前 |
| 視覺風格 | 電影感、略帶戲劇性光線 |
| 特殊需求（可跳過）| 需要留白空間放文字 |

### 模式 2：🔍 深度模式（精準掌控）

額外詢問：色彩氛圍、構圖視角、光線情緒、參考風格等共 6～8 題。

### 模式 3：⚡ 一句話生圖

直接輸入一句話，AI 自動補完所有細節：

```
一杯咖啡放在秋天的木質書桌上，窗外有金黃落葉
```

---

## 輸出範例

```
📸 英文 Prompt

A middle-aged professional man in a navy suit standing by a floor-to-ceiling office window,
city skyline at dusk visible behind him, cinematic lighting with dramatic side shadows,
warm golden tones, shallow depth of field, leaving negative space on the left for text overlay,
photorealistic, DSLR quality, sharp focus, 8K resolution --ar 16:9

---

📖 中文說明

用途：適合金融/保險/信託主題的 FB 貼文封面
主要關鍵詞：cinematic lighting（電影感光線）、negative space（留白構圖）、shallow depth of field（淺景深）
建議平台：Midjourney v6 / DALL-E 3 / Stable Diffusion XL（通用）
小提醒：Midjourney 建議加上 --ar 16:9 取得橫幅比例
```

---

## Prompt 結構說明

此技能生成的 Prompt 遵循以下 8 層結構：

```
[主體] + [動作/狀態] + [場景背景] + [視覺風格] + [色彩光線] + [構圖視角] + [品質強化詞] + [平台參數]
```

### 品質強化詞庫

| 風格類型 | 強化詞 |
|---|---|
| 寫實攝影 | `photorealistic, DSLR quality, sharp focus, 8K resolution` |
| 插畫/藝術 | `digital illustration, concept art, trending on ArtStation` |
| 電影感 | `cinematic, film grain, anamorphic lens, dramatic lighting` |
| 極簡 | `minimalist, clean composition, negative space, flat design` |
| 3D 渲染 | `3D render, octane render, volumetric lighting, hyper-realistic` |

---

## 適合哪些人使用？

- 社群媒體經營者（需要大量封面圖）
- 講師、顧問（簡報配圖需求）
- 個人品牌創作者（形象照替代方案）
- 行銷人員（廣告素材快速原型）
- 對 AI 繪圖有興趣但不知道怎麼下指令的新手

---

## 關於作者

**Rich Wang**｜問大師家族辦公室 創辦人

- 個人 FB：https://www.facebook.com/garfiwang
- 問大師 FB：https://www.facebook.com/profile.php?id=61579988407598

---

## Changelog

| 版本 | 日期 | 說明 |
|---|---|---|
| v1.0.0 | 2026-06-12 | 初始版本：三種模式（快速/深度/一句話生圖），8 層 Prompt 結構，雙語輸出 |

*Last updated: 2026-06-12*
