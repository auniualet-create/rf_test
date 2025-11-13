# Notion → ECモール 商品データ連携システム

NotionのデータベースをYahooショッピング、楽天市場などのECモールに自動連携するためのツール集です。

## 🎯 概要

Notionで一元管理している商品情報（原材料、アレルゲン、栄養成分など）を、各ECモールの商品ページに自動的に反映させることができます。

## ✨ 特徴

- 🔄 **Notionを唯一の情報源に**: 商品情報をNotionで一元管理
- 🚀 **複数のアプローチ**: 簡単なものから完全自動化まで選択可能
- 🛒 **複数モール対応**: Yahoo、楽天、その他ECモールに対応
- ⚡ **段階的な導入**: レベルに応じて段階的に自動化レベルを上げられる

## 📁 ファイル構成

```
.
├── README.md                                    # このファイル
├── QUICKSTART.md                               # クイックスタートガイド
├── notion-to-ec-integration-proposals.md       # 詳細提案書
└── examples/                                   # 実装サンプル
    ├── 1-google-apps-script/                  # Google Apps Script版
    │   ├── code.gs                            # 基本版
    │   └── code-with-notion-api.gs            # Notion API連携版
    └── 4-python-github-actions/               # Python自動化版
        ├── sync.py                            # メインスクリプト
        ├── notion_client_wrapper.py           # Notion APIクライアント
        ├── html_generator.py                  # HTML生成
        ├── ec_clients/                        # ECモールAPIクライアント
        │   ├── yahoo.py
        │   └── rakuten.py
        └── .github/workflows/sync.yml         # 自動実行設定
```

## 🚀 クイックスタート

### 最速で始める（30分）

1. **Google Sheetsを開く**
2. **Apps Scriptをコピー**: `examples/1-google-apps-script/code.gs`
3. **Notionデータを貼り付け**
4. **HTML生成してコピー**

詳細は [QUICKSTART.md](./QUICKSTART.md) をご覧ください。

## 📋 提案されている方法（6つ）

| 方法 | 自動化 | 難易度 | 月額コスト | おすすめ度 |
|------|--------|--------|-----------|-----------|
| 1️⃣ Notion API + ECモールAPI | ⭐⭐⭐⭐⭐ | 高 | 低 | ⭐⭐⭐⭐⭐ |
| 2️⃣ Zapier/Make.com | ⭐⭐⭐⭐⭐ | 中 | 中～高 | ⭐⭐⭐⭐ |
| 3️⃣ Google Apps Script | ⭐⭐ | 中 | 無料 | ⭐⭐⭐ |
| 4️⃣ Python + GitHub Actions | ⭐⭐⭐⭐⭐ | 高 | 無料 | ⭐⭐⭐⭐⭐ |
| 5️⃣ CSV Export + 一括登録 | ⭐⭐ | 低 | 無料 | ⭐⭐ |
| 6️⃣ Webhook + Serverless | ⭐⭐⭐⭐⭐ | 最高 | 従量 | ⭐⭐⭐⭐ |

詳細は [notion-to-ec-integration-proposals.md](./notion-to-ec-integration-proposals.md) をご覧ください。

## 🎯 推奨される導入ステップ

### フェーズ1: お試し（1週間）
**Google Apps Script** で基本機能を体験
- 手動でのHTML生成
- 動作確認
- 運用フローの確立

### フェーズ2: 半自動化（2-4週間）
**Notion API連携** で作業を軽減
- 自動データ取得
- 定期同期
- エラーハンドリング

### フェーズ3: 完全自動化（1-2ヶ月）
**Python + GitHub Actions** で完全自動化
- リアルタイム同期
- 複数モール対応
- 監視・アラート

## 💻 必要な環境

### 最小構成（方法3: Google Apps Script）
- Googleアカウント
- Notionアカウント
- ECモールの出店アカウント

### 完全自動化（方法4: Python + GitHub Actions）
- 上記に加えて：
- GitHubアカウント
- Python 3.11+
- 各ECモールのAPI利用権限

## 🔑 必要なAPI KEY

### Notion
- Integration Token（無料）
- Database ID

### Yahoo Shopping
- Client ID / Secret
- Store Account
- [Yahoo Developer Network](https://developer.yahoo.co.jp/) で申請

### 楽天市場
- serviceSecret / licenseKey
- RMS契約が必要
- [楽天 RMS](https://rms.rakuten.co.jp/) で申請

## 📚 ドキュメント

- **[QUICKSTART.md](./QUICKSTART.md)** - 最速で始めるためのガイド
- **[notion-to-ec-integration-proposals.md](./notion-to-ec-integration-proposals.md)** - 詳細な提案書
- **[examples/](./examples/)** - 各種実装サンプル

## 🛠️ 使い方

### Google Apps Script版

```javascript
// 1. Google Sheetsでスクリプトエディタを開く
// 2. examples/1-google-apps-script/code.gs をコピー
// 3. メニューから実行
```

### Python版

```bash
# 1. 環境変数を設定
cp examples/4-python-github-actions/.env.example .env

# 2. 依存関係をインストール
pip install -r examples/4-python-github-actions/requirements.txt

# 3. 実行
python examples/4-python-github-actions/sync.py
```

## 🔧 カスタマイズ

### HTMLテンプレートの変更

```python
# html_generator.py を編集
def generate_yahoo_html(self, product):
    # ここでテンプレートをカスタマイズ
    html_template = '''
    <table>
      <!-- 自由にカスタマイズ -->
    </table>
    '''
    return html_template.format(**product)
```

### 実行頻度の変更

```yaml
# .github/workflows/sync.yml
schedule:
  - cron: '0 */6 * * *'  # 6時間ごとに変更
```

## 📊 動作環境

- Python 3.11+
- Node.js 18+ (Zapier使用時)
- Google Apps Script (Google Sheets)
- GitHub Actions (無料枠で運用可能)

## 🆘 トラブルシューティング

### よくある問題

**Q: Notion APIに接続できない**
```
A: Integration TokenとDatabase IDが正しいか確認してください
```

**Q: Yahoo APIでエラーが出る**
```
A: API利用申請が完了しているか、認証情報が正しいか確認してください
```

**Q: HTMLが反映されない**
```
A: 文字数制限（通常10,000文字）を超えていないか確認してください
```

## 🎨 サンプルデータ

Notionデータベースの構造例：

| プロパティ名 | タイプ | 必須 |
|-------------|--------|------|
| 商品ID | Text | ✅ |
| 名称 | Title | ✅ |
| 原材料名 | Text | ✅ |
| アレルゲン | Text | ✅ |
| 栄養成分表示 | Text | ✅ |
| 内容量 | Text | ✅ |
| 賞味期限 | Text | ✅ |
| 保存方法 | Text | ✅ |
| 製造者/出荷元 | Text | ✅ |
| Yahoo商品ID | Text | - |
| 楽天商品ID | Text | - |

## 🤝 貢献

改善案や機能追加のアイデアがあれば、お気軽にIssueやPull Requestをお願いします！

## 📄 ライセンス

MIT License

## 📞 サポート

ご質問や問題がありましたら、GitHubのIssuesでお知らせください。

---

**Happy Coding! 🎉**
