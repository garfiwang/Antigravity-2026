# 🕳️ 實戰踩坑紀錄與排錯指南 (Troubleshooting & Pitfalls)

本指南記錄在實際開發與部署「Google Apps Script (GAS) 活動線上報名與現場掃碼簽到系統」過程中遭遇的真實陷阱與最佳解決方案。

---

## 坑 1：Web App 權限設定錯誤引發 Google 登入牆與多帳號切換錯誤

### 🔴 問題現象
- 一般民眾點擊報名或簽到短網址時，出現錯誤畫面：  
  `很抱歉，目前無法開啟這個檔案。請檢查網址並再試一次。`
- 或是瀏覽器自動將網址重導向至 Google 帳號切換或登入頁面（網址帶有 `/u/2/`、`/ServiceLogin`），要求訪客登入 Google 帳號。

### 🔍 根本原因
在 Google Apps Script 中，`appsscript.json` 的 `webapp.access` 欄位若設為 `"ANYONE"`，Google 會要求訪客「必須具備並登入 Google 帳號」；一旦訪客未登入、使用無痕模式，或是瀏覽器同時登入多個 Google 帳號，就會撞上 Google 帳號授權限制與帳號切換重導向 bug。

### 💡 解決方案
必須在 `appsscript.json` 明確設定為 **`"ANYONE_ANONYMOUS"`** 與 `"executeAs": "USER_DEPLOYING"`：

```json
{
  "webapp": {
    "executeAs": "USER_DEPLOYING",
    "access": "ANYONE_ANONYMOUS"
  }
}
```

* **`USER_DEPLOYING`**：後端腳本以主辦人（部署者）的身分在雲端執行，負責寫入試算表與呼叫 MailApp 發信。
* **`ANYONE_ANONYMOUS`**：允許任何人（包含未登入 Google 帳號的匿名訪客）存取，大眾無需任何登入或授權！

---

## 坑 2：clasp 建立部署與初次部署 OAuth 授權機制

### 🔴 問題現象
全新建立的 Apps Script 專案透過 CLI (`clasp create-deployment`) 部署後，未登入的訪客或 curl 請求可能收到 `HTTP 403` 或「需要存取權」的 Google Drive 錯誤頁面。

### 🔍 根本原因
Google 安全政策規定：若指令碼內含有敏感權限（例如存取試算表 `spreadsheets`、發送信件 `script.send_mail`），專案擁有者必須在 Google 官方介面上至少執行或授權過一次，Google 才會簽發後端執行憑證。

### 💡 解決方案
主辦人首次在瀏覽器中開啟 Web App 網址或 Apps Script 編輯器，會看到安全提示：
1. 點擊「**審查權限 (Review Permissions)**」。
2. 點擊左下角「**進階 (Advanced)**」。
3. 點擊「**前往〈您的專案名稱〉（不安全）**」。
4. 點擊「**允許 (Allow)**」。

> **注意**：這僅需主辦人進行一次！完成後，所有外部民眾掃描 QR Code 或開啟短網址時，皆不需要登入、不會看到任何授權提示。

---

## 坑 3：Web App 網址不可自己手拼（scriptId vs deploymentId）

### 🔴 問題現象
自行拼裝網址 `https://script.google.com/macros/s/<scriptId>/exec` 永遠回傳 404 或「找不到網頁」。

### 🔍 根本原因
clasp 中有三個完全不同的 ID：
1. **`scriptId`**：Apps Script 專案原始碼的 ID（用於 `clasp open-script`）。
2. **`parentId`**：綁定的 Google 試算表 ID（用於 `clasp open-container`）。
3. **`deploymentId`**：部署版本的 ID，網頁應用程式網址必須由 deploymentId 經由 Google API 回傳。

### 💡 解決方案
嚴禁用 scriptId 手拼網址，一律透過指令取得真實經由 API 發布的網址：
```bash
npx @google/clasp open-web-app <deploymentId> --json
```

---

## 坑 4：單一 GAS 專案實現「前台報名 + 現場簽到」雙路由

### 🔴 問題現象
傳統做法需要建立「報名專案」與「現場簽到專案」兩套 Apps Script，造成試算表共用權限繁瑣、多個 Web App 需反覆授權。

### 💡 解決方案
利用 `doGet(e)` 的路由參數，在單一專案內支援前台報名與現場簽到雙介面：

```javascript
function doGet(e) {
  // 若網址帶有 ?page=checkin，開啟現場簽到表
  if (e && e.parameter && e.parameter.page === 'checkin') {
    return HtmlService.createHtmlOutputFromFile('checkin')
      .setTitle('來賓現場簽到')
      .addMetaTag('viewport', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no')
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
  }

  // 預設開啟線上預約報名表
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('活動線上報名單')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}
```

* 報名短網址：指向 `<WEB_APP_URL>`
* 現場簽到短網址：指向 `<WEB_APP_URL>?page=checkin`

---

## 坑 5：行前提醒自動排程觸發器未啟動

### 🔴 問題現象
如果主辦人忘記手動到 Google Apps Script 介面新增定時觸發器，活動前一天傍晚不會自動發送行前提醒信。

### 💡 解決方案
在 `submitRegistration()` 中加入 `ensureReminderTrigger()` 自動保證機制：

```javascript
function ensureReminderTrigger() {
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === 'sendWorkshopReminderEmail') {
      return 'Trigger already exists';
    }
  }

  // 設定於活動前一天 18:00 (台北時間)
  var reminderDate = new Date(2026, 9, 21, 18, 0, 0);
  ScriptApp.newTrigger('sendWorkshopReminderEmail')
    .timeBased()
    .at(reminderDate)
    .create();

  Logger.log('Auto created reminder trigger for: ' + reminderDate);
}
```

每次有民眾報名或主辦人測試時，程式會自動檢查並註冊該觸發器，達成真正的**「零人工干預」全自動化**。

---

## 坑 6：現場重複簽到與同行友人代簽處置

### 🔴 問題現象
活動現場來賓常有一人代簽同行親友的需求，或是手機訊號不良時重複點擊按鈕。

### 💡 解決方案
1. **前端防呆**：按下送出後立即進入 Disabled 狀態並顯示 Spinner 動畫，防止短時間重複連點。
2. **切換成功卡片**：簽到完成後跳出綠色打勾卡片，並提供 **「➕ 替同行友人簽到」** 按鈕，點擊後清空輸入框並自動 Focus，同行親友可流暢依序簽到。
3. **後台智慧雙軌記錄**：
   * 主表 `gid=0`：更新現有列第 10 欄並高亮淺綠底色。
   * 現場簽到分頁：依實際進場順序新增流水列，完整保留每一次到場紀錄。
