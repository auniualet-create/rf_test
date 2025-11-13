# クイックスタートガイド

このガイドでは、NotionからYahooショッピング・楽天への自動同期システムを最短でセットアップする方法を説明します。

## ステップ1: 環境の準備

### Pythonのインストール
Python 3.8以上が必要です。

```bash
python --version
```

### 依存関係のインストール

```bash
pip install -r requirements.txt
```

Playwrightを使用する場合（ブラウザ自動化）：

```bash
playwright install chromium
```

## ステップ2: Notion APIの設定

### 1. Notionインテグレーションの作成

1. [Notion Integrations](https://www.notion.so/my-integrations)にアクセス
2. 「+ New integration」をクリック
3. 名前を入力して作成
4. **Internal Integration Token**をコピー（後で使用）

### 2. Notionページへのアクセス権限付与

1. 同期したいNotionページを開く
2. 右上の「...」メニューをクリック
3. 「Add connections」を選択
4. 作成したインテグレーションを選択

### 3. ページIDの取得

NotionページのURLから取得できます：
```
https://www.notion.so/Your-Page-Title-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                                    ↑ この部分がページID（32文字のハイフン区切り）
```

または、ページの「Copy link」から取得：
```
https://www.notion.so/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## ステップ3: YahooショッピングAPIの設定

### API利用申請

1. [YahooショッピングAPI](https://developer.yahoo.co.jp/webapi/shopping/)にアクセス
2. API利用申請を行う
3. 認証情報を取得：
   - Seller ID
   - Application ID
   - Client ID / Client Secret
   - Access Token

### またはブラウザ自動化を使用する場合

APIが利用できない場合は、ブラウザ自動化を使用できます：
- Yahooアカウントのユーザー名とパスワードが必要

## ステップ4: 楽天APIの設定

1. [楽天API](https://webservice.rakuten.co.jp/)にアクセス
2. アプリケーション登録を行う
3. 認証情報を取得：
   - Application ID
   - Affiliate ID
   - Secret
   - Access Token

## ステップ5: 環境変数の設定

`.env.example`をコピーして`.env`を作成：

```bash
cp .env.example .env
```

`.env`ファイルを編集して認証情報を設定：

```env
# Notion設定
NOTION_API_KEY=secret_xxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Yahooショッピング設定（API使用の場合）
YAHOO_SELLER_ID=your_seller_id
YAHOO_APPLICATION_ID=your_app_id
YAHOO_CLIENT_ID=your_client_id
YAHOO_CLIENT_SECRET=your_client_secret
YAHOO_ACCESS_TOKEN=your_access_token

# Yahooショッピング設定（ブラウザ自動化の場合）
YAHOO_USERNAME=your_username
YAHOO_PASSWORD=your_password

# 楽天設定
RAKUTEN_APPLICATION_ID=your_app_id
RAKUTEN_AFFILIATE_ID=your_affiliate_id
RAKUTEN_SECRET=your_secret
RAKUTEN_ACCESS_TOKEN=your_access_token
```

## ステップ6: 商品マッピングファイルの作成

`product_mapping.json.example`をコピー：

```bash
cp product_mapping.json.example product_mapping.json
```

`product_mapping.json`を編集：

```json
{
  "notion-page-id-1": {
    "yahoo": "yahoo-item-code-1",
    "rakuten": "rakuten-item-code-1",
    "use_browser_for_yahoo": false
  }
}
```

## ステップ7: テスト実行

### 単一商品の同期テスト

```bash
python src/main.py \
  --notion-page-id "your-notion-page-id" \
  --yahoo-item-code "yahoo-item-code" \
  --rakuten-item-code "rakuten-item-code"
```

### ブラウザ自動化のテスト（Yahoo APIが使えない場合）

```bash
python src/main.py \
  --notion-page-id "your-notion-page-id" \
  --yahoo-item-code "yahoo-item-code" \
  --use-browser
```

## ステップ8: 定期実行の設定

### cronを使用する場合（Linux/Mac）

```bash
crontab -e
```

以下を追加：

```bash
# 毎時0分に実行
0 * * * * cd /path/to/project && /usr/bin/python3 src/scheduler.py
```

### Windows タスクスケジューラー

1. タスクスケジューラーを開く
2. 「基本タスクの作成」を選択
3. トリガーを「毎時」に設定
4. 操作で以下を実行：
   ```
   python C:\path\to\project\src\scheduler.py
   ```

## トラブルシューティング

### Notion APIエラー

**エラー**: `NOTION_API_KEYが設定されていません`
- `.env`ファイルに`NOTION_API_KEY`が設定されているか確認

**エラー**: `Notionページの取得に失敗しました`
- Notionページにインテグレーションのアクセス権限が付与されているか確認
- ページIDが正しいか確認

### YahooショッピングAPIエラー

**エラー**: `YahooショッピングAPIの呼び出しに失敗しました`
- API認証情報が正しいか確認
- APIのレート制限に達していないか確認
- 商品コードが正しいか確認

### ブラウザ自動化エラー

**エラー**: `ブラウザ自動化でエラーが発生しました`
- Playwrightがインストールされているか確認: `playwright install chromium`
- Yahooのログイン情報が正しいか確認
- 管理画面のUIが変更されていないか確認（セレクタの調整が必要な場合があります）

## 次のステップ

- [README.md](README.md) - 詳細なドキュメント
- [IMPLEMENTATION_IDEAS.md](IMPLEMENTATION_IDEAS.md) - 実装アイデア集
- [examples/](examples/) - 使用例

## サポート

問題が発生した場合は、以下を確認してください：

1. ログファイル（`*.log`）を確認
2. 環境変数が正しく設定されているか確認
3. 各プラットフォームのAPIドキュメントを確認
