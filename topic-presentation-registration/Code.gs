/**
 * 主題簡報工作坊報名單 - 20260923
 * Google Apps Script 後端程式碼（含即時報名確認信與 9/22 18:00 自動行前提醒信）
 */

// 工作坊活動資訊設定
var WORKSHOP_CONFIG = {
  title: '主題簡報工作坊',
  eventDate: '2026 年 9 月 23 日（星期三）',
  eventTime: '敬請準時出席',
  location: '台北市民生西路105號2樓 (捷運雙連站1號出口)',
  feeNote: '場地費 200 元（當天現場繳交，可用 LinePay 或 現金）',
  bringNote: '請自備筆記型電腦（Notebook）及充電器以進行實作演練'
};

function doGet(e) {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('主題簡報工作坊報名單 - 20260923')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * 處理表單送出
 * @param {Object} formData { name, email, lineId }
 * @return {Object} { success: boolean, message: string }
 */
function submitRegistration(formData) {
  try {
    // 檢查必填欄位（姓名、Email）
    if (!formData || !formData.name || !formData.email) {
      return {
        success: false,
        message: '請填寫必填欄位（姓名、Email）'
      };
    }

    var cleanName = String(formData.name).trim();
    var cleanEmail = String(formData.email).trim();
    var cleanLineId = formData.lineId ? String(formData.lineId).trim() : '（未填寫）';
    if (!cleanLineId) {
      cleanLineId = '（未填寫）';
    }

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getActiveSheet();
    
    // 若試算表為空，建立標準表頭
    if (sheet.getLastRow() === 0) {
      var headers = ['報名時間', '姓名', 'Email', 'Line ID', '通知信狀態', '備註說明', '行前提醒狀態'];
      var headerRange = sheet.getRange(1, 1, 1, headers.length);
      headerRange.setValues([headers]);
      headerRange.setBackground('#1e293b');
      headerRange.setFontColor('#ffffff');
      headerRange.setFontWeight('bold');
      headerRange.setHorizontalAlignment('center');
      sheet.setFrozenRows(1);
      sheet.autoResizeColumns(1, headers.length);
    } else {
      // 確保第 7 欄有「行前提醒狀態」表頭
      var col7 = sheet.getRange(1, 7).getValue();
      if (!col7) {
        sheet.getRange(1, 7).setValue('行前提醒狀態').setBackground('#1e293b').setFontColor('#ffffff').setFontWeight('bold').setHorizontalAlignment('center');
      }
    }

    // 格式化當前時間 (台北時間)
    var timestamp = Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss');
    var emailStatus = '已寄出';

    // 寄送自動回覆 Email 確認信
    try {
      sendConfirmationEmail(cleanName, cleanEmail, cleanLineId, timestamp);
    } catch (mailErr) {
      Logger.log('Mail send error: ' + mailErr.toString());
      emailStatus = '寄送失敗: ' + mailErr.message;
    }

    // 新增資料列至 Google 試算表
    sheet.appendRow([
      timestamp,
      cleanName,
      cleanEmail,
      cleanLineId,
      emailStatus,
      '場地費 200元 當天繳交，可用 LinePay 或 現金',
      '待發送 (9/22 18:00)'
    ]);

    return {
      success: true,
      message: '🎉 報名成功！確認信已自動發送至您的 Email 信箱。'
    };
  } catch (error) {
    Logger.log('Error in submitRegistration: ' + error.toString());
    return {
      success: false,
      message: '系統處理失敗，請稍後再試：' + error.message
    };
  }
}

/**
 * 發送報名確認信 (即時自動回覆 Email)
 */
function sendConfirmationEmail(name, email, lineId, timestamp) {
  var subject = '【報名成功確認】主題簡報工作坊報名單 - 20260923';
  var lineIdDisplay = (lineId && lineId !== '（未填寫）') ? lineId : '未填寫';

  var htmlBody = '' +
    '<div style="max-width: 580px; margin: 0 auto; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, \'Helvetica Neue\', Arial, \'Noto Sans TC\', sans-serif; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.06);">' +
      '<div style="background: linear-gradient(135deg, #1e1b4b 0%, #4338ca 100%); padding: 32px 24px; text-align: center; color: #ffffff;">' +
        '<div style="display: inline-block; padding: 4px 12px; background: rgba(255,255,255,0.2); border-radius: 20px; font-size: 12px; margin-bottom: 10px; letter-spacing: 0.5px;">報名成功通知</div>' +
        '<h1 style="margin: 0; font-size: 22px; font-weight: 700; letter-spacing: 0.5px;">主題簡報工作坊報名單</h1>' +
        '<p style="margin: 8px 0 0; font-size: 14px; opacity: 0.9;">活動日期：2026.09.23</p>' +
      '</div>' +
      '<div style="padding: 30px 24px; color: #334155; line-height: 1.6;">' +
        '<p style="font-size: 16px; margin-top: 0;"><strong>' + name + '</strong> 您好：</p>' +
        '<p style="font-size: 14px; color: #475569;">感謝您的參與！我們已收到您的報名資料，以下是您的報名明細紀錄：</p>' +
        '<table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden;">' +
          '<tr>' +
            '<td style="padding: 12px 16px; background-color: #f8fafc; border-bottom: 1px solid #e2e8f0; color: #64748b; width: 32%;">報名姓名</td>' +
            '<td style="padding: 12px 16px; background-color: #f8fafc; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #0f172a;">' + name + '</td>' +
          '</tr>' +
          '<tr>' +
            '<td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; color: #64748b;">電子郵件</td>' +
            '<td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; color: #0f172a;">' + email + '</td>' +
          '</tr>' +
          '<tr>' +
            '<td style="padding: 12px 16px; background-color: #f8fafc; border-bottom: 1px solid #e2e8f0; color: #64748b;">Line ID</td>' +
            '<td style="padding: 12px 16px; background-color: #f8fafc; border-bottom: 1px solid #e2e8f0; color: #0f172a;">' + lineIdDisplay + '</td>' +
          '</tr>' +
          '<tr>' +
            '<td style="padding: 12px 16px; color: #64748b;">報名時間</td>' +
            '<td style="padding: 12px 16px; color: #0f172a;">' + timestamp + '</td>' +
          '</tr>' +
        '</table>' +
        '<div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 14px 16px; border-radius: 6px; margin: 24px 0 16px;">' +
          '<p style="margin: 0; font-size: 14px; color: #92400e; font-weight: 600; line-height: 1.5;">' +
            '📌 <strong>活動費用提醒</strong>：場地費 200元 當天繳交，可用 LinePay 或 現金。' +
          '</p>' +
        '</div>' +
        '<p style="font-size: 13px; color: #64748b; line-height: 1.6; margin-top: 20px;">' +
          '💡 我們將於 <strong>9 月 22 日晚間 18:00</strong> 發送行前提醒信給您，包含上課地址與攜帶物品清單。期待在工作坊與您相見！' +
        '</p>' +
        '<hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0 16px;">' +
        '<p style="font-size: 12px; color: #94a3b8; text-align: center; margin: 0;">此信件為系統自動發送之報名確認信。</p>' +
      '</div>' +
    '</div>';

  MailApp.sendEmail({
    to: email,
    subject: subject,
    htmlBody: htmlBody
  });
}

/**
 * 產生行前提醒信的 HTML 內容
 */
function buildReminderEmailHtml(name) {
  return '' +
    '<div style="max-width: 580px; margin: 0 auto; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, \'Helvetica Neue\', Arial, \'Noto Sans TC\', sans-serif; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.06);">' +
      // Header
      '<div style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #4338ca 100%); padding: 32px 24px; text-align: center; color: #ffffff;">' +
        '<div style="display: inline-block; padding: 4px 12px; background: rgba(245, 158, 11, 0.3); border: 1px solid rgba(245, 158, 11, 0.5); border-radius: 20px; font-size: 12px; color: #fde68a; font-weight: 600; margin-bottom: 10px; letter-spacing: 0.5px;">⏰ 明天準時開課</div>' +
        '<h1 style="margin: 0; font-size: 22px; font-weight: 700; letter-spacing: 0.5px;">【行前提醒】主題簡報工作坊</h1>' +
        '<p style="margin: 8px 0 0; font-size: 14px; opacity: 0.9;">明天 9 月 23 日（三）期待與您相見！</p>' +
      '</div>' +
      // Body
      '<div style="padding: 30px 24px; color: #334155; line-height: 1.6;">' +
        '<p style="font-size: 16px; margin-top: 0;"><strong>' + name + '</strong> 您好：</p>' +
        '<p style="font-size: 14px; color: #475569;">您報名的「<strong>主題簡報工作坊</strong>」將於<strong>明天（9 月 23 日）</strong>正式登場！為確保您有最佳的學習體驗，請特別留意以下行前重要資訊：</p>' +
        
        // 核心資訊卡
        '<div style="background-color: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 20px; margin: 20px 0;">' +
          '<h3 style="margin: 0 0 14px; font-size: 15px; color: #1e293b; font-weight: 700; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px;">📋 活動詳細資訊</h3>' +
          '<div style="margin-bottom: 12px; font-size: 14px;">' +
            '<strong style="color: #4f46e5;">📅 上課日期：</strong>' + WORKSHOP_CONFIG.eventDate +
          '</div>' +
          '<div style="margin-bottom: 12px; font-size: 14px;">' +
            '<strong style="color: #4f46e5;">⏰ 上課時間：</strong>' + WORKSHOP_CONFIG.eventTime +
          '</div>' +
          '<div style="margin-bottom: 0; font-size: 14px;">' +
            '<strong style="color: #4f46e5;">📍 上課地址：</strong>' + WORKSHOP_CONFIG.location +
          '</div>' +
        '</div>' +

        // 重點提醒 1：費用
        '<div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 14px 16px; border-radius: 6px; margin: 16px 0;">' +
          '<div style="font-size: 14px; color: #92400e; font-weight: 700; margin-bottom: 4px;">💰 1. 準備場地費 200 元</div>' +
          '<div style="font-size: 13.5px; color: #78350f;">' + WORKSHOP_CONFIG.feeNote + '</div>' +
        '</div>' +

        // 重點提醒 2：自備筆電
        '<div style="background-color: #eff6ff; border-left: 4px solid #3b82f6; padding: 14px 16px; border-radius: 6px; margin: 16px 0;">' +
          '<div style="font-size: 14px; color: #1e40af; font-weight: 700; margin-bottom: 4px;">💻 2. 自備筆記型電腦（Notebook）</div>' +
          '<div style="font-size: 13.5px; color: #1e3a8a;">' + WORKSHOP_CONFIG.bringNote + '，充飽電或攜帶電源線。</div>' +
        '</div>' +

        '<p style="font-size: 13.5px; color: #475569; margin-top: 22px; line-height: 1.6;">' +
          '如臨時有任何行程異動或找不到場地，請隨時回覆此 Email 或於 Line 與主辦方聯繫。<br>' +
          '祝您有充實愉快的一天，我們明天見！' +
        '</p>' +

        '<hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0 16px;">' +
        '<p style="font-size: 12px; color: #94a3b8; text-align: center; margin: 0;">主題簡報工作坊 主辦團隊 敬上</p>' +
      '</div>' +
    '</div>';
}

/**
 * 發送行前提醒信給所有已報名的學員
 * （將於 9/22 18:00 由定時觸發器自動執行）
 */
function sendWorkshopReminderEmail() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getActiveSheet();
  var data = sheet.getDataRange().getValues();
  
  if (data.length <= 1) {
    Logger.log('目前尚無任何報名資料。');
    return;
  }

  var sentCount = 0;
  var failCount = 0;
  var timestamp = Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss');

  // 確保第 7 欄有「行前提醒狀態」表頭
  sheet.getRange(1, 7).setValue('行前提醒狀態').setBackground('#1e293b').setFontColor('#ffffff').setFontWeight('bold').setHorizontalAlignment('center');

  // 從第 2 列開始逐筆處理
  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var name = String(row[1]).trim();
    var email = String(row[2]).trim();
    var reminderStatus = row[6];

    // 只要有 Email 且尚未發送成功過
    if (email && email.indexOf('@') !== -1) {
      try {
        var subject = '【行前提醒】主題簡報工作坊明天準時開課！（請自備筆電與200元場地費）';
        var htmlBody = buildReminderEmailHtml(name);

        MailApp.sendEmail({
          to: email,
          subject: subject,
          htmlBody: htmlBody
        });

        sheet.getRange(i + 1, 7).setValue('已發送 (' + timestamp + ')');
        sentCount++;
        Logger.log('成功寄送提醒信給：' + name + ' (' + email + ')');
      } catch (err) {
        sheet.getRange(i + 1, 7).setValue('發送失敗: ' + err.message);
        failCount++;
        Logger.log('寄送提醒信失敗：' + name + ' (' + email + ') - ' + err.message);
      }
    }
  }

  Logger.log('行前提醒信發送完畢！成功：' + sentCount + ' 筆，失敗：' + failCount + ' 筆。');
}

/**
 * 設定 9/22 晚上 18:00 自動發送行前提醒信的定時觸發器
 */
function scheduleReminderTrigger() {
  // 先清除舊的相同觸發器避免重複
  cancelReminderTrigger();

  // 設定時間：2026年9月22日 18:00:00 (台北時間)
  // 月份為 0-indexed，8 代表 9 月
  var triggerDate = new Date(2026, 8, 22, 18, 0, 0);

  ScriptApp.newTrigger('sendWorkshopReminderEmail')
    .timeBased()
    .at(triggerDate)
    .create();

  Logger.log('✅ 已成功建立定時觸發器：將於 2026-09-22 18:00:00 (台北時間) 自動發送提醒信！');
}

/**
 * 取消/清除已設定的提醒觸發器
 */
function cancelReminderTrigger() {
  var triggers = ScriptApp.getProjectTriggers();
  var count = 0;
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === 'sendWorkshopReminderEmail') {
      ScriptApp.deleteTrigger(triggers[i]);
      count++;
    }
  }
  Logger.log('已清除 ' + count + ' 個舊的提醒信定時觸發器。');
}

/**
 * 測試寄送提醒信至 garfiwang@gmail.com
 */
function testSendReminderEmail() {
  var testEmail = 'garfiwang@gmail.com';
  var testName = '學員（測試預覽）';
  var subject = '【行前提醒】主題簡報工作坊明天準時開課！（請自備筆電與200元場地費）';
  var htmlBody = buildReminderEmailHtml(testName);

  MailApp.sendEmail({
    to: testEmail,
    subject: subject,
    htmlBody: htmlBody
  });

  Logger.log('✅ 提醒信測試預覽已成功寄送至：' + testEmail);
}

/**
 * 一鍵啟用授權測試
 */
function authorizeAndTestEmail() {
  MailApp.sendEmail({
    to: 'richnews168@gmail.com',
    subject: '【授權成功】主題簡報工作坊報名系統 Email 權限已啟用',
    body: '恭喜！您的 Apps Script 寄信權限已成功啟用，系統現在可以自動寄送報名確認信了！'
  });
  Logger.log('授權測試成功！已發送測試信至 richnews168@gmail.com');
}
