---
name: event-registration-system
version: 1.0.0
description: 活動線上報名與現場掃碼簽到全自動系統。當使用者說「製作報名表單」、「製作報名連結」、「建立報名表」、「活動報名系統」、「現場簽到系統」時載入。包含前台自適應報名網頁、後台 Google 試算表（附短網址）、即時確認信與行前自動提醒信、現場來賓 QR Code 簽到（雙重智慧連動比對與獨立簽到分頁）、短網址與 QR Code 自動產生。
user-invocable: true
triggers:
  - 製作報名表單
  - 製作報名連結
  - 建立報名表
  - 現場簽到系統
  - 活動報名系統
author: 王執定 Rich <garfiwang@gmail.com>
license: MIT
changelog:
  - version: 1.0.0
    date: 2026-09-30
    note: 初始發布，整合 GAS 報名表單、後台試算表雙重連動、三合一短網址、報名與行前提醒 Email、現場快速 QR Code 簽到與圖檔自動彈出。
---

# 🎟️ 活動線上報名與現場掃碼簽到全自動系統技能

本技能專為任何線下實體講座、桌遊推演、工作坊或線上研討會設計，能**全自動建立前台報名、現場簽到、後台試算表資料庫、雙重 Email 發信，並產出短網址與高解析 QR Code**。

---

## 🚀 觸發條件
當使用者提及以下任何關鍵字時立即觸發：
- **「製作報名表單」**
- **「製作報名連結」**
- 「建立報名表」
- 「活動報名系統」
- 「現場簽到系統」
- 提供海報、活動文案要求「建立新的報名表」或「製作簽到表」

---

## 🎯 系統六大核心標準

### 1. 前台報名網頁（自適應、免登入）
* **免登入保證**：`appsscript.json` 必須設定 `"access": "ANYONE_ANONYMOUS"` 與 `"executeAs": "USER_DEPLOYING"`，一般大眾手機開啟完全不需 Google 帳號授權、免登入即可順暢報名。
* **視覺契合**：依活動海報調性客製設計（現代科技藍、高貴商務金、簡約白等），手機優先（Mobile-First）大字版排版。
* **彈性欄位規範**：
  * **姓名**：唯一必填（標示 `*`）
  * **聯絡手機 / 電話**：預設為 **(選填)**，若主辦人特別要求可切為必填
  * **電子信箱 Email**：預設為 **(選填)**，註明「填寫後將自動發送報名確認信與活動行前提醒」
  * **Line ID**：(選填)
  * **備註或期待學習事項**：(選填)

### 2. 雙重短網址與高解析 QR Code
* **報名專用短網址**：使用 Reurl 技能縮短。
* **報名專用 QR Code**：使用 `npx -y qrcode -w 600 -o qrcode.png` 產生 600px 高畫質圖檔，方便文案宣傳與印製傳單。

### 3. 雙重自動化通知信（Email）
* **① 報名成功確認信（即時發送）**：
  * 民眾填寫當下若有留 Email，系統即刻發送精美 HTML 確認信（含活動時間、地點、Google 地圖導航按鈕、現場費用說明）。
  * 若未留 Email，系統僅登記試算表，不發信亦不報錯。
* **② 活動行前提醒信（活動前一天 18:00 自動觸發）**：
  * 程式內建 `ensureReminderTrigger()`，只要有人報名（或主辦人測試），排程自動在 Google Apps Script 註冊定時觸發器。
  * 前一天傍晚 18:00 台北時間自動執行 `sendWorkshopReminderEmail`，只針對留有 Email 且尚未發送者寄出，寄出後於試算表自動標記 `已寄出 (時間戳記)`。

### 4. 後台報名試算表（Google 試算表）附短網址
* 使用 `clasp create-script --type sheets` 自動建立綁定試算表。
* 為後台試算表網址同步產生 Reurl 短網址，讓主辦團隊在手機 LINE 就能隨時點開查閱名冊。

### 5. 現場掃碼快速簽到系統（專屬頁面 + QR Code）
* **專用路由**：網址帶有 `?page=checkin`。
* **極簡介面**：只有 **「你的大名」** 輸入框（大字體、自動聚焦）與 **`<送出簽到>`** 按鈕。
* **成功卡片**：點擊後即刻切換為「🎉 報到成功！」視窗，顯示來賓大名、簽到時間、地點引導與活動小叮嚀，並提供「➕ 替同行友人簽到」按鈕。
* **現場短網址與 QR Code**：產出 `checkin_qrcode.png`，可直接列印放於迎賓報到櫃台。

### 6. 後台試算表雙重連動機制（智慧比對）
簽到資料送出時，系統自動執行**雙重連動**：
1. **主表（gid=0）智慧比對**：
   * 比對姓名：若是**已預先報名者**，在第 10 欄「現場簽到狀態」填入 `已簽到 (時間戳記)`，整列資料自動標註為**柔和淺綠色（`#f0fdf4`）**，一眼看出誰已抵達。
   * 若為**現場直接前來的未報名貴賓**，自動於主表最下方新增一列，標記為「現場簽到來賓」，整列以淺藍色（`#eff6ff`）標註。
2. **獨立「現場簽到紀錄」工作表分頁**：
   * 自動建立或維護該分頁，欄位為 `['簽到序號', '簽到時間', '來賓大名', '預先報名狀態', '備註說明']`。
   * 依實際進場先後順序以流水序號排序列出，方便前台櫃台統計實際到場人數。

---

## 🛠️ 執行 SOP（標準作業流程）

### 步驟 1：建立專案目錄並綁定 Google 試算表
```bash
# 專案名稱格式：[活動名稱英文/拼音]-registration-[YYYYMMDD]
mkdir -p /Users/garfiwang/Documents/Antigravity-2026/event-registration-2026xxxx
cd /Users/garfiwang/Documents/Antigravity-2026/event-registration-2026xxxx
npx -y @google/clasp create-script --type sheets --title "【活動名稱】報名表單"
```
從輸出紀錄取得：
- Google 試算表網址：`https://docs.google.com/spreadsheets/d/<PARENT_ID>/edit`
- Apps Script 網址：`https://script.google.com/d/<SCRIPT_ID>/edit`

---

### 步驟 2：配置 `appsscript.json`（關鍵免授權）
建立 `appsscript.json`：
```json
{
  "timeZone": "Asia/Taipei",
  "dependencies": {},
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "webapp": {
    "executeAs": "USER_DEPLOYING",
    "access": "ANYONE_ANONYMOUS"
  },
  "oauthScopes": [
    "https://www.googleapis.com/auth/script.send_mail",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/forms",
    "https://www.googleapis.com/auth/script.container.ui",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/script.scriptapp"
  ]
}
```

---

### 步驟 3：撰寫後端程式碼 `Code.gs`
`Code.gs` 必須具備以下核心架構：
1. `EVENT_CONFIG`：活動配置物件（標題、副標、日期、時間、地點、地址、導航 URL、費用、注意事項）。
2. `doGet(e)`：
   * 若 `e.parameter.page === 'checkin'`，渲染 `checkin.html`。
   * 預設渲染 `index.html`。
3. `submitRegistration(formData)`：
   * 姓名必填，電話與 Email 選填。
   * 若有 Email 發送確認信，記錄發信狀態。
   * 自動呼叫 `ensureReminderTrigger()` 確保前一天 18:00 定時觸發器已就緒。
   * 寫入主表並回傳報名結果。
4. `submitCheckIn(guestName)`（雙重連動）：
   * 搜尋主表姓名：找到則更新第 10 欄為 `已簽到 (時間)` 並標記淺綠底色。
   * 未找到則新增一列現場來賓列。
   * 同步寫入「現場簽到紀錄」分頁（序號、時間、大名、是否預先報名）。
5. `ensureReminderTrigger()` 與 `sendWorkshopReminderEmail()`：自動提醒機制。

---

### 步驟 4：撰寫前端頁面 `index.html` 與 `checkin.html`
* `index.html`：報名頁面，包含活動詳情、地圖導航按鈕、姓名（必填）、手機（選填）、Email（選填）、Line ID（選填）、備註（選填）、送出按鈕、成功彈窗。
* `checkin.html`：現場簽到頁面，僅有「你的大名」輸入框與 `<送出簽到>` 按鈕，送出後切換為「報到成功卡片」，含「➕ 替同行友人簽到」按鈕。

---

### 步驟 5：推送與正式部署
```bash
# 1. 強制推送檔案
npx -y @google/clasp push --force

# 2. 建立正式部署
npx -y @google/clasp create-deployment --description "活動報名與現場簽到系統 v1"

# 3. 取得部署網址
npx -y @google/clasp open-web-app <DEPLOYMENT_ID> --json
```

---

### 步驟 6：生成短網址與 QR Code
```bash
# 1. 報名表短網址
python3 /Users/garfiwang/Documents/Antigravity-2026/.agents/skills/short-url/shorten.py "<WEB_APP_URL>"

# 2. 現場簽到短網址 (網址尾端加上 ?page=checkin)
python3 /Users/garfiwang/Documents/Antigravity-2026/.agents/skills/short-url/shorten.py "<WEB_APP_URL>?page=checkin"

# 3. 後台試算表短網址
python3 /Users/garfiwang/Documents/Antigravity-2026/.agents/skills/short-url/shorten.py "<SPREADSHEET_URL>"

# 4. 產生報名與現場簽到高解析 QR Code (600px)
npx -y qrcode -w 600 -o qrcode.png "<REG_SHORT_URL>"
npx -y qrcode -w 600 -o checkin_qrcode.png "<CHECKIN_SHORT_URL>"
```

---

### 步驟 7：自動預覽與成果回報
* 調用 macOS `open` 指令開啟圖檔預覽與資料夾。
* 輸出精準、專業、格式齊全的 LINE 宣傳邀請文案與系統後台連結清單。

---

## 📋 成果輸出標準回報格式

每次執行完畢後，必須依以下規格清楚回報使用者：

```markdown
### 🎟️【活動名稱】線上報名與現場簽到系統已建置完成！

#### 🔗 一、 系統連結總覽
* 📱 **線上預約報名短網址**：https://reurl.cc/xxxxxx
* 🖼️ **線上報名 QR Code 圖檔**：[qrcode.png](file:///...)
* 📍 **現場來賓簽到短網址**：https://reurl.cc/yyyyyy
* 🖼️ **現場簽到 QR Code 圖檔**：[checkin_qrcode.png](file:///...)
* 📊 **後台報名試算表（含短網址）**：https://reurl.cc/zzzzzz
  （原始網址：https://docs.google.com/spreadsheets/d/.../edit）

---

#### ⚙️ 二、 機制與連動說明
1. **免登入填表**：設定為 `ANYONE_ANONYMOUS`，一般民眾免登入 Google 即可秒填送出。
2. **雙重通知信**：
   - 即時發送：填寫 Email 之報名者將收到精美確認信（含活動時間、地點、導航）。
   - 行前提醒：系統已排定活動前一天傍晚 18:00 自動定時寄送。
3. **現場雙重簽到連動**：
   - 掃碼後輸入大名即可完成簽到。
   - 主表比對：已報名者自動於第 10 欄標記「已簽到 (時間)」並上綠色；現場直接來賓自動新增列並上淺藍色。
   - 獨立分頁：同步寫入「現場簽到紀錄」分頁，依到場序號清楚排列。

---

#### 📢 三、 最新 LINE 宣傳文案（可直接複製發送）
[提供吸睛的 LINE 宣傳文案]
```

---

## 👨‍💻 作者與版權聲明 (Author & Copyright)

* **技能製作人**：王執定 (Rich Wang)
* **電子信箱**：[garfiwang@gmail.com](mailto:garfiwang@gmail.com)
* **版權聲明**：Copyright © 2026 王執定 (Rich Wang). All rights reserved.
* **授權方式**：[MIT License](https://opensource.org/licenses/MIT)

