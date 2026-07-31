---
name: transcript-to-notion
version: 1.0.0
description: 將演講/課程逐字稿（.md）自動清理、整理，寫入 Notion [G] Note database，並關聯至 Areas Database（[CC] 財富流）與 Resources Database（財富流教練包）。
changelog:
  - version: 1.0.0
    date: 2026-06-17
    note: 初始安裝自 GitHub
---

# Transcript to Notion — 逐字稿整理與寫入 Notion 技能

## Description
將演講/課程逐字稿（.md）自動清理、整理，寫入 Notion [G] Note database，並關聯至 Areas Database（[CC] 財富流）與 Resources Database（財富流教練包）。

## Trigger
使用者說「幫我整理這份逐字稿」、「寫入 notion」、「逐字稿整理」、「transcript to notion」，或提供 .md 逐字稿檔案路徑。

## Workflow

### Step 1: 讀取原始檔案
- 從使用者提供的路徑讀取原始逐字稿（.md）
- 檔案通常位於 `/Users/garfiwang/Downloads/ScreenRecording_*.md`

### Step 2: 清理與整理
- 刪除贅字與重複詞彙（如連續重複的「好也接下來呢」、「請不吝點讚…」等）
- 保留完整語意
- 標註重點與講師金句（🎯）
- 按主題分章節整理，輸出結構化 Markdown
- 存檔至 `/Users/garfiwang/Downloads/演講逐字稿_整理版_*.md`

### Step 3: 先輸出整理版給使用者確認
- 顯示整理後的內容摘要
- 讓使用者確認沒問題再寫入 Notion

### Step 4: 寫入 Notion [G] Note database

#### 資料庫資訊
- Database ID: `201c9c67-1f57-810a-8466-000b862f50e1`
- Parent (DB): `201c9c67-1f57-81e6-bf7c-c67509eef500`
- Notion Integration ID: `373c9c67-1f57-8135-ac61-00272567087c`

#### 建立頁面
使用 `notion_API-post-page`，參數：
- `parent`: `{"type": "data_source_id", "data_source_id": "201c9c67-1f57-810a-8466-000b862f50e1"}`（**注意：必須用 data_source_id 而非 database_id**）
- `properties:`
  - `Note` (title): 頁面名稱（如「財富流教練第X課：主題」）
  - `內容` (rich_text): 完整整理後的 md 內容（**不能只寫摘要**）
  - `來源` (rich_text): 原始檔案名稱
  - `Type` (select): `"Notes"`
  - `Tags` (multi_select): `["上課筆記", "自我成長"]`
  - `分類` (select): `"資訊"`
  - `標籤` (multi_select): `["演講"]`
- `children`: 結構化摘要的 block 陣列（heading_2 / paragraph / callout / divider 等）

#### Block 類型對照
| Markdown | Notion Block Type |
|----------|------------------|
| `## 標題` | `heading_2` |
| `### 標題` | `heading_3` |
| `**金句**` | `callout` + emoji 🎯 |
| `---` | `divider` |
| 一般段落 | `paragraph` |
| 作業/待辦 | `callout` + emoji 📝 |

### Step 5: 關聯資料庫

#### Areas Database: `[CC] 財富流`
- Page ID: `37ec9c67-1f57-80c6-9f6d-d321d25a62e0`
- 使用 `notion_API-patch-page` 設定：
  ```json
  "properties": {
    "Related to Areas Database": {
      "relation": [{"id": "37ec9c67-1f57-80c6-9f6d-d321d25a62e0"}]
    }
  }
  ```

#### Resources Database: `財富流教練包`
- Page ID: `380c9c67-1f57-801f-a9cf-d13316f781e7`
- 使用 `notion_API-patch-page` 設定：
  ```json
  "properties": {
    "Related to Resources Database": {
      "relation": [{"id": "380c9c67-1f57-801f-a9cf-d13316f781e7"}]
    }
  }
  ```

### Step 6: 確認完成
- 回報使用者頁面已建立
- 提供 Notion 頁面 URL
- 確認關聯已設定

## Notes
- 建立頁面時**不能**傳入 `Notion-Version` header（會報 validation_error）
- parent 須用 `type: "data_source_id"`，對應 [G] Note database 的 data_source_id
- rich_text 內容支援 Markdown 語法
- 如果已有舊頁面，需先移入垃圾桶（`patch-page` 設 `in_trash: true`）
