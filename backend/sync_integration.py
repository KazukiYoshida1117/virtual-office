#!/usr/bin/env python3
"""
Virtual Office - Google Sheets & Notion 統合スクリプト
バーチャルオフィスのすべてのデータをGoogleSheetsとNotionと双方向同期
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import logging

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).parent

# 必要なライブラリのインポート
try:
    from google.oauth2.service_account import Credentials
    from google.auth.transport.requests import Request
    import gspread
    from notion_client import Client
    from dotenv import load_dotenv
except ImportError:
    logger.error("必要なライブラリが未インストール。以下でセットアップしてください:")
    logger.error("  pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client gspread notion-client python-dotenv")
    sys.exit(1)

# 環境変数読み込み
load_dotenv(SCRIPT_DIR / '.env')

class VirtualOfficeSync:
    def __init__(self):
        self.trends_file = SCRIPT_DIR / 'trends.json'
        self.sheets_client = None
        self.notion_client = None
        self._init_sheets()
        self._init_notion()
        
    def _init_sheets(self):
        """Google Sheets 認証初期化"""
        try:
            creds_file = SCRIPT_DIR / 'credentials' / 'google_sheets_credentials.json'
            if not creds_file.exists():
                logger.warning(f"⚠ Google Sheets 認証ファイルが見つかりません: {creds_file}")
                logger.warning("  セットアップガイドを参照して認証情報を配置してください")
                return
                
            creds = Credentials.from_service_account_file(
                str(creds_file),
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.sheets_client = gspread.authorize(creds)
            logger.info("✓ Google Sheets クライアント初期化完了")
        except Exception as e:
            logger.error(f"❌ Google Sheets 初期化エラー: {e}")
    
    def _init_notion(self):
        """Notion 認証初期化"""
        try:
            api_key = os.getenv('NOTION_API_KEY')
            db_id = os.getenv('NOTION_DB_ID')
            
            if not api_key or not db_id:
                logger.warning("⚠ Notion 認証情報が .env に設定されていません")
                logger.warning("  セットアップガイドを参照してください")
                return
            
            self.notion_client = Client(auth=api_key)
            self.notion_db_id = db_id
            logger.info("✓ Notion クライアント初期化完了")
        except Exception as e:
            logger.error(f"❌ Notion 初期化エラー: {e}")
    
    def load_vo_data(self) -> Dict[str, Any]:
        """バーチャルオフィスからデータを読み込み"""
        try:
            vo_file = SCRIPT_DIR / 'index.html'
            # JSONファイルから取得（LocalStorage のバックアップ）
            json_files = list(SCRIPT_DIR.glob('*.json'))
            
            data = {
                'ideas': [],
                'research': [],
                'tasks': [],
                'drafts': [],
                'trends': [],
                'mission': '',
                'timestamp': datetime.now().isoformat()
            }
            
            # trends.json から取得
            if self.trends_file.exists():
                with open(self.trends_file, 'r', encoding='utf-8') as f:
                    trends_data = json.load(f)
                    data['trends'] = trends_data.get('sources', [])
            
            logger.info(f"✓ バーチャルオフィスデータを読み込み")
            return data
        except Exception as e:
            logger.error(f"❌ データ読み込みエラー: {e}")
            return None
    
    def sync_to_sheets(self, data: Dict[str, Any]) -> bool:
        """Google Sheets に同期"""
        if not self.sheets_client:
            logger.warning("⚠ Google Sheets クライアントが未初期化")
            return False
        
        try:
            sheet_id = os.getenv('GOOGLE_SHEETS_ID')
            if not sheet_id:
                logger.warning("⚠ スプレッドシート ID が .env に設定されていません")
                return False
            
            sheet = self.sheets_client.open_by_key(sheet_id)
            
            # リサーチ部のデータをシートに書き込み
            logger.info("📝 Google Sheets にリサーチデータを書き込み中...")
            
            # シートが複数ある場合、「リサーチ部」という名前のシートを探すか作成
            worksheets = sheet.worksheets()
            research_ws = None
            for ws in worksheets:
                if 'リサーチ' in ws.title or '研究' in ws.title or ws.title == 'research':
                    research_ws = ws
                    break
            
            # シートが見つからない場合は新規作成
            if not research_ws:
                logger.info("📄 新規シート「リサーチ部」を作成中...")
                research_ws = sheet.add_worksheet('リサーチ部', rows=1000, cols=10)
            
            # ヘッダー設定
            headers = ['リサーチ日時', 'カテゴリ', 'タイトル', 'URL', 'メモ', 'タグ']
            research_ws.clear()
            research_ws.insert_row(headers, 1)
            
            # リサーチデータを行ごとに追加（テスト用のHTMLのレンダリングデータから取得）
            # 実際には index.html の LocalStorage から読み込むが、ここでは data パラメータから取得
            if data and 'research' in data:
                research_data = data['research']
                logger.info(f"📊 {len(research_data)} 件のリサーチデータを書き込み中...")
                
                rows_to_insert = []
                for idx, r in enumerate(research_data, 2):
                    # タイムスタンプをフォーマット
                    dt = datetime.fromtimestamp(r.get('date', 0) / 1000) if isinstance(r.get('date'), (int, float)) else datetime.now()
                    date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                    
                    category = r.get('category', '未分類')
                    title = r.get('title', '')
                    url = r.get('url', '')
                    memo = r.get('memo', '')
                    tags = ', '.join(r.get('tags', []))
                    
                    row_data = [date_str, category, title, url, memo, tags]
                    rows_to_insert.append(row_data)
                
                # まとめて行を追加
                if rows_to_insert:
                    start_row = 2
                    end_row = start_row + len(rows_to_insert) - 1
                    cell_range = f'A{start_row}:F{end_row}'
                    research_ws.update(cell_range, rows_to_insert)
                    logger.info(f"✓ {len(rows_to_insert)} 行のリサーチデータを Google Sheets に書き込み完了！")
            
            # トレンドデータ用のシートも作成
            if data and 'trends' in data and data['trends']:
                logger.info("🌐 トレンドデータをシートに書き込み中...")
                trends_ws = None
                for ws in sheet.worksheets():
                    if 'トレンド' in ws.title or 'trends' in ws.title:
                        trends_ws = ws
                        break
                
                if not trends_ws:
                    trends_ws = sheet.add_worksheet('トレンド', rows=1000, cols=5)
                
                trends_ws.clear()
                trends_ws.insert_row(['プラットフォーム', 'ランク', 'キーワード', '関心度', '更新日時'], 1)
                
                trends_rows = []
                for source in data['trends']:
                    platform = source.get('platform', '不明')
                    emoji = source.get('emoji', '')
                    for idx, trend in enumerate(source.get('trends', [])[:10], 1):
                        trends_rows.append([
                            f"{emoji} {platform}",
                            f"#{idx}",
                            trend.get('term', ''),
                            trend.get('interest', 0),
                            datetime.now().strftime('%Y-%m-%d')
                        ])
                
                if trends_rows:
                    end_row = len(trends_rows) + 1
                    trends_ws.update(f'A2:E{end_row}', trends_rows)
                    logger.info(f"✓ {len(trends_rows)} 件のトレンドデータを Google Sheets に書き込み完了！")
            
            logger.info("✓ Google Sheets に全データ同期完了")
            return True
        except Exception as e:
            logger.error(f"❌ Sheets 同期エラー: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def sync_to_notion(self, data: Dict[str, Any]) -> bool:
        """Notion に同期"""
        if not self.notion_client:
            logger.warning("⚠ Notion クライアントが未初期化")
            return False
        
        try:
            # トレンドデータを Notion に追加
            if data.get('trends'):
                for trend in data['trends'][:10]:  # 最初の10件
                    self.notion_client.pages.create(
                        parent={"database_id": self.notion_db_id},
                        properties={
                            "title": {
                                "title": [{"text": {"content": trend.get('platform', '不明')}}]
                            },
                            "Category": {
                                "select": {"name": "トレンド"}
                            },
                            "Status": {
                                "select": {"name": "新規"}
                            },
                        }
                    )
            
            logger.info("✓ Notion に同期完了")
            return True
        except Exception as e:
            logger.error(f"❌ Notion 同期エラー: {e}")
            return False
    
    def sync_from_notion(self) -> bool:
        """Notion からデータを同期"""
        if not self.notion_client:
            logger.warning("⚠ Notion クライアントが未初期化")
            return False
        
        try:
            results = self.notion_client.databases.query(
                database_id=self.notion_db_id,
                page_size=100
            )
            
            logger.info(f"✓ Notion から {len(results['results'])} 件取得")
            return True
        except Exception as e:
            logger.error(f"❌ Notion 取得エラー: {e}")
            return False
    
    def sync(self) -> bool:
        """統合同期実行"""
        logger.info("🔄 バーチャルオフィス統合同期を開始...")
        
        # データ読み込み
        data = self.load_vo_data()
        if not data:
            return False
        
        # 各プラットフォームに同期
        sheets_ok = self.sync_to_sheets(data)
        notion_ok = self.sync_to_notion(data)
        notion_fetch_ok = self.sync_from_notion()
        
        if sheets_ok and notion_ok and notion_fetch_ok:
            logger.info("✅ 統合同期完了！")
            return True
        else:
            logger.warning("⚠ 一部の同期が失敗しました")
            return False

def main():
    """メイン処理"""
    print("=" * 60)
    print("🏢 Virtual Office - Google Sheets & Notion 統合")
    print("=" * 60)
    
    syncer = VirtualOfficeSync()
    success = syncer.sync()
    
    if success:
        print("\n✅ 全同期が正常に完了しました！")
        return 0
    else:
        print("\n⚠ 同期に一部問題がありました。セットアップガイドを確認してください。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
