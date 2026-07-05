---
name: weekly-report
version: 1.1.0
description: >
  產生每週進度報告 HTML。查詢 Google Calendar 行程、Notion Tasks/Projects 資料庫，
  彙整本週總覽、上週回顧、待辦任務與進行中專案。
  觸發條件：使用者輸入「每週報告」、「每週進度報告」、「weekly report」。
---

# 每週進度報告技能 (v1.1.0)

> **版本變動紀錄 (v1.1.0)**：
> - **版面排版欄位對調**：
>   - 將「本週行程」與「上週回顧」欄位與寬度對調，「本週行程」移至左側大欄 (`span-2`)，「上週回顧」移至右側小欄。
>   - 將「待辦任務」與「進行中專案」欄位與寬度對調，「待辦任務」移至左側大欄 (`span-2`)，「進行中專案」移至右側小欄。

當使用者輸入「**每週報告**」、「**每週進度報告**」、「**weekly report**」時，執行以下步驟。

## 執行步驟

**今天日期**：從系統時間取得今天日期。計算本週一～週日範圍（台灣時間）。

### 步驟 1：查詢 Notion

**1a. WIP 進行中專案**
- 查詢 `Projects Database`（ID：`201c9c67-1f57-81e8-b126-000bc08f6d75`）
- 使用 `query-data-source`，篩選 `Status` = `"WIP"`
- 記錄每個專案的名稱與 End Date

**1b. 未完成待辦任務**
- 查詢 `Tasks Database`（ID：`201c9c67-1f57-8143-bd10-000b05412488`）
- 使用 `query-data-source`，篩選 `Done` = `false`
- 記錄每個任務的名稱與 Due Date

### 步驟 2：查詢 Google Calendar

使用 `list_events`（calendarId = `primary`）：
- 查詢**上週一至本週日**（例如本週 6/1 ～ 6/7，則查 5/25 ～ 6/7）
- 時區：`Asia/Taipei`
- 依星期分組整理

### 步驟 3：產生 HTML 報告

使用下方完整 HTML 範本，填入實際資料後存檔。

#### 資料填入對照

| 佔位符 | 說明 |
|---|---|
| `{YYYY年M月D日}` / `{週X}` | 今天日期 |
| `{第X週}` | 當年ISO週數 |
| `{涵蓋期間}` | 本週一～日本週日 |
| `{WIP數}` / `{待辦數}` / `{逾期數}` / `{本週到期數}` | 統計數字 |
| `{行動一～三}` / `{原因一～三}` | Top 3 建議 |
| `{上週每日行程}` | 上週一～日，每日一組 `.week-label` + `ul.item-list` |
| `{本週每日行程}` | 本週一～日，當天標 `week-today` |
| `{WIP專案列表}` | 所有 WIP 專案的 `.project-item` |
| `{待辦任務列表}` | 所有未完成任務的 `.todo-item`（逾期加 `overdue`） |
| `{YYYY-MM-DD}` | 今日日期（檔案名與 localStorage key 用） |

#### 輸出路徑

```
OUTPUT_DIR="${MORNING_BRIEFING_DIR:-$HOME/晨間早報}"
```

但本技能使用固定路徑（可覆寫環境變數 `WEEKLY_REPORT_DIR`）：
- 預設：`$HOME/Documents/每週報告/`
- 檔名：`YYYY-MM-DD.html`（如 `2026-06-04.html`）

產生後回報使用者：「✅ 每週進度報告已存至 {路徑}」

---

## HTML 完整範本

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>📋 每週進度報告｜{YYYY年M月D日}</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #F9F5F0; color: #3E2115;
      font-family: -apple-system, BlinkMacSystemFont, "Noto Sans TC", "PingFang TC", sans-serif;
      max-width: 1200px; margin: 0 auto;
      padding: 28px 16px 60px; line-height: 1.6;
    }
    header { text-align: center; margin-bottom: 28px; }
    header h1 { font-size: 2rem; font-weight: 700; color: #3E2115; }
    header .date { color: #A47551; font-size: 1rem; margin-top: 4px; }
    header .sub { color: #A47551; font-size: 0.85rem; margin-top: 2px; }

    .bento-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    .card { background: #fff; border-radius: 16px; box-shadow: 0 2px 12px rgba(62,33,21,0.08); overflow: hidden; }
    .span-2 { grid-column: span 2; }
    .span-3 { grid-column: span 3; }

    .card-header {
      display: flex; justify-content: space-between; align-items: center;
      padding: 14px 20px; cursor: pointer; user-select: none;
      background: rgba(164,117,81,0.07); border-bottom: 1px solid rgba(62,33,21,0.08);
    }
    .card-header h2 { font-size: 0.95rem; font-weight: 600; color: #3E2115; }
    .toggle-icon { font-size: 0.9rem; color: #A47551; transition: transform 0.2s; }
    .card-body { padding: 16px 20px; }
    .card-body.collapsed { display: none; }

    .count-badge {
      display: inline-block; background: #3E2115; color: #FFD700;
      font-size: 0.7rem; font-weight: 700; padding: 1px 8px; border-radius: 10px; margin-left: 6px;
    }

    .item-list { list-style: none; }
    .item-list li {
      padding: 6px 0; border-bottom: 1px solid rgba(62,33,21,0.05);
      font-size: 0.88rem; display: flex; align-items: center; gap: 8px;
    }
    .item-list li:last-child { border-bottom: none; }

    .day-tag {
      display: inline-block; background: rgba(164,117,81,0.12); color: #A47551;
      font-size: 0.7rem; font-weight: 600; padding: 1px 6px; border-radius: 4px;
      min-width: 42px; text-align: center; flex-shrink: 0;
    }
    .time-tag {
      display: inline-block; background: rgba(62,33,21,0.08); color: #3E2115;
      font-size: 0.72rem; font-weight: 600; padding: 1px 6px; border-radius: 4px;
      min-width: 50px; text-align: center; flex-shrink: 0;
    }
    .week-label {
      font-size: 0.78rem; font-weight: 600; color: #A47551;
      padding: 8px 0 4px; border-bottom: 1px dashed rgba(164,117,81,0.2); margin-bottom: 4px;
    }
    .week-label:first-child { padding-top: 0; }
    .week-today { color: #3E2115; }

    .project-item {
      padding: 8px 12px; border-radius: 8px;
      background: rgba(164,117,81,0.07); margin-bottom: 6px; font-size: 0.85rem;
    }
    .project-item:last-child { margin-bottom: 0; }
    .project-name { font-weight: 600; color: #3E2115; }
    .project-meta { color: #A47551; font-size: 0.75rem; margin-top: 1px; display: flex; gap: 8px; }
    .overdue-tag { color: #CF202E; font-weight: 600; }
    .soon-tag { color: #D4922B; font-weight: 600; }
    .empty-note { color: #A47551; font-size: 0.85rem; font-style: italic; }

    .stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
    .stat-item { text-align: center; padding: 12px 8px; background: rgba(164,117,81,0.06); border-radius: 10px; }
    .stat-num { font-size: 1.6rem; font-weight: 700; color: #3E2115; }
    .stat-label { font-size: 0.72rem; color: #A47551; margin-top: 2px; }
    .stat-item.highlight-stat { background: #3E2115; }
    .stat-item.highlight-stat .stat-num { color: #FFD700; }
    .stat-item.highlight-stat .stat-label { color: rgba(255,215,0,0.8); }

    .top3-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
    .top3-item { background: rgba(255,255,255,0.08); border-radius: 10px; padding: 14px; border: 1px solid rgba(255,255,255,0.12); }
    .top3-num { font-size: 1.6rem; font-weight: 800; color: #FFD700; line-height: 1; margin-bottom: 6px; }
    .top3-action { font-size: 0.9rem; font-weight: 600; color: #F9F5F0; margin-bottom: 4px; }
    .top3-reason { font-size: 0.8rem; color: rgba(249,245,240,0.7); }

    .highlight-card { background: linear-gradient(135deg, #3E2115 0%, #6B3D28 100%); color: #F9F5F0; }
    .highlight-card .card-header { background: rgba(255,255,255,0.07); border-bottom-color: rgba(255,255,255,0.12); }
    .highlight-card .card-header h2 { color: #FFD700; }
    .highlight-card .toggle-icon { color: #FFD700; }

    footer { text-align: center; margin-top: 32px; color: #A47551; font-size: 0.85rem; }

    .todo-item {
      display: flex; align-items: flex-start; gap: 10px;
      padding: 6px 0; border-bottom: 1px solid rgba(62,33,21,0.05);
    }
    .todo-item:last-child { border-bottom: none; }
    .todo-item input[type="checkbox"] { width: 16px; height: 16px; accent-color: #A47551; flex-shrink: 0; margin-top: 3px; cursor: pointer; }
    .todo-item label { font-size: 0.85rem; cursor: pointer; flex: 1; }
    .todo-item.done label { text-decoration: line-through; color: #A47551; }
    .due-tag { font-size: 0.72rem; color: #A47551; margin-left: 4px; }
    .overdue { color: #CF202E !important; font-weight: 600; }

    @media (max-width: 768px) {
      .bento-grid { grid-template-columns: 1fr; }
      .span-2, .span-3 { grid-column: span 1; }
      .stat-grid { grid-template-columns: repeat(2, 1fr); }
      .top3-grid { grid-template-columns: 1fr; }
    }
    @media print {
      .toggle-icon { display: none; }
      .card-body.collapsed { display: block !important; }
      body { background: white; padding: 0; }
    }
  </style>
</head>
<body>

<header>
  <h1>📋 每週進度報告</h1>
  <p class="date">{YYYY年M月D日}（{週X}）｜第{第X週}週</p>
  <p class="sub">涵蓋期間：{涵蓋期間}</p>
</header>

<main class="bento-grid">

  <section class="card span-3">
    <div class="card-header" onclick="toggleCard(this)">
      <h2>📊 本週總覽</h2>
      <span class="toggle-icon">▾</span>
    </div>
    <div class="card-body">
      <div class="stat-grid">
        <div class="stat-item"><div class="stat-num">{WIP數}</div><div class="stat-label">進行中專案</div></div>
        <div class="stat-item"><div class="stat-num">{待辦數}</div><div class="stat-label">待辦任務</div></div>
        <div class="stat-item"><div class="stat-num">{逾期數}</div><div class="stat-label">已逾期任務</div></div>
        <div class="stat-item highlight-stat"><div class="stat-num">{本週到期數}</div><div class="stat-label">本週到期 ⚡</div></div>
      </div>
    </div>
  </section>

  <section class="card span-3 highlight-card">
    <div class="card-header" onclick="toggleCard(this)">
      <h2>💡 本週建議行動（Top 3）</h2>
      <span class="toggle-icon">▾</span>
    </div>
    <div class="card-body">
      <div class="top3-grid">
        <div class="top3-item"><div class="top3-num">1</div><div class="top3-action">{行動一}</div><div class="top3-reason">{原因一}</div></div>
        <div class="top3-item"><div class="top3-num">2</div><div class="top3-action">{行動二}</div><div class="top3-reason">{原因二}</div></div>
        <div class="top3-item"><div class="top3-num">3</div><div class="top3-action">{行動三}</div><div class="top3-reason">{原因三}</div></div>
      </div>
    </div>
  </section>

  <section class="card span-2">
    <div class="card-header" onclick="toggleCard(this)">
      <h2>📆 本週行程（{本週日期範圍}）</h2>
      <span class="toggle-icon">▾</span>
    </div>
    <div class="card-body">
      {本週每日行程}
    </div>
  </section>

  <section class="card">
    <div class="card-header" onclick="toggleCard(this)">
      <h2>📅 上週回顧（{上週日期範圍}）</h2>
      <span class="toggle-icon">▾</span>
    </div>
    <div class="card-body">
      {上週每日行程}
    </div>
  </section>

  <section class="card span-2">
    <div class="card-header" onclick="toggleCard(this)">
      <h2>✅ 待辦任務 <span class="count-badge">{待辦數}</span></h2>
      <span class="toggle-icon">▾</span>
    </div>
    <div class="card-body">
      {待辦任務列表}
    </div>
  </section>

  <section class="card">
    <div class="card-header" onclick="toggleCard(this)">
      <h2>🚀 進行中專案 <span class="count-badge">{WIP數}</span></h2>
      <span class="toggle-icon">▾</span>
    </div>
    <div class="card-body">
      {WIP專案列表}
    </div>
  </section>

</main>

<footer>每週進度報告 · 自動產生於 {YYYY-MM-DD}</footer>

<script>
  const STORAGE_KEY = 'weekly-todos-{YYYY-MM-DD}';
  function toggleCard(h) {
    const b = h.nextElementSibling, i = h.querySelector('.toggle-icon');
    const c = b.classList.toggle('collapsed');
    i.style.transform = c ? 'rotate(-90deg)' : 'rotate(0deg)';
  }
  function onTodoChange(cb) {
    const w = cb.closest('.todo-item');
    w.classList.toggle('done', cb.checked);
    const s = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    s[cb.id] = cb.checked; localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
  }
  (function init() {
    const s = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    document.querySelectorAll('.todo-item input[type="checkbox"]').forEach(cb => {
      if (s[cb.id]) { cb.checked = true; cb.closest('.todo-item').classList.add('done'); }
    });
  })();
</script>
</body>
</html>
```

---

## 注意事項

- 時間顯示為台灣時間（UTC+8）
- 逾期任務（Due Date < 今天）的 `.due-tag` 加 `overdue` class（紅色）
- 本週到期任務加 `soon-tag` class（橙色）
- 所有文字使用**繁體中文**
- HTML 必須為完整自含式，不依賴外部 CDN
- 若某資料來源查詢失敗，在對應區塊填入 `<li class="empty-note">資料取得失敗</li>`
- Top 3 建議行動：優先選擇**今天到期／逾期最 urgent**的事項，其次是**高價值客戶相關**
