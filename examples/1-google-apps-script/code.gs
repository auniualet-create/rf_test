/**
 * Google Apps Script: Notion → ECモール HTML生成
 * 
 * このスクリプトはGoogle Sheetsのデータを読み込んで、
 * Yahoo/楽天用のHTML商品説明を生成します。
 */

// スプレッドシートが開いたときに実行（カスタムメニュー追加）
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('🛒 EC連携')
    .addItem('📄 Yahoo用HTML生成', 'generateYahooHTML')
    .addItem('📄 楽天用HTML生成', 'generateRakutenHTML')
    .addItem('📋 全商品HTML生成', 'generateAllHTML')
    .addSeparator()
    .addItem('⚙️ 設定', 'showSettings')
    .addToUi();
}

/**
 * Yahoo用HTML生成（選択行）
 */
function generateYahooHTML() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const activeRow = sheet.getActiveCell().getRow();
  
  // ヘッダー行は除外
  if (activeRow === 1) {
    SpreadsheetApp.getUi().alert('データ行を選択してください');
    return;
  }
  
  // 商品データを取得
  const productData = getProductData(sheet, activeRow);
  
  // HTML生成
  const html = createYahooHTML(productData);
  
  // HTMLを表示
  showHTMLDialog('Yahoo用HTML', html);
}

/**
 * 楽天用HTML生成（選択行）
 */
function generateRakutenHTML() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const activeRow = sheet.getActiveCell().getRow();
  
  if (activeRow === 1) {
    SpreadsheetApp.getUi().alert('データ行を選択してください');
    return;
  }
  
  const productData = getProductData(sheet, activeRow);
  const html = createRakutenHTML(productData);
  
  showHTMLDialog('楽天用HTML', html);
}

/**
 * 全商品のHTML生成
 */
function generateAllHTML() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const lastRow = sheet.getLastRow();
  
  let allHTML = '';
  
  // 2行目から最終行まで処理（1行目はヘッダー）
  for (let i = 2; i <= lastRow; i++) {
    const productData = getProductData(sheet, i);
    const html = createYahooHTML(productData);
    
    allHTML += `\n\n<!-- 商品ID: ${productData.id} -->\n`;
    allHTML += html;
    allHTML += '\n<!-- ここまで -->\n';
  }
  
  showHTMLDialog('全商品HTML', allHTML);
}

/**
 * シートから商品データを取得
 */
function getProductData(sheet, row) {
  const range = sheet.getRange(row, 1, 1, 9); // A列からI列まで
  const values = range.getValues()[0];
  
  return {
    id: values[0] || '',
    name: values[1] || '',
    ingredients: values[2] || '',
    allergen: values[3] || '',
    nutrition: values[4] || '',
    content: values[5] || '',
    expiry: values[6] || '',
    storage: values[7] || '',
    manufacturer: values[8] || ''
  };
}

/**
 * Yahoo用HTMLテンプレート生成
 */
function createYahooHTML(data) {
  // HTMLエスケープ
  const escape = (str) => {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  };
  
  // 改行をbrタグに変換
  const nl2br = (str) => {
    return String(str).replace(/\n/g, '<br>');
  };
  
  const html = `<table width="100%" border="0" cellpadding="3" cellspacing="2" bgcolor="#fff">
  <tr>
    <td width="25%" bgcolor="#FFCC99">名称</td>
    <td>${escape(data.name)}</td>
  </tr>
  
  <tr>
    <td class="abst" bgcolor="#FFCC99">原材料名</td>
    <td>${nl2br(escape(data.ingredients))}</td>
  </tr>
  
  <tr>
    <td bgcolor="#FFCC99">アレルゲン</td>
    <td>${nl2br(escape(data.allergen))}</td>
  </tr>
  
  <tr>
    <td bgcolor="#FFCC99">栄養成分表示</td>
    <td>${nl2br(escape(data.nutrition))}</td>
  </tr>
  
  <tr>
    <td bgcolor="#FFCC99">内容量</td>
    <td>${escape(data.content)}</td>
  </tr>
  
  <tr>
    <td bgcolor="#FFCC99">賞味期限</td>
    <td>${escape(data.expiry)}</td>
  </tr>
  
  <tr>
    <td bgcolor="#FFCC99">保存方法</td>
    <td>${escape(data.storage)}</td>
  </tr>
  
  <tr>
    <td bgcolor="#FFCC99">製造者/出荷元</td>
    <td>${nl2br(escape(data.manufacturer))}</td>
  </tr>
</table>`;
  
  return html;
}

/**
 * 楽天用HTMLテンプレート生成
 */
function createRakutenHTML(data) {
  const escape = (str) => {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  };
  
  const nl2br = (str) => {
    return String(str).replace(/\n/g, '<br>');
  };
  
  // 楽天用のスタイル（少し異なるデザイン）
  const html = `<table width="100%" border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
  <tr style="background-color: #FFE4B5;">
    <th width="150">名称</th>
    <td>${escape(data.name)}</td>
  </tr>
  
  <tr style="background-color: #FFE4B5;">
    <th>原材料名</th>
    <td>${nl2br(escape(data.ingredients))}</td>
  </tr>
  
  <tr style="background-color: #FFE4B5;">
    <th>アレルゲン</th>
    <td>${nl2br(escape(data.allergen))}</td>
  </tr>
  
  <tr style="background-color: #FFE4B5;">
    <th>栄養成分表示</th>
    <td>${nl2br(escape(data.nutrition))}</td>
  </tr>
  
  <tr style="background-color: #FFE4B5;">
    <th>内容量</th>
    <td>${escape(data.content)}</td>
  </tr>
  
  <tr style="background-color: #FFE4B5;">
    <th>賞味期限</th>
    <td>${escape(data.expiry)}</td>
  </tr>
  
  <tr style="background-color: #FFE4B5;">
    <th>保存方法</th>
    <td>${escape(data.storage)}</td>
  </tr>
  
  <tr style="background-color: #FFE4B5;">
    <th>製造者/出荷元</th>
    <td>${nl2br(escape(data.manufacturer))}</td>
  </tr>
</table>`;
  
  return html;
}

/**
 * HTMLダイアログを表示
 */
function showHTMLDialog(title, htmlContent) {
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
          #htmlCode {
            width: 100%;
            height: 400px;
            font-family: monospace;
            font-size: 12px;
            border: 1px solid #ccc;
            padding: 10px;
          }
          .buttons {
            margin-top: 10px;
            text-align: right;
          }
          button {
            padding: 10px 20px;
            margin-left: 10px;
            cursor: pointer;
            font-size: 14px;
          }
          .copy-btn {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
          }
          .copy-btn:hover {
            background-color: #45a049;
          }
          .preview {
            margin-top: 20px;
            padding: 20px;
            border: 1px solid #ddd;
            background-color: #f9f9f9;
          }
          h3 {
            margin-top: 0;
          }
        </style>
      </head>
      <body>
        <h2>${title}</h2>
        <textarea id="htmlCode" readonly>${htmlContent.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</textarea>
        <div class="buttons">
          <button class="copy-btn" onclick="copyToClipboard()">📋 クリップボードにコピー</button>
          <button onclick="google.script.host.close()">閉じる</button>
        </div>
        
        <div class="preview">
          <h3>プレビュー:</h3>
          ${htmlContent}
        </div>
        
        <script>
          function copyToClipboard() {
            const textarea = document.getElementById('htmlCode');
            textarea.select();
            document.execCommand('copy');
            alert('HTMLをクリップボードにコピーしました！');
          }
        </script>
      </body>
    </html>
  `)
    .setWidth(800)
    .setHeight(600);
  
  SpreadsheetApp.getUi().showModalDialog(htmlTemplate, title);
}

/**
 * 設定ダイアログ表示
 */
function showSettings() {
  const ui = SpreadsheetApp.getUi();
  ui.alert(
    '設定',
    '今後のバージョンアップで、以下の機能を追加予定:\n\n' +
    '• Notion API連携\n' +
    '• 自動同期スケジュール\n' +
    '• カスタムテンプレート\n' +
    '• 各種ECモールAPI連携',
    ui.ButtonSet.OK
  );
}
