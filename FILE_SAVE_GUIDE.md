# ファイル保存ガイド

Web版Cursorでダウンロードできない場合、以下の手順でファイルを保存してください。

## 保存手順

1. **新しいフォルダを作成**
   - ローカルPCに `notion-ecommerce-sync` というフォルダを作成

2. **各ファイルをコピー＆ペースト**
   - 以下のファイル一覧から、各ファイルの内容をコピー
   - テキストエディタ（メモ帳、VS Code、Sublime Textなど）で新規ファイルを作成
   - ファイル名と内容を貼り付け

## ファイル一覧と保存場所

### ルートディレクトリ
- `README.md` - メインドキュメント（上記で表示済み）
- `requirements.txt` - Python依存パッケージ（上記で表示済み）
- `.env.example` - 環境変数のテンプレート（上記で表示済み）
- `product_mapping.json.example` - 商品マッピングのテンプレート（上記で表示済み）
- `.gitignore` - Git除外設定（上記で表示済み）
- `QUICK_START.md` - クイックスタートガイド（上記で表示済み）
- `SOLUTION_PROPOSAL.md` - ソリューション提案書（上記で表示済み）
- `IMPLEMENTATION_IDEAS.md` - 実装アイデア集（上記で表示済み）

### src/ ディレクトリ
以下のファイルを `src/` フォルダ内に保存：
- `src/__init__.py` - パッケージ初期化ファイル（上記で表示済み）
- `src/notion_client.py` - Notion APIクライアント（上記で表示済み）
- `src/yahoo_client.py` - YahooショッピングAPIクライアント（上記で表示済み）
- `src/rakuten_client.py` - 楽天APIクライアント（上記で表示済み）
- `src/sync_service.py` - 同期サービス（上記で表示済み）
- `src/scheduler.py` - 定期実行スケジューラー（上記で表示済み）
- `src/main.py` - メイン実行スクリプト（上記で表示済み）

### examples/ ディレクトリ
以下のファイルを `examples/` フォルダ内に保存：
- `examples/basic_usage.py` - 基本的な使用例（上記で表示済み）
- `examples/notion_data_extraction.py` - Notionデータ取得の例（上記で表示済み）

### .github/workflows/ ディレクトリ
以下のファイルを `.github/workflows/` フォルダ内に保存：
- `.github/workflows/sync.yml` - GitHub Actionsワークフロー（上記で表示済み）

## ディレクトリ構造

```
notion-ecommerce-sync/
├── README.md
├── requirements.txt
├── .env.example
├── product_mapping.json.example
├── .gitignore
├── QUICK_START.md
├── SOLUTION_PROPOSAL.md
├── IMPLEMENTATION_IDEAS.md
├── src/
│   ├── __init__.py
│   ├── notion_client.py
│   ├── yahoo_client.py
│   ├── rakuten_client.py
│   ├── sync_service.py
│   ├── scheduler.py
│   └── main.py
├── examples/
│   ├── basic_usage.py
│   └── notion_data_extraction.py
└── .github/
    └── workflows/
        └── sync.yml
```

## 注意事項

1. **ファイル名の先頭にドット（.）が付くファイル**
   - `.env.example`、`.gitignore` などは、ファイル名の先頭にドット（.）を含めてください
   - Windowsの場合、エクスプローラーで直接作成できない場合は、コマンドプロンプトから作成してください

2. **エンコーディング**
   - すべてのファイルはUTF-8エンコーディングで保存してください

3. **実行権限**
   - Pythonファイル（.py）には実行権限が必要な場合があります（Linux/Mac）

## 確認方法

すべてのファイルを保存したら、以下のコマンドで確認できます：

```bash
# ファイル一覧を確認
find . -type f | sort

# Pythonファイルの構文チェック
python -m py_compile src/*.py
```
