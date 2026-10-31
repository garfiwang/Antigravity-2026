# ambitious-brief：往上想一層・往下挖一層・往外借一招

> **把一句「幫我做 X」升級成一整件交給 AI 的高維度工作任務說明書。**

[![Version: 1.0.0](https://img.shields.io/badge/version-1.0.0-blue.svg)](./CHANGELOG.md)
[![Platform: Claude Code & Antigravity](https://img.shields.io/badge/platform-Claude_Code_%7C_Antigravity-orange.svg)](#-安裝方式)
[![Methodology: Felix Rieseberg](https://img.shields.io/badge/methodology-Anthropic_Engineering-purple.svg)](https://felixrieseberg.com/)
[![Troubleshooting Guide](https://img.shields.io/badge/docs-Troubleshooting_Guide-red.svg)](./TROUBLESHOOTING.md)

---

## 💡 核心由來與設計理念

本技能方法源自 **Anthropic 工程主管 Felix Rieseberg** 的知名文章〈*How to be more ambitious: A tutorial for humans with models*〉，由 **Fanko AI 範式** 整理為繁體中文實戰工作流。

當我們對 AI 下指令時，往往只停留在「做一個動作」（例如：*「幫我做投影片」*、*「幫我回信」*、*「幫我選供應商」*）。本技能透過**「三步升級法 ＋ 一道驗證關卡」**，幫助你把瑣碎的動作指令，升級為具備商業戰略高度、第一手真實查核、跨界視角團隊以及免作弊檢驗的專業級任務交付說明（Brief）。

---

## 🎯 觸發關鍵字 (Trigger Keywords)

在 **Claude Code** 或 **Google Antigravity** 對話中，輸入以下任一指令即可自動觸發：

* **`提升任務：[你的任務]`**（最推薦，簡潔明瞭！）
* **`提升任務`**
* **`用三個方法幫我升級這個任務：[你的任務]`**
* **`幫我把這件事交代得更有野心：[你的任務]`**
* **`往上想往下挖往外借：[你的任務]`**
* **`ambitious brief：[你的任務]`**

> 💡 **自動動手秘訣**：  
> 若希望改寫完成後**由 AI 直接照著新交代動手執行**，只要在句尾加上 **「改完直接做」** 即可！

---

## 🏗️ 核心升級三步驟

| 步驟 | 核心思維 | 具體做法 |
| :--- | :--- | :--- |
| **1. 往上想一層**<br>*(把事情交大)* | **從「動作」改為「結果」** | 釐清「做完後接下來希望發生什麼？」，並鎖定 AI 必須具備的三條件：**看得到**（資料）、**動得了**（權限）、**確認得了**（自檢標準）。 |
| **2. 往下挖一層**<br>*(做得更深，不是更多)* | **以行業頂尖專家的標準執行** | 逼問自己：該行最厲害的人會多做什麼？翻哪些第一手資料？使用什麼硬核算式？加上**極度具體的指標**與**第三方無法作弊的檢核方式**。 |
| **3. 往外借一招**<br>*(借跨界行業的眼光)* | **換個領域借招，組建專業戰隊** | 將名詞化為動詞，思考該動詞哪個行業做得最好。組建 3～5 人專家團隊，並要求**「挑毛病角色只看最終成品，不看過程」**，徹底杜絕自查盲區。 |
| **最後關卡**<br>*(標準分流機制)* | **區分標準答案 vs 主觀感覺** | • **查得出對錯（數據、程式）** ➔ 放心交大放手跑。<br>• **靠感覺（選人、文案風格）** ➔ 拆成兩輪，先給選項與決策矩陣，保留真人拍板。 |

---

## 📦 輸出成果結構

調用本技能後，AI 會交付以下標準結構：

1. **改寫後的交代（Direct Prompt）**：一段可直接複製貼入 Claude / ChatGPT / Gemini 對話視窗的完整任務指令（含背景、角色分工、邊界條件與格式）。
2. **貼之前要準備什麼**：明確提醒需手動填換的 `【請填：…】` 變數、需附帶的真實文件檔案，以及務必刪除的敏感機密個資。
3. **升級說明（最多 10 行）**：清楚交代為何這樣改、往上想了什麼、借了哪一招，以及為你做的合理商業假設。

---

## 🚀 安裝方式

### 1. Claude Code
```bash
# 在終端機中執行指令安裝
claude skills add garfiwang/AI-skill --path 02-productivity/ambitious-brief
```

### 2. Google Antigravity
* **專案級技能**：將本資料夾複製至專案根目錄的 `.agents/skills/ambitious-brief/`
* **全域級技能**：複製至全域配置 `~/.gemini/config/skills/ambitious-brief/`

### 3. ChatGPT / Gemini 等無 Skill 功能的平台
打開資料夾內的 [`prompt.md`](./prompt.md)，複製整篇提示詞貼入對話視窗開頭，即可在一般對話中暢享相同的升級體驗。

---

## 📚 檔案清單與文檔連結

* [`SKILL.md`](./SKILL.md)：Skill 核心規範與決策邏輯
* [`CHANGELOG.md`](./CHANGELOG.md)：版本變更歷史紀錄
* [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md)：實戰踩坑紀錄與排查手冊
* [`references/examples.md`](./references/examples.md)：官方經典改寫範例（季報、選供應商、輕版客訴）
* [`prompt.md`](./prompt.md)：單次通用提示詞版

---

## 👤 製作人與授權

* **製作人**：王執定 Rich (garfiwang@gmail.com) · 問大師家族辦公室
* **授權協議**：[MIT License](../../LICENSE)
