# 🏗️ 專案初始化助手 (`project-init` skill)

> **版本**：`v1.1.0`  
> **適用類型**：Antigravity / AI Coding Assistant  
> **核心職責**：自動進行「專案初始化」，依照當前環境工具鏈自動建構最高支援的三層級基礎設施（L1 本地藍圖、L2 GitHub 私有庫、L3 Obsidian 第二大腦筆記）。

---

## 📖 技能簡介

`project-init` 是一套**三層級自動偵測與適應**的專案初始化技能。當開啟新專案或在新資料夾動工時，AI Agent 會依照這台電腦已啟用的工具鏈，自動建立：
- **L1 本地**：跨 Agent 開放標準專案藍圖 (`AGENTS.md`) 與交接檔 (`handoff.md`)。
- **L2 GitHub**：本地 Git 版本控制並透過 GitHub CLI 自動建立 Private Repo 雲端備份。
- **L3 Obsidian**：在第二大腦 Obsidian Vault 中建立專案工作流程與詳細紀錄筆記。

---

## 🎯 觸發關鍵字

當使用者輸入以下任何內容時，將自動觸發本技能：
- `初始化專案`
- `專案初始化`
- `幫這個專案做初始化`
- `開新專案`
- `建立專案藍圖`
- `幫我 init 專案`

---

## 🏗️ 三層級偵測架構

| 層級 | 偵測條件 | 執行的初始化動作 |
| :--- | :--- | :--- |
| **L1 本地** | 無條件永遠執行 | 建立 `AGENTS.md`（專案藍圖）與 `handoff.md`（交接檔） |
| **L2 GitHub** | 具備 `git` 且 `gh auth status` 顯示已登入 | 初始化 Git、建立 `.gitignore`、首發 commit，並使用 `gh repo create` 建立遠端私有庫 |
| **L3 Obsidian** | 具備 Obsidian MCP 或偵測到本機標準 Vault 路徑 | 建立專案資料夾與 `<專案資料夾>/專案工作流程.md` 詳細脈絡筆記 |

---

## 📋 執行 SOP 流程

1. **L1 本地藍圖建立**：
   - 掃描資料夾結構與既有檔案。
   - 詢問專案名稱、目標與關鍵時程。
   - 建立 `AGENTS.md` 與 `handoff.md`。
2. **L2 GitHub 遠端建立**：
   - 啟用系統權限 (`BypassSandbox: true`) 執行 `gh auth status` 確保設定檔讀取正常。
   - 執行 `git init`、設定使用者資訊、加入 `.gitignore` 並完成首發 Commit。
   - 建立 GitHub 私有儲存庫並推播程式碼。
   - 將 GitHub 儲存庫網址回填至 `AGENTS.md`。
3. **L3 Obsidian 筆記建立**：
   - 雙軌自動偵測（優先 MCP，Fallback 自動定位本地標準 Vault 目錄如 `~/Documents/Obsidian`）。
   - 建立專案工作流程筆記（脈絡、決策、踩坑、變更紀錄）。
   - 將筆記路徑回填至 `AGENTS.md`。
4. **輸出初始化層級報告**。

---

## 📄 輸出範例

```text
🏗️ 本專案初始化至第 3 層級
✅ L1 本地：AGENTS.md ＋ handoff.md 已建立
✅ L2 GitHub：garfiwang/my-new-project（私有儲存庫已建立並推播）
✅ L3 Obsidian：/Users/garfiwang/Documents/Obsidian/my-new-project/專案工作流程.md 已建立詳細筆記
```

---

## 🔗 相關技能

- [🚀 開工接續助手 (`startup`)](../startup/README.md)：新對話開始時自動讀取藍圖與交接檔。
- [🛑 收工同步助手 (`shutdown`)](../shutdown/README.md)：對話結束前自動更新交接檔、Git Push 與 Obsidian 紀錄。
