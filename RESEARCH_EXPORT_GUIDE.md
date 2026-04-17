# 🔄 リサーチデータ Google Sheets エクスポートガイド

バーチャルオフィスの**リサーチ部**で収集したデータを、Google Sheets に自動エクスポートするための完全ガイドです。

## 📋 概要

このシステムでは以下の流れでリサーチデータが Google Sheets に同期されます：

```
バーチャルオフィス (HTML/LocalStorage)
    ↓
JSONファイルにエクスポート
    ↓
Pythonバックエンドサーバー
    ↓
Google Sheets API (gspread)
    ↓
Google Sheets に自動保存
```

## 🚀 初回セットアップ

### 1. Google Sheets APIの準備

まず、以下の手順に従って Google Sheets API の認証情報を取得してください。詳細は [SETUP_GUIDE.md](SETUP_GUIDE.md) を参照：

```bash
# 認証ファイルを配置
cp ~/.credentials/google_sheets_credentials.json ./credentials/
```

### 2. 環境設定

`.env` ファイルに Google Sheets ID を設定：

```bash
# .env ファイルを作成
cp .env.example .env

# 以下を編集します：
# GOOGLE_SHEETS_ID=あなたのスプレッドシートID
# NOTION_API_KEY=（Notion同期を使う場合）
# NOTION_DB_ID=（Notion同期を使う場合）
```

Google Sheets ID の取得方法：
- Google Sheets で共有したいスプレッドシートを開く
- URL から ID をコピー：`https://docs.google.com/spreadsheets/d/【ID】/edit`

### 3. 必要ライブラリのインストール

```bash
pip install -r requirements.txt
```

または手動インストール：

```bash
pip install gspread google-auth-oauthlib google-auth-httplib2 python-dotenv
```

## 📊 使用方法

### ステップ 1: バーチャルオフィスでリサーチデータを追加

1. ブラウザで `index.html` を開く
2. 左タブから **リサーチ部** をクリック
3. 新規リサーチ追加フォームでデータを入力：
   - **タイトル**: 記事やサイトのタイトル
   - **カテゴリ**: 💻テクノロジー, 📊市場分析, etc
   - **URL**: 情報元のリンク（任意）
   - **メモ**: 重要な要点や感想
   - **タグ**: 複数のタグをカンマで区切って入力
4. **保存** をクリック

### ステップ 2: Google Sheets にエクスポート

#### 方法 A: 自動同期（推奨）

1. **バックエンドサーバーを起動**（初回のみ、またはコンピューター再起動後）

```bash
# 方法1: シェルスクリプトで起動（最も簡単）
./start_backend.sh

# 方法2: 直接Pythonスクリプトで起動
python3 backend_server.py
```

出力例：
```
============================================================
🚀 バーチャルオフィス バックエンドサーバー
============================================================
📍 リッスン: http://localhost:8888
ログ: virtual-office/server.log

利用可能なエンドポイント:
  • GET  http://localhost:8888/status
  • POST http://localhost:8888/api/sync-research-to-sheets
  • POST http://localhost:8888/api/export-research
```

2. **リサーチ部パネルで「📤 リサーチデータをエクスポート」をクリック**
   - JSON ファイルがダウンロードされます
   - status: ✅ X件のデータをダウンロード！

3. **統合部で「📊 Google Sheets に同期」をクリック**
   - バックエンドサーバーが自動的に Python スクリプトを実行
   - リサーチデータが Google Sheets に書き込まれます
   - status: ✅ Google Sheets に同期完了！

#### 方法 B: 手動実行（サーバーを使わない場合）

バックエンドサーバーを起動せずに、直接Pythonスクリプトを実行：

```bash
# 1. 最初に JSONファイルをダウンロード（HTMLから実行）
# 2. export_research_to_sheets.py を実行
python3 export_research_to_sheets.py
```

出力例：
```
============================================================
📊 リサーチデータ Google Sheets エクスポーター
============================================================
🚀 リサーチデータのGoogle Sheets エクスポート開始...
✓ Google Sheets 認証完了
✓ スプレッドシート 'My Virtual Office' を開きました
✓ 保存済みデータを読み込み (3 件)
✓ シート 'リサーチ部' を使用
✓ ヘッダーを設定
✓ 3 件のデータをGoogle Sheetsに書き込み完了！
✅ リサーチデータのエクスポート完了！
```

## 📈 生成される Google Sheets

### リサーチ部シート

**列構成:**
| リサーチ日時 | カテゴリ | タイトル | URL | メモ | タグ |
|---|---|---|---|---|---|
| 2024-01-15 10:30:45 | 💻 テクノロジー | Claude 3 リリース | https://... | 次世代AI... | AI, Claude |
| 2024-01-14 14:20:12 | 📊 市場分析 | 2024年マーケット予測 | https://... | 成長率5%... | 市場, 予測 |

**機能:**
- ✅ 日時タイムスタンプ（YYYY-MM-DD HH:MM:SS形式）
- ✅ カテゴリ別分類
- ✅ ハイパーリンク対応（URLクリック可能）
- ✅ メモと複数タグの保存
- ✅ 自動ソート機能対応

### トレンドシート

Notion同期を有効にした場合、トレンドデータも自動作成：

| プラットフォーム | ランク | キーワード | 関心度 | 更新日時 |
|---|---|---|---|---|
| Google | 1 | AI市場 | 高 | 2024-01-15 |
| Twitter | 2 | 新製品 | 高 | 2024-01-15 |

## 🔧 トラブルシューティング

### ❌ エラー: "認証エラー"

**原因:** Google認証ファイルが見つからない or 無効

**解決策:**
```bash
# 認証ファイルの確認
ls -la credentials/google_sheets_credentials.json

# SETUP_GUIDE.md に従って再度認証ファイルを取得
```

### ❌ エラー: ".env に GOOGLE_SHEETS_ID が設定されていません"

**解決策:**
```bash
# .env ファイルを編集
nano .env

# 以下を追加:
GOOGLE_SHEETS_ID=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
```

### ❌ エラー: "サーバー接続エラー: Failed to fetch"

**原因:** バックエンドサーバーが起動していない

**解決策:**
```bash
# バックエンドサーバーを起動
./start_backend.sh
# または
python3 backend_server.py
```

サーバー起動後、テスト接続：
```bash
curl http://localhost:8888/status
```

### ❌ エラー: "スプレッドシート ID が設定されていません"

**解決策:**
1. 統合部を開く（🔗 統合部）
2. 「Google Sheets ID」に スプレッドシートIDを入力
3. 「⚙ 設定を保存」をクリック
4. 再度同期を試す

## 🔐 セキュリティ対策

### 認証ファイルの管理

```bash
# 秘密ファイルを .gitignore に追加（既に設定済み）
echo "credentials/" >> .gitignore
echo ".env" >> .gitignore

# 重要: 認証ファイルを Git にコミットしないこと！
git status  # 確認
```

### API キーの保護

- `.env` ファイルは絶対に Git にコミットしない
- `credentials/*.json` も同様
- 他人にこれらのファイルを見せない

## 📅 定期実行（オプション）

### macOS/Linux: cron で自動実行

毎日 09:00 に自動同期を実行：

```bash
# crontab を編集
crontab -e

# 以下の行を追加:
0 9 * * * cd /Users/yourname/Desktop/claude/virtual-office && python3 export_research_to_sheets.py >> sync.log 2>&1
```

確認：
```bash
crontab -l
```

### バックエンドサーバーの永続化

Mac の LaunchAgent で常時実行：

```bash
# LaunchAgent ファイルを作成
cat > ~/Library/LaunchAgents/com.virtualoffice.backend.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.virtualoffice.backend</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/yourname/Desktop/claude/virtual-office/backend_server.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/yourname/Desktop/claude/virtual-office</string>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/yourname/Desktop/claude/virtual-office/backend.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/yourname/Desktop/claude/virtual-office/backend.error.log</string>
</dict>
</plist>
EOF

# サービスを有効化
launchctl load ~/Library/LaunchAgents/com.virtualoffice.backend.plist

# ステータス確認
launchctl list | grep virtualoffice
```

## 💡 ベストプラクティス

### 1. 定期的にデータをバックアップ

```bash
# Google Sheets をダウンロード
# → メニュー > ファイル > ダウンロード > CSV

# または自動バックアップ
cp ~/Desktop/claude/virtual-office/research_export.json ~/Backups/research_$(date +%Y%m%d).json
```

### 2. タグの統一運用

カテゴリ例:
- AI/機械学習
- データベース
- クラウド
- セキュリティ
- UI/UX
- マーケティング

### 3. メモは簡潔に

良い例: "Claude 3 は 4x 高速。API価格 50%低下"
悪い例: "新しいAIのリリースがありました"

### 4. URLは共有可能なものを

- ✅ https://example.com/article
- ❌ http://localhost:3000/draft

## 📞 サポート

詳細な Google Sheets 設定上については `SETUP_GUIDE.md` を参照してください。

問題が発生した場合：
1. `server.log` でエラーを確認
2. `python3 export_research_to_sheets.py` を直接実行してみる
3. `.env` の設定を確認
4. 認証ファイルが正しく配置されているか確認

---

**バージョン:** 1.0  
**最終更新:** 2024年1月  
