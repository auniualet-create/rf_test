# クイックスタートガイド 🚀

Notion → ECモール連携を最速で始めるためのガイドです。

## 📝 前提条件

- [ ] Notionアカウント
- [ ] 商品情報が入ったNotionデータベース
- [ ] Yahoo/楽天の出店アカウント
- [ ] 各ECモールのAPI利用権限

---

## 🎯 方法1: Google Apps Script で始める（最速・推奨）

### 所要時間: 30分

1. **Google Sheetsを開く**
   - 新しいシートを作成
   - ヘッダー行を追加: `商品ID`, `名称`, `原材料名`, `アレルゲン`, `栄養成分表示`, `内容量`, `賞味期限`, `保存方法`, `製造者/出荷元`

2. **Apps Scriptをコピー**
   - メニュー: 拡張機能 → Apps Script
   - `examples/1-google-apps-script/code.gs` の内容をコピー
   - 保存

3. **Notionデータをコピー**
   - Notionデータベースから商品情報をコピー
   - Google Sheetsに貼り付け

4. **HTML生成**
   - メニュー: 🛒 EC連携 → 📄 Yahoo用HTML生成
   - 生成されたHTMLをコピー
   - Yahoo管理画面に貼り付け

### ✅ 完了！

---

## 🎯 方法2: Notion API連携（本格運用）

### 所要時間: 1-2時間

1. **Notion Integration作成**
   ```
   https://www.notion.so/my-integrations
   ```
   - 「New integration」をクリック
   - 名前を入力（例: EC連携）
   - Internal Integrationを選択
   - Tokenをコピー

2. **データベースを共有**
   - Notionデータベースページを開く
   - 右上の「...」→「Add connections」
   - 作成したIntegrationを選択

3. **Database IDを取得**
   ```
   https://www.notion.so/your-workspace/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?v=...
                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                       これがDatabase ID
   ```

4. **Google Apps Scriptに設定**
   - Apps Scriptエディタを開く
   - `examples/1-google-apps-script/code-with-notion-api.gs` の内容をコピー
   - ツール → スクリプトプロパティ
   - 以下を追加:
     - `NOTION_API_KEY`: コピーしたToken
     - `NOTION_DATABASE_ID`: Database ID

5. **同期実行**
   - メニュー: 🛒 EC連携 → 🔄 Notionから同期
   - HTML生成して各モールに貼り付け

### ✅ 完了！

---

## 🎯 方法3: Python + GitHub Actions（完全自動化）

### 所要時間: 2-3時間

1. **リポジトリをクローン**
   ```bash
   cd examples/4-python-github-actions
   ```

2. **環境変数を設定**
   ```bash
   cp .env.example .env
   # .env を編集
   ```

3. **ローカルでテスト**
   ```bash
   pip install -r requirements.txt
   python sync.py
   ```

4. **GitHubにプッシュ**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   gh repo create notion-ec-sync --private
   git push -u origin main
   ```

5. **GitHub Secretsを設定**
   - Settings → Secrets and variables → Actions
   - 以下を追加:
     - `NOTION_API_KEY`
     - `NOTION_DATABASE_ID`
     - `YAHOO_API_KEY`
     - `YAHOO_API_SECRET`
     - `YAHOO_STORE_ACCOUNT`
     - `RAKUTEN_SERVICE_SECRET`
     - `RAKUTEN_LICENSE_KEY`

6. **自動実行を確認**
   - Actions タブで実行状況を確認
   - 3時間ごとに自動実行されます

### ✅ 完了！

---

## 🆘 トラブルシューティング

### Notion APIエラー
```
Error: Could not find database
```
**解決策**: データベースがIntegrationに共有されているか確認

### Yahoo API エラー
```
Error: Authentication failed
```
**解決策**: API KeyとSecretが正しいか確認。Yahoo Developer Networkで利用状況を確認

### HTMLが反映されない
**解決策**: 
- HTMLの構文エラーがないか確認
- 各モールの文字数制限（通常10,000文字）を超えていないか確認

---

## 📚 次のステップ

1. **自動化レベルを上げる**
   - Apps Script → Notion API連携
   - Notion API連携 → Python自動化

2. **カスタマイズ**
   - HTMLテンプレートの調整
   - 追加フィールドの対応

3. **他のモールに対応**
   - Amazon
   - BASE
   - STORES

---

## 💡 おすすめの運用フロー

### 初期段階
1. Google Apps Scriptで手動HTML生成
2. 運用フローを確立

### 中期段階
3. Notion API連携で半自動化
4. データ品質を改善

### 最終段階
5. Python + GitHub Actions で完全自動化
6. 監視・アラート機能を追加

---

## 📞 サポート

質問や問題がある場合は、以下を確認してください：

- `notion-to-ec-integration-proposals.md` - 詳細な提案書
- `examples/` - 各種サンプルコード
- GitHub Issues - 問題報告

Happy Coding! 🎉
