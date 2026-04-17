# 📊 リサーチデータ Google Sheets エクスポート - クイックスタート

## ⚡ 3分で完了！

### 状況
バーチャルオフィスの**リサーチ部**で収集したデータが Google Sheets に**自動保存**されるようになりました🎉

---

## 🚀 使い方（3ステップ）

### ステップ 1️⃣: バックエンドサーバーを起動

```bash
cd ~/Desktop/claude/virtual-office
./start_backend.sh
```

以下が表示されたら OK ✓
```
🚀 バーチャルオフィス バックエンドサーバー
📍 リッスン: http://localhost:8888
```

### ステップ 2️⃣: バーチャルオフィスを開く

```bash
open index.html
```

### ステップ 3️⃣: リサーチデータを同期

1. **リサーチ部** タブで データを入力
2. **「📤 リサーチデータをエクスポート」** をクリック
   - JSON ファイルがダウンロード
   - メッセージ表示: ✅ XXX件のデータをダウンロード！
3. **統合部** タブ（🔗）を開く
4. **「📊 Google Sheets に同期」** をクリック
   - メッセージ表示: ✅ Google Sheets に同期完了！
5. **Google Sheets** で確認 → 📊 自動的にデータが同期される！

---

## 📋 必須設定（最初の1回）

### Google Sheets ID を設定

**統合部**（🔗）で以下を入力：

```
Google Sheets ID: あなたのスプレッドシートID
```

**ID の取得方法:**
1. Google Sheets でスプレッドシートを開く
2. URL から ID をコピー
   ```
   https://docs.google.com/spreadsheets/d/【ここがID】/edit
   ```
3. 統合部に貼り付け → **⚙ 設定を保存**

### Google API 認証ファイルを配置

1. [SETUP_GUIDE.md](SETUP_GUIDE.md) に従う
2. `google_sheets_credentials.json` を取得
3. `credentials/` フォルダに配置

```bash
cp ~/.credentials/google_sheets_credentials.json credentials/
```

---

## 📊 結果

### 生成される Google Sheets

| リサーチ日時 | カテゴリ | タイトル | URL | メモ | タグ |
|---|---|---|---|---|---|
| 2024-01-15 10:30 | 💻 テクノロジー | Claude 3 | https://... | 新型AI | AI, Claude |
| 2024-01-14 14:20 | 📊 市場分析 | 市場予測 | https://... | 成長5% | 市場, 予測 |

**自動保存** ✓ → 何度でも同期可能

---

## 🔄 定期自動同期（オプション）

**毎日 09:00 に自動同期したい場合:**

```bash
crontab -e
```

以下を追加：
```
0 9 * * * cd ~/Desktop/claude/virtual-office && python3 export_research_to_sheets.py
```

---

## ⚠️ エラー対応

### ❌ "サーバー接続エラー"
→ バックエンドサーバーが起動していません
```bash
./start_backend.sh
```

### ❌ "スプレッドシート ID が設定されていません"
→ 統合部（🔗）で Google Sheets ID を入力して保存

### ❌ "認証エラー"
→ [SETUP_GUIDE.md](SETUP_GUIDE.md) に従って認証ファイルを配置

---

## 📖 詳細ドキュメント

| ドキュメント | 内容 |
|---|---|
| [RESEARCH_EXPORT_GUIDE.md](RESEARCH_EXPORT_GUIDE.md) | 詳細な使用方法・トラブルシューティング |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Google Sheets API 認証セットアップ |
| [IMPLEMENTATION_REPORT.md](IMPLEMENTATION_REPORT.md) | 実装仕様書 |

---

## 🎯 よくある質問

**Q: 複数人でアクセスできる？**
A: はい。Google Sheets の共有設定で権限を付与すればOK

**Q: リアルタイムに同期される？**
A: いいえ。「同期」ボタンをクリックしたタイミングで同期

**Q: 現在のデータが上書きされるのでは？**
A: いいえ。Google Sheets の既存データは保持されます

**Q: サーバーを停止してもいい？**
A: はい。同期の度に起動してもOK（毎日9時のみなど）

---

## 🎉 これであなたの研究チームは完全デジタル化！

```
バーチャルオフィス
    ↓
リサーチ部で情報収集
    ↓
自動保存（LocalStorage）
    ↓
Google Sheets に同期
    ↓
チーム全体で共有・管理
    ↓
✨ 完全自動ワークフロー実現！
```

---

**何か問題があれば、[RESEARCH_EXPORT_GUIDE.md](RESEARCH_EXPORT_GUIDE.md) を参照するか、ログファイルを確認してください:**

```bash
tail -f ~/Desktop/claude/virtual-office/server.log
```

Happy researching! 🚀📊
