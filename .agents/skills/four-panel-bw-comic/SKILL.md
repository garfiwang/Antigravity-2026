---
name: four-panel-bw-comic
version: 2.1.0
description: 專門生成「2x2 四格故事/漫畫圖片（預設 16:9 橫幅，支援多種風格選擇）」的技能。當使用者提到「這是我的腳本，請幫我生成四格漫畫」、「生成四格黑白漫畫風格」、「四格漫畫」、「四格梗圖」或提供腳本要求此風格時載入。本技能嚴格遵守「風格互動選擇」、「故事依據腳本」與「生圖前先提供四格分鏡表供確認」三大原則。
user-invocable: true
changelog:
  - version: 1.0.0
    date: 2026-08-27
    note: 初始版本。定義 2x2 懷舊黑白寫實底片電影感視覺風格、起承轉合四步反轉敘事結構與分鏡表確認流程。
  - version: 1.1.0
    date: 2026-08-27
    note: 強化 Prompt 生成邏輯，要求 90 年代東亞寫實底片攝影感、Kodak Tri-X 35mm 顆粒、明暗對比（Chiaroscuro）與抓拍張力微表情。
  - version: 1.2.0
    date: 2026-08-27
    note: 設定 16:9 寬螢幕橫幅為預設畫面比例。
  - version: 2.0.0
    date: 2026-08-27
    note: 完全對齊樟腦丸梗圖參考圖，將色調調整為「暖棕復古單色底片色調（Warm Sepia-toned Monochrome）」。
  - version: 2.1.0
    date: 2026-08-27
    note: 新增風格選擇引導機制。收到觸發指令後，第一步先詢問風格選擇（1. 暖棕懷舊底片風格 / 2. 日系可愛漫畫風格 / 3. 自行輸入），確認風格後再輸出分鏡表。
---

# 🎬 四格故事漫畫生成技能 (four-panel-bw-comic)

## 技能定位與三大鐵則

本技能專注於將使用者提供的故事腳本轉換為 **2x2 四格拼盤圖片（16:9 寬螢幕）**。

### 📌 三大鐵則：
1. **第一步先詢問風格**：收到觸發指令後，必須先列出風格選項請使用者選擇，確認風格後才展開分鏡設計。
2. **嚴格依據腳本**：圖片情節、人物動作與反轉細節必須忠實還原使用者提供的腳本內容。
3. **生圖前必須分鏡確認**：輸出分鏡表後**絕對不可同時呼叫生圖工具**，必須等待使用者確認同意後才可執行生圖。

---

## 標準三步驟執行流程

### 🔹 第一步：風格詢問引導（觸發後立即詢問）

當使用者提供腳本並觸發技能（例如說出「這是我的腳本，請幫我生成四格漫畫」）時，**立即回應以下選單，不要做其他事**：

```markdown
收到您的故事腳本了！🎨
請選擇您要的圖片風格：

1. **暖棕懷舊底片風格**（預設，對照樟腦丸梗圖質感，35mm 顆粒、高對比寫實光影與微表情）
2. **日系可愛漫畫風格**（溫暖手繪感、可愛 Q 版/二次元插畫、柔和色彩）
3. **自行輸入**（請直接回覆您想要的風格描述，例如：水彩插畫、美式美漫、極簡扁平...）

👉 請直接回覆數字 (1 / 2) 或輸入您指定的風格！
```

---

### 🔹 第二步：輸出【四格分鏡確認表】（暫停等候確認）

收到使用者選擇的風格後，根據腳本與該風格設計分鏡，並輸出以下分鏡表：

```markdown
### 📋 四格漫畫分鏡表

* **故事主題**：[故事核心摘要]
* **選擇風格**：[1. 暖棕懷舊底片風格 / 2. 日系可愛漫畫風格 / 3. 自行輸入之風格]
* **畫面規格**：16:9 寬螢幕 $2 \times 2$ 四格拼盤

---

#### 🖼️ 第一格（起・開端）
* **【畫面構圖】**：[鏡頭視角與場景描述]
* **【主體動作與表情】**：[人物動作、表情細節]
* **【畫面配文】**：「[第一格文案]」

#### 🖼️ 第二格（承・過程/升級）
* **【畫面構圖】**：[鏡頭視角與場景描述]
* **【主體動作與表情】**：[人物動作、表情細節]
* **【畫面配文】**：「[第二格文案]」

#### 🖼️ 第三格（轉・高潮/衝突）
* **【畫面構圖】**：[鏡頭視角與場景描述]
* **【主體動作與表情】**：[人物動作、表情細節]
* **【畫面配文】**：「[第三格文案]」

#### 🖼️ 第四格（合・反轉/結尾）
* **【畫面構圖】**：[鏡頭視角與場景描述]
* **【主體動作與表情】**：[人物動作、表情細節]
* **【畫面配文】**：「[第四格反轉文案]」

---
💬 **請確認以上分鏡與文案是否符合您的期望？若需要微調畫面細節或文字請告訴我；確認無誤後，我將立即為您生成圖片！**
```

---

### 🔹 第三步：收到確認後執行生圖 (Image Generation)

收到使用者確認（如「確認」、「可以」、「生圖」）後，呼叫 `generate_image` 生圖工具（`AspectRatio: "16:9"`）。

#### 各風格 Prompt 構造規範：

- **風格 1（暖棕懷舊底片風格）**：
  `A 16:9 horizontal image structured as a 2x2 four-panel comic grid (2 rows, 2 columns) with thin black borders. Visual Style: Warm sepia-toned vintage 35mm film photo, warm brownish monochrome palette, high-contrast dramatic chiaroscuro lighting, gritty documentary photojournalism realism, candid emotional micro-expressions, rich film grain. NO pure cold black and white, NO digital smooth look. ...`

- **風格 2（日系可愛漫畫風格）**：
  `A 16:9 horizontal image structured as a 2x2 four-panel comic grid (2 rows, 2 columns) with thin black borders. Visual Style: Cute Japanese anime comic strip style, soft pastel colors, warm line art, expressive chibi/manga character facial expressions, cozy watercolor textures, high quality manga illustration. ...`

- **風格 3（自行輸入）**：
  根據使用者指定的風格融合至 16:9 $2 \times 2$ 4-panel prompt 中。

生成完成後，自動複製至 `assets/` 目錄並執行 `open -R` 開啟 Finder 視窗！

---

## 觸發詞清單

- 「這是我的腳本，請幫我生成四格漫畫」
- 「生成四格黑白漫畫風格」
- 「生成四格漫畫風格」
- 「四格漫畫」
- 「四格黑白梗圖」
- 「四格懷舊圖片」
