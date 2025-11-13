# Notion → Eコマースプラットフォーム自動同期システム

Notionに記載した商品情報（原材料など）をYahooショッピングや楽天などのeコマースプラットフォームに自動的に同期するシステムです。

## 機能

- ✅ Notion APIから商品情報を取得
- ✅ Yahooショッピングへの自動同期（APIまたはブラウザ自動化）
- ✅ 楽天への自動同期（API）
- ✅ HTML形式への自動変換
- ✅ 定期実行対応（cron/スケジューラー）

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env.example`をコピーして`.env`を作成し、必要な認証情報を設定してください。

```bash
cp .env.example .env
# .envファイルを編集して認証情報を設定
```

### 3. 商品マッピングファイルの作成

`product_mapping.json.example`をコピーして`product_mapping.json`を作成し、NotionページIDと各プラットフォームの商品コードをマッピングしてください。

```bash
cp product_mapping.json.example product_mapping.json
# product_mapping.jsonを編集して商品マッピングを設定
```

## 使用方法

### 手動実行

単一の商品を同期する場合：

```bash
python src/main.py \
  --notion-page-id "your-notion-page-id" \
  --yahoo-item-code "yahoo-item-code" \
  --rakuten-item-code "rakuten-item-code"
```

ブラウザ自動化を使用する場合（Yahoo APIが使えない場合）：

```bash
python src/main.py \
  --notion-page-id "your-notion-page-id" \
  --yahoo-item-code "yahoo-item-code" \
  --use-browser
```

マッピングファイルを使用する場合：

```bash
python src/main.py \
  --notion-page-id "your-notion-page-id" \
  --mapping-file "product_mapping.json"
```

### 定期実行の設定

#### cronを使用する場合（Linux/Mac）

```bash
# 毎時0分に実行
0 * * * * cd /path/to/project && /usr/bin/python3 src/scheduler.py
```

#### Windows タスクスケジューラー

1. タスクスケジューラーを開く
2. 基本タスクの作成
3. トリガーを設定（例: 毎時）
4. 操作で`python src/scheduler.py`を実行するように設定

#### GitHub Actionsを使用する場合

`.github/workflows/sync.yml`を作成：

```yaml
name: Sync Products

on:
  schedule:
    - cron: '0 * * * *'  # 毎時実行
  workflow_dispatch:  # 手動実行も可能

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: python src/scheduler.py
        env:
          NOTION_API_KEY: ${{ secrets.NOTION_API_KEY }}
          # その他の環境変数...
```

## アーキテクチャ

### コンポーネント

1. **NotionClient** (`src/notion_client.py`)
   - Notion APIから商品情報を取得
   - HTML形式に変換

2. **YahooShoppingClient** (`src/yahoo_client.py`)
   - YahooショッピングAPIで商品情報を更新
   - ブラウザ自動化の代替手段も提供

3. **RakutenClient** (`src/rakuten_client.py`)
   - 楽天APIで商品情報を更新

4. **SyncService** (`src/sync_service.py`)
   - 各プラットフォームへの同期を統合管理

5. **Scheduler** (`src/scheduler.py`)
   - 定期実行のためのスケジューラー

## 実装アプローチ

### アプローチ1: API連携（推奨）

各プラットフォームのAPIを使用して直接更新します。最も安定性が高く、推奨される方法です。

**メリット:**
- 高速
- 安定性が高い
- メンテナンスが容易

**必要なもの:**
- 各プラットフォームのAPI認証情報

### アプローチ2: ブラウザ自動化

APIが利用できない場合、Playwrightを使用してブラウザを自動操作します。

**メリット:**
- APIがなくても動作する
- 既存の管理画面をそのまま利用

**デメリット:**
- 実行速度が遅い
- UI変更に弱い
- メンテナンスコストが高い

## 注意事項

1. **API認証情報の管理**
   - `.env`ファイルはGitにコミットしないでください
   - 本番環境では環境変数やシークレット管理サービスを使用してください

2. **レート制限**
   - 各プラットフォームのAPIレート制限に注意してください
   - 必要に応じてリトライロジックを実装してください

3. **エラーハンドリング**
   - ネットワークエラーやAPIエラーに対する適切な処理を実装してください
   - ログを確認して問題を特定してください

4. **データ変換**
   - Notionのリッチテキストを各プラットフォームの形式に変換する際、制約に注意してください
   - HTMLタグの制限や文字数制限を確認してください

## トラブルシューティング

### Notion APIエラー

- `NOTION_API_KEY`が正しく設定されているか確認
- NotionページのIDが正しいか確認
- NotionページがAPIキーにアクセス権限を持っているか確認

### YahooショッピングAPIエラー

- API認証情報が正しいか確認
- 商品コードが正しいか確認
- APIのレート制限に達していないか確認

### ブラウザ自動化エラー

- Playwrightがインストールされているか確認: `playwright install chromium`
- Yahooのログイン情報が正しいか確認
- 管理画面のUIが変更されていないか確認

## 今後の拡張

- [ ] Webhookによるリアルタイム同期
- [ ] ダッシュボード/管理画面の作成
- [ ] その他プラットフォームへの対応（Amazon、BASEなど）
- [ ] 画像の自動アップロード
- [ ] 変更履歴の追跡
- [ ] エラー通知機能（メール/Slack）

## ライセンス

MIT License
