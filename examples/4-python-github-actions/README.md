# Python + GitHub Actions 自動同期システム

## 概要
Pythonスクリプトを使ってNotion APIから商品データを取得し、各ECモールのAPIに自動的に反映させるシステムです。
GitHub Actionsで定期実行することで、完全な自動化を実現します。

## 機能
- ✅ Notion APIから商品データ自動取得
- ✅ Yahoo/楽天用HTML自動生成
- ✅ ECモールAPI連携（Yahoo Shopping, 楽天RMS）
- ✅ GitHub Actionsで定期実行（3時間ごと）
- ✅ 手動実行も可能
- ✅ エラーログ・実行履歴の記録

## セットアップ手順

### 1. リポジトリの準備

```bash
# このディレクトリをGitリポジトリとして初期化
git init
git add .
git commit -m "Initial commit"

# GitHubにプッシュ
gh repo create notion-ec-sync --private
git remote add origin https://github.com/your-username/notion-ec-sync.git
git push -u origin main
```

### 2. 環境変数の設定

GitHubリポジトリの Settings → Secrets and variables → Actions で以下を設定：

- `NOTION_API_KEY`: Notion Integration Token
- `NOTION_DATABASE_ID`: 商品データベースID
- `YAHOO_API_KEY`: Yahoo Shopping API Key
- `YAHOO_API_SECRET`: Yahoo Shopping API Secret
- `YAHOO_STORE_ACCOUNT`: Yahoo店舗アカウント
- `RAKUTEN_SERVICE_SECRET`: 楽天 serviceSecret
- `RAKUTEN_LICENSE_KEY`: 楽天 licenseKey

### 3. 依存関係のインストール（ローカルテスト用）

```bash
pip install -r requirements.txt
```

### 4. ローカルでのテスト実行

```bash
# .env.example を .env にコピーして編集
cp .env.example .env

# スクリプト実行
python sync.py
```

### 5. GitHub Actionsの有効化

リポジトリの Actions タブから、ワークフローを有効化してください。

## ファイル構成

```
.
├── sync.py                 # メイン同期スクリプト
├── notion_client.py        # Notion API クライアント
├── html_generator.py       # HTML生成ロジック
├── ec_clients/
│   ├── yahoo.py           # Yahoo Shopping API
│   └── rakuten.py         # 楽天 RMS API
├── requirements.txt        # Python依存関係
├── .env.example           # 環境変数サンプル
└── .github/
    └── workflows/
        └── sync.yml       # GitHub Actions設定
```

## 使い方

### 自動実行
GitHub Actionsが3時間ごとに自動実行します。

### 手動実行
1. GitHubリポジトリの Actions タブを開く
2. "Notion to EC Mall Sync" ワークフローを選択
3. "Run workflow" ボタンをクリック

### ローカル実行
```bash
python sync.py
```

## トラブルシューティング

### API認証エラー
- GitHub Secretsが正しく設定されているか確認
- APIキーの有効期限を確認

### データ同期エラー
- Notionデータベースの構造が正しいか確認
- ECモールのAPI制限に達していないか確認

### ログの確認
- GitHub Actions の実行ログを確認
- `logs/` ディレクトリ（ローカル実行時）

## カスタマイズ

### 実行頻度の変更
`.github/workflows/sync.yml` の `cron` を編集：

```yaml
schedule:
  - cron: '0 */6 * * *'  # 6時間ごとに変更
```

### HTMLテンプレートのカスタマイズ
`html_generator.py` の `generate_yahoo_html()` / `generate_rakuten_html()` を編集
