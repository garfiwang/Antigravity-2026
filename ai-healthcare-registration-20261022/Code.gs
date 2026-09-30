/**
 * AI 照護大健康講座 報名系統
 * 活動主題：科技賦能，精準健康
 * 時間：10月22日 (週六) 14:00 - 16:00
 * 地點：敦化北路168號1樓體驗館
 * 費用：每位 $400（含檢測及下午茶）
 */

var EVENT_CONFIG = {
  title: 'AI 照護大健康講座',
  subtitle: '科技賦能，精準健康',
  eventDate: '10月22日 (週六)',
  eventTime: '14:00 - 16:00（13:45 開放報到入場）',
  venue: '敦化北路168號1樓體驗館',
  address: '台北市松山區敦化北路168號1樓',
  mapUrl: 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent('台北市松山區敦化北路168號'),
  feeNote: '每位 $400（含現場健康檢測及精緻下午茶，當天現場報到繳交）',
  highlights: [
    '🤖 科技賦能：AI 智慧照護與精準健康趨勢解析',
    '⌚ 健康檢測：現場穿戴式科技與生理數據體驗',
    '☕ 精緻下午茶：輕鬆自在的交流茶敘與答疑'
  ],
  contactNote: '若有任何問題，歡迎隨時回覆此信件或於報到處洽詢現場工作人員。'
};

function doGet(e) {
  if (e && e.parameter && (e.parameter.page === 'checkin' || e.parameter.action === 'checkin')) {
    return HtmlService.createHtmlOutputFromFile('checkin')
      .setTitle('來賓現場簽到 — AI 照護大健康講座')
      .addMetaTag('viewport', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no')
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
  }

  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('AI 照護大健康講座 報名單')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * 處理報名表單送出
 * @param {Object} formData { name, phone, email, lineId, remarks }
 * @return {Object} { success: boolean, message: string }
 */
function submitRegistration(formData) {
  try {
    if (!formData || !formData.name) {
      return {
        success: false,
        message: '請填寫姓名！'
      };
    }

    var cleanName = String(formData.name).trim();
    if (!cleanName) {
      return {
        success: false,
        message: '請填寫姓名！'
      };
    }

    var cleanPhone = formData.phone ? String(formData.phone).trim() : '（未填寫）';
    if (!cleanPhone) cleanPhone = '（未填寫）';

    var cleanEmail = formData.email ? String(formData.email).trim() : '';
    var cleanLineId = formData.lineId ? String(formData.lineId).trim() : '（未填寫）';
    if (!cleanLineId) cleanLineId = '（未填寫）';

    var cleanRemarks = formData.remarks ? String(formData.remarks).trim() : '無特殊備註';
    if (!cleanRemarks) cleanRemarks = '無特殊備註';

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getActiveSheet();

    // 初始化表頭
    if (sheet.getLastRow() === 0) {
      var headers = ['報名時間', '姓名', '聯絡電話', 'Email', 'Line ID', '費用狀態', '通知信狀態', '備註與期待', '行前提醒狀態'];
      var headerRange = sheet.getRange(1, 1, 1, headers.length);
      headerRange.setValues([headers]);
      headerRange.setBackground('#0284c7');
      headerRange.setFontColor('#ffffff');
      headerRange.setFontWeight('bold');
      headerRange.setHorizontalAlignment('center');
      sheet.setFrozenRows(1);
      sheet.autoResizeColumns(1, headers.length);
    }

    var timestamp = Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss');
    var emailStatus = '未填寫（無需寄送）';

    // 若有填寫 Email，發送自動報名確認信
    if (cleanEmail && cleanEmail.indexOf('@') !== -1) {
      try {
        sendConfirmationEmail(cleanName, cleanPhone, cleanEmail, cleanLineId, cleanRemarks, timestamp);
        emailStatus = '已寄出';
      } catch (mailErr) {
        Logger.log('Mail send error: ' + mailErr.toString());
        emailStatus = '寄送失敗: ' + mailErr.message;
      }
    }

    var reminderInitStatus = (cleanEmail && cleanEmail.indexOf('@') !== -1) ? '待排程發送' : '無Email（免發送）';

    // 寫入 Google Sheet
    sheet.appendRow([
      timestamp,
      cleanName,
      cleanPhone,
      cleanEmail ? cleanEmail : '（未填寫）',
      cleanLineId,
      '每位 $400 (現場繳交)',
      emailStatus,
      cleanRemarks,
      reminderInitStatus
    ]);

    // 自動確保行前提醒定時觸發器已建立 (活動前一天 10/21 18:00)
    try {
      ensureReminderTrigger();
    } catch (trigErr) {
      Logger.log('Auto trigger check notice: ' + trigErr.toString());
    }

    var successMsg = (cleanEmail && cleanEmail.indexOf('@') !== -1)
      ? '報名成功！確認信件已同步寄送至您的電子信箱。'
      : '報名成功！活動當天請直接至現場 1 樓報到處核對姓名入場。';

    return {
      success: true,
      message: successMsg,
      data: {
        name: cleanName,
        phone: cleanPhone,
        email: cleanEmail,
        eventDate: EVENT_CONFIG.eventDate,
        eventTime: EVENT_CONFIG.eventTime,
        venue: EVENT_CONFIG.venue,
        address: EVENT_CONFIG.address,
        feeNote: EVENT_CONFIG.feeNote
      }
    };
  } catch (error) {
    Logger.log('submitRegistration Error: ' + error.toString());
    return {
      success: false,
      message: '報名處理失敗：' + error.message
    };
  }
}

/**
 * 寄送報名確認信
 */
function sendConfirmationEmail(name, phone, email, lineId, remarks, timestamp) {
  var subject = '【報名成功確認】AI 照護大健康講座（科技賦能，精準健康）';
  var htmlBody = buildConfirmationEmailHtml(name, phone, email, lineId, remarks, timestamp);

  MailApp.sendEmail({
    to: email,
    subject: subject,
    htmlBody: htmlBody,
    name: 'AI 照護大健康講座 主辦團隊'
  });
}

/**
 * 建構報名確認信 HTML
 */
function buildConfirmationEmailHtml(name, phone, email, lineId, remarks, timestamp) {
  return '<!DOCTYPE html>' +
    '<html>' +
    '<head>' +
    '<meta charset="UTF-8">' +
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">' +
    '<title>報名成功確認信</title>' +
    '</head>' +
    '<body style="margin:0; padding:0; background-color:#f0f9ff; font-family:-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, \'Helvetica Neue\', Arial, sans-serif; color:#1e293b; -webkit-font-smoothing:antialiased;">' +
    '<table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed; background-color:#f0f9ff; padding:24px 12px;">' +
    '<tr><td align="center">' +
    '<table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:580px; background-color:#ffffff; border-radius:18px; overflow:hidden; box-shadow:0 10px 25px rgba(2, 132, 199, 0.08); border:1px solid #e0f2fe;">' +
    
    // Header Banner
    '<tr>' +
    '<td style="background: linear-gradient(135deg, #0284c7 0%, #06b6d4 100%); padding:32px 24px; text-align:center; color:#ffffff;">' +
    '<div style="font-size:13px; font-weight:700; letter-spacing:2px; text-transform:uppercase; background:rgba(255,255,255,0.2); display:inline-block; padding:4px 12px; border-radius:20px; margin-bottom:12px;">AI HEALTHCARE FORUM</div>' +
    '<h1 style="margin:0 0 8px 0; font-size:24px; font-weight:800; letter-spacing:0.5px; line-height:1.3;">' + EVENT_CONFIG.title + '</h1>' +
    '<p style="margin:0; font-size:15px; color:#e0f2fe; font-weight:500;">' + EVENT_CONFIG.subtitle + '</p>' +
    '</td>' +
    '</tr>' +
    
    // Content Body
    '<tr>' +
    '<td style="padding:28px 24px;">' +
    '<div style="font-size:16px; line-height:1.6; color:#0f172a; margin-bottom:20px;">' +
    '親愛的 <strong>' + name + '</strong> 您好：<br>' +
    '感謝您報名參加<strong>【' + EVENT_CONFIG.title + '】</strong>！您的報名資料已成功登記，我們非常期待當天與您見面交流。' +
    '</div>' +
    
    // Highlight Card
    '<div style="background-color:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; padding:16px; margin-bottom:24px;">' +
    '<div style="font-weight:700; color:#166534; font-size:14px; margin-bottom:8px;">🌟 本場活動雙重享受：</div>' +
    '<div style="font-size:13px; color:#15803d; line-height:1.6;">' +
    '• <strong>🩺 專業健康檢測</strong>：現場穿戴與生理數據體驗<br>' +
    '• <strong>☕ 精緻下午茶</strong>：精美茶點與咖啡，舒適自在交流' +
    '</div>' +
    '</div>' +
    
    // Event Details Table
    '<table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:#f8fafc; border-radius:14px; padding:18px; margin-bottom:24px; border:1px solid #e2e8f0;">' +
    '<tr><td style="padding:7px 0; font-size:14px; color:#64748b; width:80px; vertical-align:top;">📅 活動日期</td><td style="padding:7px 0; font-size:14px; font-weight:700; color:#0f172a;">' + EVENT_CONFIG.eventDate + '</td></tr>' +
    '<tr><td style="padding:7px 0; font-size:14px; color:#64748b; vertical-align:top;">⏰ 活動時間</td><td style="padding:7px 0; font-size:14px; font-weight:700; color:#0284c7;">' + EVENT_CONFIG.eventTime + '</td></tr>' +
    '<tr><td style="padding:7px 0; font-size:14px; color:#64748b; vertical-align:top;">📍 活動地點</td><td style="padding:7px 0; font-size:14px; font-weight:700; color:#0f172a;">' + EVENT_CONFIG.venue + '</td></tr>' +
    '<tr><td style="padding:7px 0; font-size:14px; color:#64748b; vertical-align:top;">🏢 詳細地址</td><td style="padding:7px 0; font-size:14px; color:#334155;">' + EVENT_CONFIG.address + '</td></tr>' +
    '<tr><td style="padding:7px 0; font-size:14px; color:#64748b; vertical-align:top;">💰 活動費用</td><td style="padding:7px 0; font-size:14px; font-weight:700; color:#e11d48;">' + EVENT_CONFIG.feeNote + '</td></tr>' +
    '</table>' +
    
    // Map Button
    '<div style="text-align:center; margin-bottom:24px;">' +
    '<a href="' + EVENT_CONFIG.mapUrl + '" target="_blank" style="display:inline-block; background-color:#0284c7; color:#ffffff; font-size:14px; font-weight:700; text-decoration:none; padding:12px 28px; border-radius:10px; box-shadow:0 4px 12px rgba(2, 132, 199, 0.25);">' +
    '📍 開啟 Google 地圖導航' +
    '</a>' +
    '</div>' +
    
    // Participant Info Box
    '<div style="border-top:1px dashed #cbd5e1; padding-top:18px; margin-bottom:18px;">' +
    '<div style="font-size:13px; font-weight:700; color:#475569; margin-bottom:8px;">📋 您的報名登記資料：</div>' +
    '<div style="font-size:13px; color:#64748b; line-height:1.7;">' +
    '• 參加者姓名：<strong>' + name + '</strong><br>' +
    '• 聯絡電話：<strong>' + phone + '</strong><br>' +
    '• 電子郵件：' + email + '<br>' +
    '• Line ID：' + lineId + '<br>' +
    '• 備註與期待：' + remarks + '<br>' +
    '• 登記時間：' + timestamp +
    '</div>' +
    '</div>' +
    
    // Footer Note
    '<div style="background-color:#eff6ff; border-radius:10px; padding:12px; font-size:12px; color:#1e40af; line-height:1.5;">' +
    '💡 溫馨提醒：活動前一天傍晚將會為您發送「行前提醒通知信」，敬請留意您的收件匣。若當天不克前往，請提早回信告知，以利保留名額予候補學員。' +
    '</div>' +
    
    '</td>' +
    '</tr>' +
    
    // Footer
    '<tr>' +
    '<td style="background-color:#f8fafc; padding:18px 24px; text-align:center; border-top:1px solid #e2e8f0; font-size:12px; color:#94a3b8;">' +
    '© 2026 AI 照護大健康講座 主辦團隊<br>科技賦能，精準健康' +
    '</td>' +
    '</tr>' +
    
    '</table>' +
    '</td></tr></table>' +
    '</body>' +
    '</html>';
}

/**
 * 確保行前提醒排程觸發器存在（活動前一天 10/21 18:00 自動寄發）
 */
function ensureReminderTrigger() {
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === 'sendWorkshopReminderEmail') {
      return 'Trigger already exists';
    }
  }

  // 設定 10月21日 18:00 台北時間
  var reminderDate = new Date(2026, 9, 21, 18, 0, 0); // 9 = 10月
  ScriptApp.newTrigger('sendWorkshopReminderEmail')
    .timeBased()
    .at(reminderDate)
    .create();

  Logger.log('Auto created reminder trigger for: ' + reminderDate);
  return 'Trigger created for ' + reminderDate;
}

/**
 * 排程設定：手動或強制重設行前提醒觸發器
 * 於活動前一天 18:00 自動寄出行前提醒
 */
function scheduleReminderTrigger() {
  // 清除舊觸發器
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === 'sendWorkshopReminderEmail') {
      ScriptApp.deleteTrigger(triggers[i]);
    }
  }

  // 設定 10月21日 18:00
  var reminderDate = new Date(2026, 9, 21, 18, 0, 0); // 月份 0-indexed, 9 = 10月
  ScriptApp.newTrigger('sendWorkshopReminderEmail')
    .timeBased()
    .at(reminderDate)
    .create();

  Logger.log('Reminder trigger scheduled for: ' + reminderDate.toString());
  return '行前提醒排程已成功設定於：' + Utilities.formatDate(reminderDate, 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss');
}

/**
 * 發送行前提醒信給所有已報名學員
 */
function sendWorkshopReminderEmail() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getActiveSheet();
  var data = sheet.getDataRange().getValues();

  if (data.length <= 1) {
    Logger.log('No registered participants found.');
    return;
  }

  var sendCount = 0;
  var sendTime = Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss');

  for (var r = 1; r < data.length; r++) {
    var name = data[r][1];
    var email = data[r][3] ? String(data[r][3]).trim() : '';
    var reminderStatus = String(data[r][8] || '');

    // 若未填寫 Email 或是預設佔位文字，跳過並標記
    if (!email || email.indexOf('@') === -1 || email === '（未填寫）') {
      if (!reminderStatus || reminderStatus === '待排程發送') {
        sheet.getRange(r + 1, 9).setValue('無Email（免發送）');
      }
      continue;
    }

    // 若尚未發送行前提醒
    if (reminderStatus.indexOf('已寄出') === -1) {
      try {
        var subject = '【行前提醒】明日「AI 照護大健康講座」出席須知（含檢測與精緻下午茶）';
        var htmlBody = buildReminderEmailHtml(name);

        MailApp.sendEmail({
          to: email,
          subject: subject,
          htmlBody: htmlBody,
          name: 'AI 照護大健康講座 主辦團隊'
        });

        sheet.getRange(r + 1, 9).setValue('已寄出 (' + sendTime + ')');
        sendCount++;
        Utilities.sleep(400); // 避免頻率限制
      } catch (err) {
        Logger.log('Failed to send reminder to ' + email + ': ' + err.toString());
        sheet.getRange(r + 1, 9).setValue('寄送失敗: ' + err.message);
      }
    }
  }

  Logger.log('Total reminders sent: ' + sendCount);
}

/**
 * 建構行前提醒信 HTML
 */
function buildReminderEmailHtml(name) {
  return '<!DOCTYPE html>' +
    '<html>' +
    '<head>' +
    '<meta charset="UTF-8">' +
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">' +
    '<title>行前提醒通知信</title>' +
    '</head>' +
    '<body style="margin:0; padding:0; background-color:#f0f9ff; font-family:-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, \'Helvetica Neue\', Arial, sans-serif; color:#1e293b;">' +
    '<table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout:fixed; background-color:#f0f9ff; padding:24px 12px;">' +
    '<tr><td align="center">' +
    '<table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:580px; background-color:#ffffff; border-radius:18px; overflow:hidden; box-shadow:0 10px 25px rgba(2, 132, 199, 0.08); border:1px solid #e0f2fe;">' +
    
    // Header
    '<tr>' +
    '<td style="background: linear-gradient(135deg, #0284c7 0%, #06b6d4 100%); padding:28px 24px; text-align:center; color:#ffffff;">' +
    '<div style="font-size:12px; font-weight:700; letter-spacing:2px; background:rgba(255,255,255,0.2); display:inline-block; padding:4px 12px; border-radius:20px; margin-bottom:10px;">REMINDER NOTICE</div>' +
    '<h1 style="margin:0 0 6px 0; font-size:22px; font-weight:800; line-height:1.3;">明日活動提醒：' + EVENT_CONFIG.title + '</h1>' +
    '<p style="margin:0; font-size:14px; color:#e0f2fe;">' + EVENT_CONFIG.subtitle + '</p>' +
    '</td>' +
    '</tr>' +
    
    // Body
    '<tr>' +
    '<td style="padding:24px;">' +
    '<div style="font-size:15px; line-height:1.6; color:#0f172a; margin-bottom:18px;">' +
    '親愛的 <strong>' + name + '</strong> 您好：<br>' +
    '明天就是期待已久的<strong>【' + EVENT_CONFIG.title + '】</strong>！主辦團隊期待與您相見，特此為您整理行前重要資訊：' +
    '</div>' +
    
    // Key Details Box
    '<div style="background-color:#f8fafc; border-radius:14px; padding:16px; margin-bottom:20px; border-left:4px solid #0284c7;">' +
    '<div style="font-size:14px; margin-bottom:6px;">📅 <strong>活動時間</strong>：' + EVENT_CONFIG.eventDate + ' ' + EVENT_CONFIG.eventTime + '</div>' +
    '<div style="font-size:14px; margin-bottom:6px;">📍 <strong>活動地點</strong>：' + EVENT_CONFIG.venue + '</div>' +
    '<div style="font-size:14px; margin-bottom:6px;">🏢 <strong>地點地址</strong>：' + EVENT_CONFIG.address + '</div>' +
    '<div style="font-size:14px; color:#e11d48;">💰 <strong>活動費用</strong>：' + EVENT_CONFIG.feeNote + '</div>' +
    '</div>' +
    
    // Map Button
    '<div style="text-align:center; margin-bottom:22px;">' +
    '<a href="' + EVENT_CONFIG.mapUrl + '" target="_blank" style="display:inline-block; background-color:#0284c7; color:#ffffff; font-size:14px; font-weight:700; text-decoration:none; padding:12px 24px; border-radius:10px;">' +
    '🧭 點我打開 Google Maps 路線導航' +
    '</a>' +
    '</div>' +
    
    // Warm Reminders
    '<div style="background-color:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; padding:16px; font-size:13px; color:#166534; line-height:1.6;">' +
    '<strong>💡 溫馨報到叮嚀：</strong><br>' +
    '1. 建議於 <strong>13:45 提早入場</strong> 完成報到與領取健康檢測識別。<br>' +
    '2. 現場備有健康檢測體驗與精緻下午茶，敬請攜帶好心情準時出席。<br>' +
    '3. 若臨時行程有變更無法出席，請提早回信告知工作團隊，謝謝！' +
    '</div>' +
    
    '</td>' +
    '</tr>' +
    
    // Footer
    '<tr>' +
    '<td style="background-color:#f8fafc; padding:16px; text-align:center; border-top:1px solid #e2e8f0; font-size:12px; color:#94a3b8;">' +
    '© 2026 AI 照護大健康講座 主辦團隊' +
    '</td>' +
    '</tr>' +
    
    '</table>' +
    '</td></tr></table>' +
    '</body>' +
    '</html>';
}

/**
 * 處理來賓現場掃碼簽到
 * @param {string} guestName 來賓大名
 * @return {Object} { success: boolean, message: string, data: Object }
 */
function submitCheckIn(guestName) {
  try {
    if (!guestName || !String(guestName).trim()) {
      return {
        success: false,
        message: '請輸入您的大名！'
      };
    }

    var cleanName = String(guestName).trim();
    var timestamp = Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss');
    var ss = SpreadsheetApp.getActiveSpreadsheet();

    // 1. 在主要報名工作表 (gid=0) 搜尋與註記簽到狀態
    var mainSheet = ss.getSheets()[0];
    var data = mainSheet.getDataRange().getValues();

    // 若主表為空，初始化標準表頭（包含第 10 欄：現場簽到狀態）
    if (mainSheet.getLastRow() === 0) {
      var headers = ['報名時間', '姓名', '聯絡電話', 'Email', 'Line ID', '費用狀態', '通知信狀態', '備註與期待', '行前提醒狀態', '現場簽到狀態'];
      var headerRange = mainSheet.getRange(1, 1, 1, headers.length);
      headerRange.setValues([headers]);
      headerRange.setBackground('#0284c7');
      headerRange.setFontColor('#ffffff');
      headerRange.setFontWeight('bold');
      headerRange.setHorizontalAlignment('center');
      mainSheet.setFrozenRows(1);
      data = mainSheet.getDataRange().getValues();
    } else {
      // 確保第 10 欄有「現場簽到狀態」表頭
      var col10 = mainSheet.getRange(1, 10).getValue();
      if (!col10) {
        mainSheet.getRange(1, 10)
          .setValue('現場簽到狀態')
          .setBackground('#0284c7')
          .setFontColor('#ffffff')
          .setFontWeight('bold')
          .setHorizontalAlignment('center');
      }
    }

    var isPreRegistered = false;
    var matchedRow = -1;

    // 比對欄位 2（姓名）
    for (var r = 1; r < data.length; r++) {
      var rowName = String(data[r][1]).trim();
      if (rowName === cleanName) {
        matchedRow = r + 1;
        isPreRegistered = true;
        break;
      }
    }

    if (isPreRegistered && matchedRow > 0) {
      // 找到事先報名者：更新簽到時間並加上柔和綠色標註
      mainSheet.getRange(matchedRow, 10).setValue('已簽到 (' + timestamp + ')');
      mainSheet.getRange(matchedRow, 1, 1, 10).setBackground('#f0fdf4');
    } else {
      // 現場直接前來未事先報名：新增一列至主表
      mainSheet.appendRow([
        timestamp,
        cleanName,
        '（現場簽到）',
        '（未填寫）',
        '（未填寫）',
        '每位 $400 (現場繳交)',
        '現場簽到',
        '現場直接簽到來賓',
        '無Email（免發送）',
        '已簽到 (' + timestamp + ')'
      ]);
      var lastRow = mainSheet.getLastRow();
      mainSheet.getRange(lastRow, 1, 1, 10).setBackground('#eff6ff');
    }

    // 2. 同步寫入專屬「現場簽到紀錄」工作表，依序號與時間清楚排序
    var checkInSheet = ss.getSheetByName('現場簽到紀錄');
    if (!checkInSheet) {
      checkInSheet = ss.insertSheet('現場簽到紀錄');
      var checkInHeaders = ['簽到序號', '簽到時間', '來賓大名', '預先報名狀態', '備註說明'];
      var chkHeaderRange = checkInSheet.getRange(1, 1, 1, checkInHeaders.length);
      chkHeaderRange.setValues([checkInHeaders]);
      chkHeaderRange.setBackground('#0f172a');
      chkHeaderRange.setFontColor('#ffffff');
      chkHeaderRange.setFontWeight('bold');
      chkHeaderRange.setHorizontalAlignment('center');
      checkInSheet.setFrozenRows(1);
    }

    var checkInSeq = Math.max(1, checkInSheet.getLastRow()); // 序號
    checkInSheet.appendRow([
      checkInSeq,
      timestamp,
      cleanName,
      isPreRegistered ? '已事先報名' : '現場直接前來',
      '現場簽到完成'
    ]);
    checkInSheet.autoResizeColumns(1, 5);

    return {
      success: true,
      message: '簽到成功！',
      data: {
        guestName: cleanName,
        checkInTime: timestamp,
        isPreRegistered: isPreRegistered
      }
    };
  } catch (error) {
    Logger.log('submitCheckIn Error: ' + error.toString());
    return {
      success: false,
      message: '簽到處理失敗：' + error.message
    };
  }
}
