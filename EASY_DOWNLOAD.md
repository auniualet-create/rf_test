# 簡単ダウンロード方法

Web版Cursorの制限を回避して、すべてのファイルを簡単にダウンロードする方法です。

## 方法1: Base64エンコード方式（推奨・最も簡単）

### ステップ1: ターミナルでbase64データを取得

Web版Cursorのターミナルで以下のコマンドを実行：

```bash
cd /workspace
base64 notion-ecommerce-sync.zip
```

### ステップ2: 出力をコピー

ターミナルに表示されたbase64データを**すべてコピー**してください（長い文字列です）

### ステップ3: ローカルPCでデコード

ローカルPCのターミナル（コマンドプロンプト/PowerShell）で：

**Windowsの場合:**
```powershell
# base64データをクリップボードから取得してファイルに保存
# 1. base64データをテキストファイルに貼り付け（例: zip_base64.txt）
# 2. PowerShellで実行:
[System.IO.File]::WriteAllBytes("notion-ecommerce-sync.zip", [System.Convert]::FromBase64String((Get-Content zip_base64.txt -Raw)))
```

**Mac/Linuxの場合:**
```bash
# base64データをクリップボードから取得してファイルに保存
# 1. base64データをテキストファイルに貼り付け（例: zip_base64.txt）
# 2. ターミナルで実行:
base64 -d zip_base64.txt > notion-ecommerce-sync.zip
```

**Pythonを使用する場合（どのOSでも動作）:**
```python
import base64

# base64データをテキストファイルから読み込む
with open('zip_base64.txt', 'r') as f:
    base64_data = f.read().strip()

# デコードしてzipファイルに保存
zip_data = base64.b64decode(base64_data)
with open('notion-ecommerce-sync.zip', 'wb') as f:
    f.write(zip_data)

print("✓ notion-ecommerce-sync.zip が作成されました！")
```

## 方法2: ターミナルから直接コピー（小さいファイル向け）

各ファイルを個別にコピーする方法：

```bash
# ファイルの内容を表示
cat ファイル名

# 例: README.mdの内容を表示
cat README.md
```

表示された内容をコピーして、ローカルPCでファイルとして保存してください。

## 方法3: GitHub経由（Gitリポジトリがある場合）

もしGitリポジトリが設定されていれば：

```bash
# 変更をコミット
git add .
git commit -m "Add Notion to e-commerce sync system"

# GitHubにプッシュ
git push origin main

# その後、GitHubのWebインターフェースからzipファイルをダウンロード
# または、GitHubのリリース機能を使用
```

## 推奨方法

**最も簡単なのは方法1（Base64エンコード方式）です。**

1. ターミナルで `base64 notion-ecommerce-sync.zip` を実行
2. 出力された長い文字列をすべてコピー
3. ローカルPCでPythonスクリプトまたはコマンドでデコード

これで、すべてのファイルが含まれたzipファイルを一度に取得できます！
