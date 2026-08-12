# 🛑 收工同步助手 (`shutdown` skill)

> **版本**：`v1.0.0`  
> **適用類型**：Antigravity / AI Coding Assistant  
> **核心職責**：自動進行「收工同步與進度保存」，確保每次工作結束後進度皆完整寫入專案藍圖、Git 儲存庫與 Obsidian。

---

## 📖 技能簡介

`shutdown` 是一個具備**三層級自動偵測（L1 本地 / L2 GitHub / L3 Obsidian）**的收工同步技能。當使用者準備結束工作、下班或更換電腦時，AI Agent 會盤點本次 Session 的成果，將最新進度整理由精簡的 `handoff.md` 交接檔寫入本地、推送到 GitHub，並同步完整的踩坑與決策紀錄至 Obsidian，達成無縫的跨 Session / 跨電腦交接。

---

## 🎯 觸發關鍵字

當使用者輸入以下任何內容時，將自動觸發本技能：
- `收工`
- `結束了`
- `下班`
- `準備換電腦`
- `同步`
- `先到這裡`
- `換電腦繼續做`

---

## 🏗️ 三層級同步架構

| 層級 | 同步動作 | 目標讀者 / 用途 |
| :--- | :--- | :--- |
| **L1 本地** | 更新 `AGENTS.md` Checklist，重寫 `handoff.md` 交接檔 | 下一個 Session 的任何 AI Agent 或使用者 |
| **L2 GitHub** | 擬定中文 Commit 訊息，點頭確認後執行 `commit + push` | 版本歷史記錄、雲端備份與團隊協作 |
| **L3 Obsidian** | 將詳細決策與踩坑筆記寫入 `專案工作流程.md` | 未來需要深度回溯脈絡與踩坑經驗時參考 |

---

## 📋 執行 SOP 流程

1. **盤點本次成果**：從 Session 對話歷史與檔案變更中整理摘要。
2. **L1 藍圖與交接檔更新**：
   - 更新 `AGENTS.md` 進度清單。
   - **重寫** `handoff.md`（包含：目前做到哪、目前狀態、下一步、注意事項、最後更新者與電腦）。
3. **L2 Git Commit & Push**：
   - 擬定繁體中文 Commit 訊息（包含動詞、對象與重點異動列表）。
   - 請使用者過目確認後執行 Commit 與 `git push`。
   - 回填 `handoff.md` 的 Git push 狀態。
4. **L3 Obsidian 紀錄寫入**（若可用）：
   - 更新 `專案工作流程.md` 的紀錄表格與踩坑筆記。
5. **輸出層級 Checklist 回報**。

---

## 📄 輸出範例

```text
✅ L1 本地：AGENTS.md 進度已更新、handoff.md 已改寫（更新者：Agent @ Mac-Pro）
✅ L2 GitHub：Antigravity-2026 已 commit + push（feat(skills): 新增技能 README 說明檔）
✅ L3 Obsidian：專案工作流程.md 已補紀錄
```

---

## 🔗 相關技能

- [🚀 開工接續助手 (`startup`)](../startup/README.md)：與本技能呈**對偶關係**（開工是「讀」、收工是「寫」）。
