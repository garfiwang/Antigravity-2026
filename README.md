# 🌌 Antigravity-2026

> **Google Antigravity AI Agent 專案藍圖、個人工作流程與技能庫**

歡迎來到 `Antigravity-2026`！本 Repository 為個人 AI Agent 工作流、專案藍圖及技能庫（Skills Directory）。

---

## 📌 核心工作流技能 (Core Skills)

本儲存庫整合了最新的**三層級自動偵測架構 (L1 本地 / L2 GitHub / L3 Obsidian)**，支援跨對話 Session、跨電腦的無縫進度銜接：

| 技能名稱 | 版本 | 觸發關鍵字 | 簡介與說明檔 |
| :--- | :--- | :--- | :--- |
| **🚀 開工接續助手 (`startup`)** | `v1.0.0` | `開工` `開始工作` `上次做到哪` | 自動讀取藍圖與交接檔、檢查 Git 與遠端狀態。<br>👉 [詳細說明檔](.agents/skills/startup/README.md) |
| **🛑 收工同步助手 (`shutdown`)** | `v1.0.0` | `收工` `結束了` `準備換電腦` | 自動盤點成果、重寫 `handoff.md`、推送 Git 並寫入 Obsidian。<br>👉 [詳細說明檔](.agents/skills/shutdown/README.md) |
| **🛠️ 完整技能庫導覽** | - | - | 包含簡報、文案、記錄等全套 Agent 技能目錄。<br>👉 [完整技能目錄](.agents/skills/README.md) |

---

## 🏗️ 三層級自動偵測架構 (3-Tier Architecture)

1. **L1 本地層**：讀寫專案藍圖 `AGENTS.md` 與動態交接檔 `handoff.md`（紀錄當前狀態與下一步）。
2. **L2 GitHub 層**：自動繁體中文 Commit 訊息擬定、確認點頭後 `git push` 備份。
3. **L3 Obsidian 層**：同步完整脈絡、決策過程與踩坑筆記至個人 Obsidian 知識庫。

---

## 🚀 快速上手 (Usage)

在 Antigravity Agent 環境中：
* **開始工作時**：輸入 `開工` 或 `上次做到哪`，Agent 即會自動執行 `startup` 技能回報狀況。
* **結束工作時**：輸入 `收工` 或 `下班`，Agent 即會自動執行 `shutdown` 技能儲存與同步進度。
