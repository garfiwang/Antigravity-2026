---
name: wendashi-pptx
version: 2.0.0
description: >
  製作問大師家族辦公室（Wendashi Family Office）品牌簡報的專屬技能。
  當使用者說「做問大師簡報」、「幫我做一份問大師的簡報」、「做一份信託簡報」、
  「做一份家族辦公室的簡報」、「做一份問大師風格的PPT」，或任何需要產出
  符合問大師品牌識別系統 PPTX 的需求，一律使用此技能。
  本技能（v2.0.0）包含全套「七大經典排版樣式」（封面目錄、問題過渡、雙欄對照、數據排行榜、三欄軸線矩陣、時間軸敘事、三步驟行動），
  自動套用問大師專屬品牌色彩與規格，產出頂級專業的 .pptx 簡報檔案。
---

# 問大師家族辦公室 · 簡報製作技能 (v2.0.0 七大經典版型全涵蓋版)

> **版本變動紀錄 (v2.0.0)**：
> - **全面升級七大經典排版樣式**：新增封面目錄、巨幅問題過渡、雙欄對照、數據排行榜、三欄軸線與六宮格矩陣、時間軸敘事與運算公式框、三步驟行動結尾等 7 大模組化樣式模板。
> - **Logo 全頁固定座標與零遮擋保護**：精確制定 20 頁米白底內容頁之 Logo 固定規範（`x: 8.1, y: 5.14, w: 1.5, h: 0.292`），確保絕對不遮擋任何文字，且全篇大小位置完全一致。
> - **強化問大師 5 大品牌色彩與元件規範**：標準化 Header、金黃 Accent 裝飾線與底部金線組件。

---

## 品牌色彩系統

```
深棕色  #3E2115  → Primary 主色（標題 Header、過渡頁背景、重點卡片）
金黃色  #FFD700  → Accent 強調（分隔線、Bullet 圓點、底部色條、標題字）
米白色  #F9F5F0  → Background 背景（所有內容頁主背景）
朱紅色  #CF202E  → Alert 警示（巨型數據、漲幅、高光提醒）
暖棕色  #A47551  → Neutral 輔助（副標、頁碼、次要文字）
白色    #FFFFFF  → 反白文字、白卡背景
```

**pptxgenjs 色碼常數（不加 # 號）：**
```javascript
const C = {
  deepBrown: "3E2115",
  gold:      "FFD700",
  cream:     "F9F5F0",
  red:       "CF202E",
  warmBrown: "A47551",
  white:     "FFFFFF",
  gray:      "666666",
  darkGray:  "333333"
};
```

---

## Logo 使用規範

| 版本 | 使用場景 | 規則 |
|------|---------|------|
| 標準版（米白底） | 所有米白色 `#F9F5F0` 背景頁面 | 右下角固定位置與大小：`x: 8.1, y: 5.14, w: 1.5, h: 0.292` |
| 反白版（深棕底） | 深色背景頁面（章節頁、問題過渡頁、結尾頁） | **不放 Logo**，深棕背景上維持大氣簡潔反白樣式 |

**Logo 三大禁止事項：**
1. **禁止拉伸變形**：不得任意調整寬高比例，必須保持原始比例縮放（`w: 1.5, h: 0.292`）
2. **零遮擋保護**：Logo 位於 `y: 5.14`~`5.43`，上方距離內容卡片有充分留白，下方停於金黃底條上方，不得遮擋任何文字
3. **固定一致性**：所有內容頁面的 Logo 位置與大小必須完全一模一樣

---

## 固定設計元素（每頁必有）

1. **金黃底線**：每頁底部 `y: 5.5, h: 0.125, fill: FFD700`
2. **Header 色塊**：內容頁使用深棕色 Header (`y: 0, h: 0.9, fill: 3E2115`)，左側加金色 Accent 條 (`x: 0, y: 0, w: 0.1, h: 0.9`)
3. **標題與頁碼**：Header 內文字為金色 (`FFD700`) 20pt 粗體；右上角頁碼為暖棕色 (`A47551`) 15pt 粗體右對齊

---

## 🏛️ 七大經典排版樣式與代碼模板

本技能將所有簡報頁面歸類為 **7 大經典排版樣式**，製作時請靈活調用對應之 `pptxgenjs` 代碼模板：

### 樣式一：封面與導覽型 (Cover & TOC Layouts)
* **用途**：第一頁封面與第二頁目錄
```javascript
// 1.1 封面頁
const s1 = pres.addSlide();
s1.background = { color: C.cream };
s1.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 0.8, w: 8.8, h: 3.8, fill: { color: C.deepBrown }, shadow: makeShadow() });
s1.addShape(pres.shapes.RECTANGLE, { x: 1.0, y: 1.3, w: 0.1, h: 2.4, fill: { color: C.gold } });
s1.addText("【組織 / 系列名稱】", { x: 1.3, y: 1.25, w: 7.0, h: 0.4, fontSize: 15, fontFace: "Calibri", color: C.gold, bold: true });
s1.addText("【主標題名稱】", { x: 1.3, y: 1.7, w: 7.5, h: 1.1, fontSize: 36, fontFace: "Calibri", bold: true, color: C.white });
s1.addShape(pres.shapes.RECTANGLE, { x: 1.3, y: 2.95, w: 5.5, h: 0.04, fill: { color: C.gold } });
s1.addText("【副標題 / 摘要說明】", { x: 1.3, y: 3.1, w: 7.0, h: 0.6, fontSize: 16, fontFace: "Calibri", color: C.cream });
addLogo(s1); addGoldBar(s1);

// 1.2 目錄頁 (2x3 六分格卡片)
const s2 = pres.addSlide(); s2.background = { color: C.cream };
addHeader(s2, "報告目錄", "Table of Contents", 2);
chapters.forEach((ch, i) => {
  const col = i % 2, row = Math.floor(i / 2);
  const x = 0.6 + col * 4.5, y = 1.2 + row * 1.3;
  s2.addShape(pres.shapes.RECTANGLE, { x, y, w: 4.3, h: 1.1, fill: { color: C.white }, shadow: makeShadow() });
  s2.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.1, h: 1.1, fill: { color: C.gold } });
  s2.addShape(pres.shapes.RECTANGLE, { x: x+0.2, y: y+0.15, w: 1.0, h: 0.35, fill: { color: C.deepBrown } });
  s2.addText(ch.num, { x: x+0.2, y: y+0.15, w: 1.0, h: 0.35, fontSize: 12, fontFace: "Calibri", bold: true, color: C.gold, align: "center" });
  s2.addText(ch.title, { x: x+0.2, y: y+0.55, w: 3.9, h: 0.5, fontSize: 13, fontFace: "Calibri", bold: true, color: C.deepBrown });
});
addLogo(s2); addGoldBar(s2);
```

---

### 樣式二：問題過渡與章節分隔型 (Bold Question Transition Layout)
* **用途**：章節開頭、核心問句過渡頁 (Q1~Q6)
```javascript
function addQuestionSlide(title, mainQ, subQ) {
  const s = pres.addSlide();
  s.background = { color: C.deepBrown };
  s.addShape(pres.shapes.RECTANGLE, { x: 0.8, y: 1.2, w: 0.1, h: 3.2, fill: { color: C.gold } });
  s.addText(title, { x: 1.2, y: 1.1, w: 8, h: 0.8, fontSize: 48, fontFace: "Calibri", bold: true, color: C.gold });
  s.addText(mainQ, { x: 1.2, y: 2.0, w: 7.8, h: 1.3, fontSize: 28, fontFace: "Calibri", bold: true, color: C.white });
  s.addShape(pres.shapes.RECTANGLE, { x: 1.2, y: 3.4, w: 4.0, h: 0.03, fill: { color: C.gold } });
  if (subQ) s.addText(subQ, { x: 1.2, y: 3.6, w: 7.8, h: 0.9, fontSize: 16, fontFace: "Calibri", color: C.cream });
  addGoldBar(s); // 深棕底反白頁不放 Logo
  return s;
}
```

---

### 樣式三：雙欄對照與比較型 (Two-Column Comparison Layouts)
* **用途**：概念定義對照、生成式 vs 非生成式、策略建議對照
```javascript
const s = pres.addSlide(); s.background = { color: C.cream };
addHeader(s, "【頁面標題】", "【章節小字】", pageNum);
// 左欄（深色高光或白底）
s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 1.2, w: 4.2, h: 3.8, fill: { color: C.deepBrown }, shadow: makeShadow() });
s.addText("【左欄標題】", { x: 0.8, y: 1.4, w: 3.8, h: 0.5, fontSize: 18, fontFace: "Calibri", bold: true, color: C.gold });
s.addText("【左欄說明文字...】", { x: 0.8, y: 2.0, w: 3.8, h: 2.8, fontSize: 14, fontFace: "Calibri", color: C.cream });
// 右欄（白底金邊）
s.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 1.2, w: 4.2, h: 3.8, fill: { color: C.white }, shadow: makeShadow() });
s.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 1.2, w: 0.1, h: 3.8, fill: { color: C.gold } });
s.addText("【右欄標題】", { x: 5.5, y: 1.4, w: 3.6, h: 0.5, fontSize: 18, fontFace: "Calibri", bold: true, color: C.deepBrown });
s.addText("【右欄說明文字...】", { x: 5.5, y: 2.0, w: 3.6, h: 2.8, fontSize: 14, fontFace: "Calibri", color: C.darkGray });
addLogo(s); addGoldBar(s);
```

---

### 樣式四：數據排行榜與網格陣列型 (Data & Ranking Grid Layouts)
* **用途**：Top 8 職類/產業、Top 3 成長高光、起薪溢價
```javascript
// 4.1 3欄巨型數字高光卡片 (Top 3 成長)
top3.forEach((item, i) => {
  const x = 0.6 + i * 3.0;
  s.addShape(pres.shapes.RECTANGLE, { x, y: 1.3, w: 2.8, h: 3.6, fill: { color: item.bg }, shadow: makeShadow() });
  s.addText(item.rank, { x: x+0.2, y: 1.5, w: 2.4, h: 0.4, fontSize: 20, fontFace: "Calibri", bold: true, color: item.tc, align: "center" });
  s.addText(item.rate, { x: x+0.1, y: 2.65, w: 2.6, h: 0.8, fontSize: 36, fontFace: "Calibri", bold: true, color: item.rc, align: "center" });
});
```

---

### 樣式五：多欄結構與路徑型 (Multi-Column Path & Matrix Layouts)
* **用途**：三條軸線路徑、六宮格職務技能矩陣 (3×2)
```javascript
// 5.1 6宮格職務矩陣 (3x2)
roles.forEach((r, i) => {
  const col = i % 3, row = Math.floor(i / 3);
  const x = 0.5 + col * 3.05, y = 1.2 + row * 1.9;
  s.addShape(pres.shapes.RECTANGLE, { x, y, w: 2.9, h: 1.75, fill: { color: C.white }, shadow: makeShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x, y, w: 2.9, h: 0.4, fill: { color: C.deepBrown } });
  s.addText(r.title, { x: x+0.1, y, w: 2.7, h: 0.4, fontSize: 13, fontFace: "Calibri", bold: true, color: C.gold });
});
```

---

### 樣式六：故事敘事與流程時間軸型 (Narrative & Timeline Layouts)
* **用途**：4 階段時間軸 (Roadmap)、人物對比側寫、π型人才運算公式
```javascript
// 6.1 π型人才運算公式 (原專業 + AI工具 = 賦能後)
s.addText("＋", { x: 3.3, y: 2.3, w: 0.4, h: 0.8, fontSize: 32, fontFace: "Calibri", bold: true, color: C.gold, align: "center" });
s.addText("＝", { x: 6.5, y: 2.3, w: 0.4, h: 0.8, fontSize: 32, fontFace: "Calibri", bold: true, color: C.gold, align: "center" });
```

---

### 樣式七：行動指南與結尾型 (Actionable Steps & Closing Layouts)
* **用途**：STEP 1~3 行動卡片、結尾頁
```javascript
// 7.1 STEP 1~3 行動卡片 (深棕背景)
steps3.forEach((item, i) => {
  const x = 0.6 + i * 3.0;
  s.addShape(pres.shapes.RECTANGLE, { x, y: 1.6, w: 2.8, h: 3.3, fill: { color: C.white, transparency: 95 }, line: { color: C.gold, width: 1.5 } });
  s.addText(item.st, { x, y: 1.8, w: 2.8, h: 0.4, fontSize: 18, fontFace: "Calibri", bold: true, color: C.gold, align: "center" });
});
```

---

## 📋 QA 檢查與檔名輸出規範

- **輸出檔名**：`問大師_[主題]_[YYYYMMDD].pptx`
- **QA 驗證**：產出後必須檢查：
  - [ ] 每頁底部有金黃底線 (`y: 5.5, h: 0.125`)
  - [ ] 米白底頁面 Logo 精確位於 `x: 8.1, y: 5.14, w: 1.5, h: 0.292` 且零遮擋
  - [ ] 深棕底頁面不放置 Logo
  - [ ] 字體無溢出或卡片重疊
