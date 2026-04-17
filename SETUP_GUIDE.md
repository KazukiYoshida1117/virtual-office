# 🚀 Google Sheets & Notion 統合セットアップガイド

## 📊 Google Sheets API セットアップ

### 1. Google Cloud Platform プロジェクト作成
```bash
# ブラウザで以下を開く
https://console.cloud.google.com/

# 新しいプロジェクトを作成
# プロジェクト名: "Virtual Office"
```

### 2. Google Sheets API を有効化
```
1. Google Cloud Console にアクセス
2. 「ライブラリ」から "Google Sheets API" を検索
3. 「有効にする」をクリック
```

### 3. サービスアカウントを作成
```
1. 左側メニューから「認証情報」を選択
2. 「認証情報を作成」→「サービスアカウント」
3. サービスアカウント名: virtual-office-service
4. 完了後、「鍵を追加」→「JSON」を選択
5. ダウンロードした JSON ファイルを以下の場所に保存:

/Users/kazukiyoshida/Desktop/claude/virtual-office/credentials/
google_sheets_credentials.json
```

### 4. スプレッドシートを作成

https://sheets.google.com/

スプレッドシートを新規作成して、以下の ID をメモしておく：
```
スプレッドシート ID: https://docs.google.com/spreadsheets/d/{SHEET_ID}/...
↑ この長い英数字の部分
```

### 5. スプレッドシートに共有設定
- サービスアカウントのメールアドレス（JSON ファイルの `client_email` 参照）
- スプレッドシートの共有設定で「編集者」を付与

---

## 🔗 Notion API セットアップ

### 1. Notion Integration を作成
```
1. https://www.notion.so/my-integrations にアクセス
2. 「新しいインテグレーション」を作成
3. 名前: "Virtual Office"
4. 能力: 「コンテンツの読み書き」をチェック
5. 「送信」で確認
```

### 2. Notion API キーを取得
```
インテグレーション作成後、表示される「Secrets」から
トークンをコピー：

NOTION_API_KEY = sk-...

以下にファイルを作成して保存:
/Users/kazukiyoshida/Desktop/claude/virtual-office/.env

内容:
NOTION_API_KEY=sk-xxxxxxxxxxxx
```

### 3. Notion Database を作成
```
1. https://notion.so で新しいページ作成
2. 「データベース」（FullPage）を追加
3. 名前: "Virtual Office Sync"
4. プロパティを追加:
   - Title: 項目名 (default)
   - Category: 選択肢（企画部, リサーチ部, 執務部, etc）
   - Status: 選択肢（新規, 進行中, 完了）
   - Description: テキスト
   - Updated: 作成日時 (default)
```

### 4. Notion Database ID をメモ
```
Database URL: https://www.notion.so/XXXXXXXX?v=YYYYYYYY
↑ XXXXXXXX の部分が Database ID

.env に追加:
NOTION_DB_ID=xxxxxxxxxxxxxxxx
```

---

## ✅ セットアップ完了後

以下のコマンドを実行して認証を確認:

```bash
cd /Users/kazukiyoshida/Desktop/claude/virtual-office
python3 setup_credentials.py
```

成功メッセージが表示されたら準備完了です！
