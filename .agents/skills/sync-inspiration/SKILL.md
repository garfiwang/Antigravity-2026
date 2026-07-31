---
name: sync-inspiration
version: 1.0.0
description: 同步靈感盒 Clippings 到 Notion
changelog:
  - version: 1.0.0
    date: 2026-07-05
    note: 初始版本
---

# 同步靈感盒 Skill

## 觸發條件
當使用者說「同步靈感盒」、「sync 靈感盒」、「同步 clippings」時立即執行。

---

## 欄位對應

| Notion 欄位 | Obsidian frontmatter |
|---|---|
| 標題 | title + 檔名 |
| 來源 | source |
| 內容 | 正文 |
| 分類 | type |
| 標籤 | tags |
| 建立時間 | created |

---

## 執行步驟

### Step 1：查詢 Notion 靈感盒
使用 `notion-query-database-view`：
- view_url: `https://www.notion.so/32ac9c671f578135af59d67d058a09a0?v=32ac9c671f57819cbf24000c8e8e25d2`
- 取回所有項目（已有 Archive=false 的 filter）

### Step 2：取得 Obsidian 現有檔案清單
使用 `mcp__obsidian__list_directory`，path = `Clippings`
取得所有 .md 檔名，存為比對清單。

### Step 3：逐筆比對並寫入

對每個 Notion 項目執行：

1. **檔名處理**：將「標題」移除 `/ : * ? " < > | \` 等特殊字元，作為檔名
2. **比對**：若 `Clippings/{檔名}.md` 已存在 → 略過
3. **不存在則寫入**，格式如下：

```
---
title: {標題}
source: {來源}        ← 若為空則省略此行
created: {建立時間，格式 YYYY-MM-DD}
type: {分類}          ← 若為空則省略此行
tags: {標籤陣列}      ← 若為空則省略此行，有值則格式為 ["tag1", "tag2"]
---

{內容欄位文字}        ← 若內容為空則留空白
```

使用 `mcp__obsidian__write_note`，path = `Clippings/{檔名}.md`

### Step 4：輸出同步報告

格式：
```
✅ 同步完成
- 新增：N 筆（列出標題）
- 略過：N 筆（已存在）
- 失敗：N 筆（若有，列出標題與原因）
```

---

## 注意事項
- Archive = true 的項目不同步
- 標題為空的項目不處理（記錄為失敗）
- 同步為**單向**：Notion → Obsidian，不寫回 Notion
