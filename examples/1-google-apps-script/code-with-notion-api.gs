/**
 * Google Apps Script: Notion API連携版
 * 
 * このスクリプトはNotion APIから直接データを取得し、
 * Google Sheetsに同期して、HTML生成します。
 */

// === 設定 ===
// スクリプトプロパティに以下を設定してください：
// - NOTION_API_KEY: NotionのIntegration Token
// - NOTION_DATABASE_ID: 商品データベースID

/**
 * Notionから商品データを取得してシートに同期
 */
function syncFromNotion() {
  const ui = SpreadsheetApp.getUi();
  
  // APIキーとデータベースIDを取得
  const scriptProps = PropertiesService.getScriptProperties();
  const apiKey = scriptProps.getProperty('NOTION_API_KEY');
  const databaseId = scriptProps.getProperty('NOTION_DATABASE_ID');
  
  if (!apiKey || !databaseId) {
    ui.alert('エラー', 'Notion API設定が必要です。\n\n' +
             'ツール → スクリプトプロパティ から\n' +
             'NOTION_API_KEY と NOTION_DATABASE_ID を設定してください。', 
             ui.ButtonSet.OK);
    return;
  }
  
  try {
    // Notion APIを呼び出し
    const products = fetchNotionDatabase(apiKey, databaseId);
    
    // シートに書き込み
    updateSheet(products);
    
    ui.alert('同期完了', `${products.length}件の商品データを同期しました。`, ui.ButtonSet.OK);
    
  } catch (error) {
    ui.alert('エラー', `同期に失敗しました:\n${error.message}`, ui.ButtonSet.OK);
    Logger.log('Error: ' + error);
  }
}

/**
 * Notion APIからデータベースを取得
 */
function fetchNotionDatabase(apiKey, databaseId) {
  const url = `https://api.notion.com/v1/databases/${databaseId}/query`;
  
  const options = {
    method: 'post',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Notion-Version': '2022-06-28',
      'Content-Type': 'application/json'
    },
    payload: JSON.stringify({
      page_size: 100
    }),
    muteHttpExceptions: true
  };
  
  const response = UrlFetchApp.fetch(url, options);
  const json = JSON.parse(response.getContentText());
  
  if (response.getResponseCode() !== 200) {
    throw new Error(`Notion API Error: ${json.message || 'Unknown error'}`);
  }
  
  // Notionのデータを商品オブジェクトに変換
  return json.results.map(page => extractProductFromPage(page));
}

/**
 * NotionページからI品データを抽出
 */
function extractProductFromPage(page) {
  const props = page.properties;
  
  // プロパティ名は実際のNotionデータベースの構造に合わせて調整してください
  return {
    id: getPlainText(props['商品ID'] || props['ID']),
    name: getPlainText(props['名称'] || props['商品名']),
    ingredients: getPlainText(props['原材料名']),
    allergen: getPlainText(props['アレルゲン']),
    nutrition: getPlainText(props['栄養成分表示']),
    content: getPlainText(props['内容量']),
    expiry: getPlainText(props['賞味期限']),
    storage: getPlainText(props['保存方法']),
    manufacturer: getPlainText(props['製造者/出荷元'] || props['製造者'])
  };
}

/**
 * Notionプロパティからプレーンテキストを取得
 */
function getPlainText(property) {
  if (!property) return '';
  
  // プロパティタイプに応じて処理
  switch (property.type) {
    case 'title':
      return property.title.map(t => t.plain_text).join('');
    case 'rich_text':
      return property.rich_text.map(t => t.plain_text).join('');
    case 'number':
      return property.number?.toString() || '';
    case 'select':
      return property.select?.name || '';
    case 'multi_select':
      return property.multi_select.map(s => s.name).join(', ');
    default:
      return '';
  }
}

/**
 * シートにデータを書き込み
 */
function updateSheet(products) {
  const sheet = SpreadsheetApp.getActiveSheet();
  
  // ヘッダー行を設定（1行目）
  const headers = [
    '商品ID', '名称', '原材料名', 'アレルゲン', 
    '栄養成分表示', '内容量', '賞味期限', '保存方法', '製造者/出荷元'
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
  sheet.getRange(1, 1, 1, headers.length).setBackground('#4285F4');
  sheet.getRange(1, 1, 1, headers.length).setFontColor('#FFFFFF');
  
  // データ行を設定（2行目以降）
  if (products.length > 0) {
    const data = products.map(p => [
      p.id, p.name, p.ingredients, p.allergen,
      p.nutrition, p.content, p.expiry, p.storage, p.manufacturer
    ]);
    
    // 既存データをクリア
    if (sheet.getLastRow() > 1) {
      sheet.getRange(2, 1, sheet.getLastRow() - 1, headers.length).clearContent();
    }
    
    // 新しいデータを書き込み
    sheet.getRange(2, 1, data.length, headers.length).setValues(data);
  }
  
  // 列幅を自動調整
  for (let i = 1; i <= headers.length; i++) {
    sheet.autoResizeColumn(i);
  }
}

/**
 * カスタムメニュー（Notion連携版）
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('🛒 EC連携')
    .addItem('🔄 Notionから同期', 'syncFromNotion')
    .addSeparator()
    .addItem('📄 Yahoo用HTML生成', 'generateYahooHTML')
    .addItem('📄 楽天用HTML生成', 'generateRakutenHTML')
    .addItem('📋 全商品HTML生成', 'generateAllHTML')
    .addSeparator()
    .addItem('⚙️ Notion API設定', 'showNotionAPISettings')
    .addToUi();
}

/**
 * Notion API設定ダイアログ
 */
function showNotionAPISettings() {
  const ui = SpreadsheetApp.getUi();
  const scriptProps = PropertiesService.getScriptProperties();
  
  const currentApiKey = scriptProps.getProperty('NOTION_API_KEY') || '(未設定)';
  const currentDbId = scriptProps.getProperty('NOTION_DATABASE_ID') || '(未設定)';
  
  const htmlTemplate = HtmlService.createHtmlOutput(`
    <!DOCTYPE html>
    <html>
      <head>
        <base target="_top">
        <style>
          body {
            font-family: Arial, sans-serif;
            padding: 20px;
          }
          .form-group {
            margin-bottom: 15px;
          }
          label {
            display: block;
            font-weight: bold;
            margin-bottom: 5px;
          }
          input {
            width: 100%;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
          }
          .current-value {
            font-size: 12px;
            color: #666;
            margin-top: 3px;
          }
          button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
          }
          button:hover {
            background-color: #45a049;
          }
          .info {
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
          }
        </style>
      </head>
      <body>
        <h2>Notion API設定</h2>
        
        <div class="info">
          <strong>設定手順:</strong><br>
          1. <a href="https://www.notion.so/my-integrations" target="_blank">Notion Integrations</a> でIntegrationを作成<br>
          2. Integration Tokenをコピー<br>
          3. 商品データベースをIntegrationに共有<br>
          4. データベースIDをURLから取得
        </div>
        
        <div class="form-group">
          <label>Notion API Key (Integration Token):</label>
          <input type="password" id="apiKey" placeholder="secret_...">
          <div class="current-value">現在: ${currentApiKey.substring(0, 20)}...</div>
        </div>
        
        <div class="form-group">
          <label>Notion Database ID:</label>
          <input type="text" id="databaseId" placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx">
          <div class="current-value">現在: ${currentDbId}</div>
        </div>
        
        <button onclick="saveSettings()">保存</button>
        
        <script>
          function saveSettings() {
            const apiKey = document.getElementById('apiKey').value;
            const databaseId = document.getElementById('databaseId').value;
            
            if (!apiKey && !databaseId) {
              alert('少なくとも1つの値を入力してください');
              return;
            }
            
            google.script.run
              .withSuccessHandler(() => {
                alert('設定を保存しました');
                google.script.host.close();
              })
              .withFailureHandler((error) => {
                alert('エラー: ' + error.message);
              })
              .saveNotionAPISettings(apiKey, databaseId);
          }
        </script>
      </body>
    </html>
  `)
    .setWidth(600)
    .setHeight(500);
  
  ui.showModalDialog(htmlTemplate, 'Notion API設定');
}

/**
 * Notion API設定を保存
 */
function saveNotionAPISettings(apiKey, databaseId) {
  const scriptProps = PropertiesService.getScriptProperties();
  
  if (apiKey) {
    scriptProps.setProperty('NOTION_API_KEY', apiKey);
  }
  if (databaseId) {
    scriptProps.setProperty('NOTION_DATABASE_ID', databaseId);
  }
}

/**
 * 自動同期トリガーを設定
 */
function setupAutoSync() {
  // 既存のトリガーを削除
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === 'syncFromNotion') {
      ScriptApp.deleteTrigger(trigger);
    }
  });
  
  // 新しいトリガーを作成（毎日午前9時に実行）
  ScriptApp.newTrigger('syncFromNotion')
    .timeBased()
    .atHour(9)
    .everyDays(1)
    .create();
  
  SpreadsheetApp.getUi().alert(
    '自動同期設定完了',
    '毎日午前9時にNotionから自動同期されます。',
    SpreadsheetApp.getUi().ButtonSet.OK
  );
}

// code.gs の関数もここに含める（前のコードから）
// generateYahooHTML, generateRakutenHTML, createYahooHTML, createRakutenHTML, etc.
