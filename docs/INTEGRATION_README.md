# 🏢 バーチャルオフィス - Google Sheets & Notion 統合ガイド

## 📚 クイックスタート

### ファイル構成
```
virtual-office/
├── index.html                    # メインUI
├── fetch_trends.py               # トレンド自動取得
├── sync_integration.py           # 統合同期スクリプト
├── SETUP_GUIDE.md               # セットアップ詳細ガイド
├── .env.example                 # 環境変数テンプレート
└── credentials/                 # 認証ファイル格納フォルダ
    └── google_sheets_credentials.json
```

---

## 🚀 セットアップ手順（初回のみ）

### ステップ1: Google Cloud Setup
1. https://console.cloud.google.com/ にアクセス
2. **新規プロジェクト作成**: "Virtual Office"  
3. **Google Sheets API を有効化**
4. **サービスアカウント作成**:
   - 認証情報 → 認証情報を作成 → サービスアカウント
   - 名前: `virtual-office-service`
   - JSON キーをダウンロード
5. ファイルをここに保存:
   ```
   credentials/google_sheets_credentials.json
   ```

### ステップ2: Google Sheets 準備
1. https://sheets.google.com で新規スプレッドシート作成
2. URL から ID をコピー:
   ```
   https://docs.google.com/spreadsheets/d/{SHEET_ID}/...
   ```
3. スプレッドシートを共有:
   - 共有ボタン → サービスアカウントメール（credentials JSON の `client_email`）
   - 権限: **編集者**

### ステップ3: Notion Setup
1. https://www.notion.so/my-integrations にアクセス
2. **インテグレーション作成**:
   - 名前: "Virtual Office"
   - 能力: ✓ コンテンツの読み書き
3. **API キーをコピー** (表示される `Secrets` から)
4. Notion でデータベース作成:
   - 新規ページ → データベース追加
   - プロパティ設定:
     - `Title`: 項目名 (Default)
     - `Category`: 選択肢
     - `Status`: 選択肢
     - `Updated`: 作成日時

### ステップ4: 環境変数設定
`.env` ファイルを作成:

```bash
cp .env.example .env
```

`.env` ファイルを編集:
```env
GOOGLE_SHEETS_ID=YOUR_SHEET_ID
NOTION_API_KEY=sk-xxxxxxxxxx
NOTION_DB_ID=xxxxxxxxxxxxxxxx
SYNC_INTERVAL_HOURS=1
ENABLE_AUTO_SYNC=true
```

### ステップ5: Python パッケージインストール
```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client gspread notion-client python-dotenv
```

---

## 🎮 バーチャルオフィスでの使用方法

### 統合部へのアクセス
1. バーチャルオフィスを開く
2. **オフィスフロア** から **「🔗 統合部」** をクリック
3. または `index.html` 内で:
   ```javascript
   openModal('integrate')
   ```

### UI 機能

#### 📊 同期ステータス
- リアルタイムで接続状态を表示
- Google Sheets, Notion, バーチャルオフィスの接続状態

#### 同期ボタン
| ボタン | 機能 | 用途 |
|--------|------|------|
| 📊 Google Sheets に同期 | バーチャルオフィスのデータを Google Sheets に送信 | 定期レポート作成 |
| 🔗 Notion に同期 | バーチャルオフィスのデータを Notion に送信 | チーム共有 |
| ⬇ Notion から取得 | Notion のデータをバーチャルオフィスに取り込み | 逆同期 |
| 🔄 完全同期 | すべてのデータを双方向同期 | 確実な同期 |

#### APIキー管理
- Google Sheets ID 設定
- Notion API キー設定
- Notion Database ID 設定
- ⚙ **設定を保存** ボタンで LocalStorage に保存

#### 同期ログ
全ての操作をリアルタイムでログ表示

---

## ⚡ 自動同期設定

### Cron ジョブで定期実行

毎日 08:00 に自動同期するには:

```bash
crontab -e
```

以下を追加:

```
0 8 * * * cd /Users/kazukiyoshida/Desktop/claude/virtual-office && /usr/bin/python3 sync_integration.py >> /tmp/vo_sync.log 2>&1
```

### ログ確認
```bash
tail -f /tmp/vo_sync.log
```

---

## 📊 同期対象データ

### バーチャルオフィス → Google Sheets
- ✓ リサーチ部のすべての項目
- ✓ 企画部のアイデア
- ✓ 執務部のタスク
- ✓ SNS展開部の下書き
- ✓ トレンド情報

### バーチャルオフィス ↔ Notion
- ✓ すべてのデータ項目
- ✓ メタデータ（日付、カテゴリ）
- ✓ タグ・ステータス情報

---

## 🔧 トラブルシューティング

### ❌ "Google Sheets 認証ファイルが見つかりません"
→ `credentials/google_sheets_credentials.json` が正しい場所に保存されているか確認

### ❌ "Notion 認証情報が .env に設定されていません"
→ `.env` ファイルが `/virtual-office/` ルートに存在し、`NOTION_API_KEY` と `NOTION_DB_ID` が設定されているか確認

### ❌ "スプレッドシート ID が .env に設定されていません"
→ `.env` に `GOOGLE_SHEETS_ID` が正しく設定されているか確認

### ❌ 同期ボタンが反応しない
→ ブラウザのコンソール（F12 → Console）でエラーを確認

---

## 📝 スクリプト実行方法

### 手動同期実行
```bash
cd /Users/kazukiyoshida/Desktop/claude/virtual-office
python3 sync_integration.py
```

### トレンド情報のみ更新
```bash
python3 fetch_trends.py
```

---

## 🔐 セキュリティ注意事項

- ⚠️ `.env` ファイルを Git リポジトリに追加しないこと
- ⚠️ `credentials/` フォルダは `.gitignore` に追加
- ⚠️ API キーを絶対に第三者と共有しない
- ⚠️ 定期的にキーをローテーション

---

## 📖 参考リンク

- [Google Sheets API](https://developers.google.com/sheets/api)
- [Notion API Documentation](https://developers.notion.com)
- [gspread Documentation](https://docs.gspread.org/)
- [notion-client Python](https://github.com/ramnes/notion-sdk-py)

---

## 💡 ヒント

- バーチャルオフィスのデータは LocalStorage に保存されます
- `DB.load()` で読み込み、`DB.save()` で保存
- 統合部は UI でデータを管理するだけで、実際の同期は Python スクリプトで実行
- Sheets と Notion のどちらでもデータの単一ソースとして機能可能

---

**Happy workspace management! 🚀**
