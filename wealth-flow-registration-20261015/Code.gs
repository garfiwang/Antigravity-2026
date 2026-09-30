/**
 * 財富流桌遊報名單 - 20261015
 * Google Apps Script 後端程式碼（含即時報名確認信與 10/14 18:00 自動行前提醒信）
 */

// 活動資訊設定
var EVENT_CONFIG = {
  title: '財富流桌遊',
  eventDate: '2026 年 10 月 15 日（星期四）',
  eventTime: '下午 14:00 - 17:00（請提早 10 分鐘報到入場）',
  venue: '寰宇商務中心VIP室',
  address: '台北市中山區復華里建國北路二段3巷15號4 樓 之 2',
  mapUrl: 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent('台北市中山區建國北路二段3巷15號4樓之2'),
  feeNote: '場地費 200 元（當天現場繳交，可用 LinePay 或 現金）',
  note: '一場推演、一次覺察！請準時出席以利完整體驗桌遊推演與覆盤流程。'
};

function doGet(e) {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('財富流桌遊 報名單 - 20261015')
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
      var headers = ['報名時間', '姓名', 'Email', 'Line ID', '通知信狀態', '活動備註', '行前提醒狀態'];
      var headerRange = sheet.getRange(1, 1, 1, headers.length);
      headerRange.setValues([headers]);
      headerRange.setBackground('#0f172a');
      headerRange.setFontColor('#ffffff');
      headerRange.setFontWeight('bold');
      headerRange.setHorizontalAlignment('center');
      sheet.setFrozenRows(1);
      sheet.autoResizeColumns(1, headers.length);
    } else {
      // 確保第 7 欄有「行前提醒狀態」表頭
      var col7 = sheet.getRange(1, 7).getValue();
      if (!col7) {
        sheet.getRange(1, 7).setValue('行前提醒狀態').setBackground('#0f172a').setFontColor('#ffffff').setFontWeight('bold').setHorizontalAlignment('center');
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
      '2026.10.15 14:00-17:00 | 寰宇商務中心VIP室 | 200元',
      '待發送 (10/14 18:00)'
    ]);

    return {
      success: true,
      message: '🎉 報名成功！活動確認信已發送至您的 Email 信箱。'
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
  var subject = '【報名成功確認】財富流桌遊 - 20261015（活動時間與地址提醒）';
  var lineIdDisplay = (lineId && lineId !== '（未填寫）') ? lineId : '未填寫';

  var htmlBody = '' +
    '<div style="max-width: 580px; margin: 0 auto; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, \'Helvetica Neue\', Arial, \'Noto Sans TC\', sans-serif; background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.06);">' +
      // Header
      '<div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #b45309 100%); padding: 32px 24px; text-align: center; color: #ffffff;">' +
        '<div style="display: inline-block; padding: 4px 14px; background: rgba(251, 191, 36, 0.2); border: 1px solid rgba(251, 191, 36, 0.4); border-radius: 20px; font-size: 13px; font-weight: 700; color: #fef3c7; margin-bottom: 10px; letter-spacing: 0.5px;">富而喜悅・覺察體驗</div>' +
        '<h1 style="margin: 0; font-size: 23px; font-weight: 800; letter-spacing: 0.5px;">財富流桌遊 報名成功</h1>' +
        '<p style="margin: 8px 0 0; font-size: 14px; opacity: 0.95;">活動日期：2026.10.15（四）下午 14:00 - 17:00</p>' +
      '</div>' +
      // Body
      '<div style="padding: 30px 24px; color: #334155; line-height: 1.6;">' +
        '<p style="font-size: 16px; margin-top: 0;"><strong>' + name + '</strong> 您好：</p>' +
        '<p style="font-size: 14px; color: #475569;">恭喜您成功報名「<strong>財富流桌遊</strong>」！透過 3 小時的人生推演，看見自己的盲點與財富思維。以下是您的報名明細與活動重要資訊：</p>' +
        
        // 活動核心資訊框
        '<div style="background-color: #fffbeb; border: 1.5px solid #fde68a; border-radius: 10px; padding: 20px; margin: 20px 0;">' +
          '<h3 style="margin: 0 0 14px; font-size: 16px; color: #92400e; font-weight: 800; display: flex; align-items: center; gap: 6px;">🎲 活動重要資訊</h3>' +
          '<table style="width: 100%; border-collapse: collapse; font-size: 14px;">' +
            '<tr>' +
              '<td style="padding: 7px 0; color: #78350f; width: 28%;">📅 活動日期</td>' +
              '<td style="padding: 7px 0; font-weight: 700; color: #1e293b;">' + EVENT_CONFIG.eventDate + '</td>' +
            '</tr>' +
            '<tr>' +
              '<td style="padding: 7px 0; color: #78350f;">⏰ 活動時間</td>' +
              '<td style="padding: 7px 0; font-weight: 800; color: #b45309; font-size: 15px;">' + EVENT_CONFIG.eventTime + '</td>' +
            '</tr>' +
            '<tr>' +
              '<td style="padding: 7px 0; color: #78350f;">📍 活動地點</td>' +
              '<td style="padding: 7px 0; font-weight: 700; color: #1e293b;">' + EVENT_CONFIG.venue + '</td>' +
            '</tr>' +
            '<tr>' +
              '<td style="padding: 7px 0; color: #78350f;">🏢 詳細地址</td>' +
              '<td style="padding: 7px 0; font-weight: 600; color: #1e293b;">' + EVENT_CONFIG.address + '</td>' +
            '</tr>' +
            '<tr>' +
              '<td style="padding: 7px 0; color: #78350f;">💰 活動費用</td>' +
              '<td style="padding: 7px 0; font-weight: 700; color: #dc2626;">' + EVENT_CONFIG.feeNote + '</td>' +
            '</tr>' +
          '</table>' +
          
          // Google 地圖導航按鈕
          '<div style="margin-top: 18px; padding-top: 14px; border-top: 1px dashed #fde68a; text-align: center;">' +
            '<a href="' + EVENT_CONFIG.mapUrl + '" target="_blank" style="display: inline-block; background-color: #b45309; color: #ffffff; text-decoration: none; padding: 10px 22px; border-radius: 8px; font-weight: 700; font-size: 14px; box-shadow: 0 4px 10px rgba(180, 83, 9, 0.25);">' +
              '🗺️ 開啟 Google 地圖導航' +
            '</a>' +
          '</div>' +
        '</div>' +

        // 報名明細表格
        '<table style="width: 100%; border-collapse: collapse; margin: 18px 0; font-size: 14px; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden;">' +
          '<tr>' +
            '<td style="padding: 10px 14px; background-color: #f8fafc; border-bottom: 1px solid #e2e8f0; color: #64748b; width: 32%;">報名姓名</td>' +
            '<td style="padding: 10px 14px; background-color: #f8fafc; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #0f172a;">' + name + '</td>' +
          '</tr>' +
          '<tr>' +
            '<td style="padding: 10px 14px; border-bottom: 1px solid #e2e8f0; color: #64748b;">電子郵件</td>' +
            '<td style="padding: 10px 14px; border-bottom: 1px solid #e2e8f0; color: #0f172a;">' + email + '</td>' +
          '</tr>' +
          '<tr>' +
            '<td style="padding: 10px 14px; background-color: #f8fafc; border-bottom: 1px solid #e2e8f0; color: #64748b;">Line ID</td>' +
            '<td style="padding: 10px 14px; background-color: #f8fafc; border-bottom: 1px solid #e2e8f0; color: #0f172a;">' + lineIdDisplay + '</td>' +
          '</tr>' +
          '<tr>' +
            '<td style="padding: 10px 14px; color: #64748b;">報名時間</td>' +
            '<td style="padding: 10px 14px; color: #0f172a;">' + timestamp + '</td>' +
          '</tr>' +
        '</table>' +

        '<div style="background-color: #f8fafc; border-left: 4px solid #b45309; padding: 12px 16px; border-radius: 6px; margin: 20px 0 16px;">' +
          '<p style="margin: 0; font-size: 13.5px; color: #334155; line-height: 1.5;">' +
            '💡 <strong>溫馨提醒</strong>：' + EVENT_CONFIG.note + '<br>' +
            '我們將於 <strong>10 月 14 日晚間 18:00</strong> 發送行前提醒信給您。期待在推演盤上與您相遇！' +
          '</p>' +
        '</div>' +
        
        '<hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0 16px;">' +
        '<p style="font-size: 13px; color: #71717a; text-align: center; margin: 0; font-weight: 600;">財富流桌遊 主辦團隊 敬上</p>' +
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
      '<div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #b45309 100%); padding: 32px 24px; text-align: center; color: #ffffff;">' +
        '<div style="display: inline-block; padding: 4px 14px; background: rgba(251, 191, 36, 0.2); border: 1px solid rgba(251, 191, 36, 0.4); border-radius: 20px; font-size: 13px; font-weight: 700; color: #fef3c7; margin-bottom: 10px; letter-spacing: 0.5px;">⏰ 明天下午準時開局</div>' +
        '<h1 style="margin: 0; font-size: 23px; font-weight: 800; letter-spacing: 0.5px;">【行前提醒】財富流桌遊明天登場！</h1>' +
        '<p style="margin: 8px 0 0; font-size: 14px; opacity: 0.95;">明天 10 月 15 日（四）下午 14:00 寰宇商務中心見！</p>' +
      '</div>' +
      // Body
      '<div style="padding: 30px 24px; color: #334155; line-height: 1.6;">' +
        '<p style="font-size: 16px; margin-top: 0;"><strong>' + name + '</strong> 您好：</p>' +
        '<p style="font-size: 14px; color: #475569;">您報名的「<strong>財富流桌遊</strong>」將於<strong>明天下午 14:00</strong> 正式開始！以下是為您彙整的行前提醒與交通資訊：</p>' +
        
        // 核心資訊卡
        '<div style="background-color: #fffbeb; border: 1.5px solid #fde68a; border-radius: 10px; padding: 20px; margin: 20px 0;">' +
          '<h3 style="margin: 0 0 14px; font-size: 16px; color: #92400e; font-weight: 800;">📋 活動時間與場地資訊</h3>' +
          '<table style="width: 100%; border-collapse: collapse; font-size: 14px;">' +
            '<tr>' +
              '<td style="padding: 7px 0; color: #78350f; width: 28%;">📅 活動日期</td>' +
              '<td style="padding: 7px 0; font-weight: 700; color: #1e293b;">' + EVENT_CONFIG.eventDate + '</td>' +
            '</tr>' +
            '<tr>' +
              '<td style="padding: 7px 0; color: #78350f;">⏰ 活動時間</td>' +
              '<td style="padding: 7px 0; font-weight: 800; color: #b45309; font-size: 15px;">' + EVENT_CONFIG.eventTime + '</td>' +
            '</tr>' +
            '<tr>' +
              '<td style="padding: 7px 0; color: #78350f;">📍 活動地點</td>' +
              '<td style="padding: 7px 0; font-weight: 700; color: #1e293b;">' + EVENT_CONFIG.venue + '</td>' +
            '</tr>' +
            '<tr>' +
              '<td style="padding: 7px 0; color: #78350f;">🏢 詳細地址</td>' +
              '<td style="padding: 7px 0; font-weight: 600; color: #1e293b;">' + EVENT_CONFIG.address + '</td>' +
            '</tr>' +
            '<tr>' +
              '<td style="padding: 7px 0; color: #78350f;">💰 活動費用</td>' +
              '<td style="padding: 7px 0; font-weight: 700; color: #dc2626;">' + EVENT_CONFIG.feeNote + '</td>' +
            '</tr>' +
          '</table>' +

          // Google 地圖導航按鈕
          '<div style="margin-top: 18px; padding-top: 14px; border-top: 1px dashed #fde68a; text-align: center;">' +
            '<a href="' + EVENT_CONFIG.mapUrl + '" target="_blank" style="display: inline-block; background-color: #b45309; color: #ffffff; text-decoration: none; padding: 10px 22px; border-radius: 8px; font-weight: 700; font-size: 14px; box-shadow: 0 4px 10px rgba(180, 83, 9, 0.25);">' +
              '🗺️ 開啟 Google 地圖導航' +
            '</a>' +
          '</div>' +
        '</div>' +

        // 溫馨提醒卡
        '<div style="background-color: #f8fafc; border-left: 4px solid #b45309; padding: 14px 16px; border-radius: 6px; margin: 16px 0;">' +
          '<div style="font-size: 13.5px; color: #334155; line-height: 1.6;">' +
            '💡 <strong>行前叮嚀</strong>：<br>' +
            '1. 桌遊將於 <strong>14:00 準時開局</strong>，為避免影響整組玩家進度，請於 <strong>13:50</strong> 提前抵達簽到。<br>' +
            '2. 現場備有茶水，請帶著輕鬆、開放的心情前來體驗！' +
          '</div>' +
        '</div>' +

        '<p style="font-size: 13.5px; color: #475569; margin-top: 22px; line-height: 1.6;">' +
          '期待明天下午與您一同在財富流推演中探索更多可能性！' +
        '</p>' +

        '<hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0 16px;">' +
        '<p style="font-size: 12px; color: #94a3b8; text-align: center; margin: 0;">財富流桌遊 主辦團隊 敬上</p>' +
      '</div>' +
    '</div>';
}

/**
 * 發送行前提醒信給所有已報名的學員
 * （將於 10/14 18:00 由定時觸發器自動執行）
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
  sheet.getRange(1, 7).setValue('行前提醒狀態').setBackground('#0f172a').setFontColor('#ffffff').setFontWeight('bold').setHorizontalAlignment('center');

  // 從第 2 列開始逐筆處理
  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var name = String(row[1]).trim();
    var email = String(row[2]).trim();

    // 只要有 Email 且尚未發送成功過
    if (email && email.indexOf('@') !== -1) {
      try {
        var subject = '【行前提醒】財富流桌遊明天下午 14:00 準時登場！（含場地與交通資訊）';
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
 * 設定 10/14 晚上 18:00 自動發送行前提醒信的定時觸發器
 */
function scheduleReminderTrigger() {
  cancelReminderTrigger();

  // 設定時間：2026年10月14日 18:00:00 (台北時間)
  // 月份為 0-indexed，9 代表 10 月
  var triggerDate = new Date(2026, 9, 14, 18, 0, 0);

  ScriptApp.newTrigger('sendWorkshopReminderEmail')
    .timeBased()
    .at(triggerDate)
    .create();

  Logger.log('✅ 已成功建立定時觸發器：將於 2026-10-14 18:00:00 (台北時間) 自動發送提醒信！');
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
 * 測試寄送提醒信至 garfiwang@gmail.com 以便預覽排版
 */
function testSendReminderEmail() {
  var testEmail = 'garfiwang@gmail.com';
  var testName = '玩家（測試預覽）';
  var subject = '【行前提醒】財富流桌遊明天下午 14:00 準時登場！（測試預覽）';
  var htmlBody = buildReminderEmailHtml(testName);

  MailApp.sendEmail({
    to: testEmail,
    subject: subject,
    htmlBody: htmlBody
  });

  Logger.log('✅ 提醒信測試預覽已成功寄送至：' + testEmail);
}

/**
 * 一鍵啟用授權測試 ＋ 同步自動建立 10/14 18:00 定時提醒觸發器
 */
function authorizeAndTestEmail() {
  // 1. 自動建立 10/14 18:00 定時提醒觸發器
  scheduleReminderTrigger();

  // 2. 寄送測試確認信
  MailApp.sendEmail({
    to: 'richnews168@gmail.com',
    subject: '【授權成功】財富流桌遊報名系統 Email 權限與 10/14 定時提醒排程已啟用',
    body: '恭喜！您的 Apps Script 寄信權限已成功啟用，且【10 月 14 日 18:00 行前提醒信自動發送排程】已同步建立成功！'
  });
  Logger.log('✅ 授權測試成功！已建立 10/14 18:00 定時排程，並發送測試信至 richnews168@gmail.com');
}

/**
 * 檢查目前是否有設定排程觸發器
 */
function checkTriggerStatus() {
  var triggers = ScriptApp.getProjectTriggers();
  var count = 0;
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === 'sendWorkshopReminderEmail') {
      count++;
    }
  }
  if (count > 0) {
    Logger.log('✅ 恭喜！目前已有 ' + count + ' 個【sendWorkshopReminderEmail】定時排程觸發器正常運作中（將於 10/14 18:00 自動執行）！');
  } else {
    Logger.log('⚠️ 目前尚未建立定時排程！請執行【scheduleReminderTrigger】或【authorizeAndTestEmail】來啟動排程。');
  }
}

