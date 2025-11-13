# ファイルのダウンロード方法

## Web版Cursorでのファイルダウンロード方法

### 方法1: サイドバーからファイルを探す

Web版Cursorでは、以下のいずれかの場所にファイルエクスプローラーがある可能性があります：

1. **左側のサイドバー** - フォルダアイコンやファイルアイコンをクリック
2. **上部メニュー** - 「File」や「ファイル」メニューから「Open Folder」を選択
3. **左側のタブ** - 「Explorer」「Files」「File Explorer」などのタブ

### 方法2: ターミナルから直接ダウンロード

以下のコマンドをターミナルで実行してください：

```bash
# 現在のディレクトリを確認
pwd

# zipファイルの場所を確認
ls -lh notion-ecommerce-sync.zip
```

### 方法3: ファイルの内容を直接確認・コピー

個別のファイルが必要な場合は、以下のコマンドで内容を表示できます：

```bash
# ファイルの内容を表示
cat ファイル名

# 例：README.mdの内容を表示
cat README.md
```

## 含まれているファイル一覧

以下のファイルがzipに含まれています：

### ソースコード
- `src/notion_client.py`
- `src/yahoo_client.py`
- `src/rakuten_client.py`
- `src/sync_service.py`
- `src/scheduler.py`
- `src/main.py`
- `src/__init__.py`

### 使用例
- `examples/basic_usage.py`
- `examples/notion_data_extraction.py`

### ドキュメント
- `README.md`
- `QUICK_START.md`
- `SOLUTION_PROPOSAL.md`
- `IMPLEMENTATION_IDEAS.md`

### 設定ファイル
- `requirements.txt`
- `.env.example`
- `product_mapping.json.example`
- `.gitignore`
- `.github/workflows/sync.yml`

## 手動でファイルを作成する場合

zipファイルがダウンロードできない場合は、各ファイルを個別に作成することもできます。
各ファイルの内容は、ターミナルで `cat` コマンドを使用して確認できます。
