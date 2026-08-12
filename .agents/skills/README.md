# 🛠️ AntiGravity 技能庫 (.agents/skills)

本目錄包含專案中使用的 **AntiGravity Agent 技能 (Skills)**。技能是用於擴充 AI Agent 能力的標準化指令與工作流程規範。

---

## 📌 核心工作流技能 (Core Workflow Skills)

| 技能名稱 | 版本 | 觸發關鍵字 | 簡介 | 說明檔 |
| :--- | :--- | :--- | :--- | :--- |
| **🚀 開工接續 (`startup`)** | `v1.0.0` | `開工` `開始工作` `上次做到哪` | 三層級自動偵測開工脈絡接續助手（讀取交接檔與 Git 狀態） | [說明檔](startup/README.md) |
| **🛑 收工同步 (`shutdown`)** | `v1.0.0` | `收工` `結束了` `準備換電腦` | 三層級自動偵測收工同步助手（寫入交接檔、Git Commit/Push、Obsidian） | [說明檔](shutdown/README.md) |
| **🏗️ 專案初始化 (`project-init`)** | `v1.0.0` | `初始化專案` `init 專案` | 自動建立專案藍圖 (`AGENTS.md`) 與交接檔 (`handoff.md`) | - |

---

## 💡 常用領域技能 (Domain Skills)

* **簡報與排版**：
  * `wendashi-pptx` (v2.0.0)：問大師家族辦公室品牌簡報製作
  * `html-slide-builder`：樂齡友善 Reveal.js 互動簡報製作
  * `newspaper-pptx`：報紙風格單頁 PPTX 排版
  * `pptx-legal-slide`：問大師簡報法規/判決版
* **內容與文案**：
  * `ai-advisors-team` (v1.0.0)：三國五人智囊決策輔助
  * `fb-long-post` (v1.0.0)：高流量 FB 長文撰寫
  * `threads-post` (v1.0.0)：每日 Threads 短文生成
  * `storytelling-7steps` (v1.0.0)：故事創作七步法
* **工具與記錄**：
  * `morning-briefing` (v1.1.0)：早晨日報與任務彙整
  * `notion-note` / `notion-inspiration-box`：Notion 資料庫快速記錄
  * `obsidian-weekly-review`：Obsidian 週度知識整理

---

## 🛠️ 如何新增或更新技能

1. 在 `.agents/skills/<skill-name>/` 下建立 `SKILL.md`。
2. 在 `SKILL.md` 的 Frontmatter 中標明 `name`、`version`、`description` 及 `changelog`。
3. 建議同步建立 `README.md` 以供人類使用者參閱與使用說明。
