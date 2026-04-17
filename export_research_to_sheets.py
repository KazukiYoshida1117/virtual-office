#!/usr/bin/env python3
"""
リサーチデータをGoogle Sheetsに自動エクスポートするスクリプト
バーチャルオフィスの LocalStorage データを読み込んで Google Sheets に反映
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).parent

# Google Sheets 認証
try:
    from google.oauth2.service_account import Credentials
    import gspread
    from dotenv import load_dotenv
except ImportError:
    logger.error("必要なライブラリがインストールされていません")
    logger.error("pip install gspread google-auth-oauthlib google-auth-httplib2 python-dotenv")
    sys.exit(1)

load_dotenv(SCRIPT_DIR / '.env')

def export_research_to_sheets():
    """リサーチデータをGoogle Sheetsにエクスポート"""
    
    logger.info("🚀 リサーチデータのGoogle Sheets エクスポート開始...")
    
    # 1. 認証情報を読み込み
    try:
        creds_file = SCRIPT_DIR / 'credentials' / 'google_sheets_credentials.json'
        if not creds_file.exists():
            logger.error(f"❌ 認証ファイルが見つかりません: {creds_file}")
            logger.error("SETUP_GUIDE.md を参照して認証情報を配置してください")
            return False
        
        creds = Credentials.from_service_account_file(
            str(creds_file),
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        sheets_client = gspread.authorize(creds)
        logger.info("✓ Google Sheets 認証完了")
    except Exception as e:
        logger.error(f"❌ 認証エラー: {e}")
        return False
    
    # 2. スプレッドシートを開く
    try:
        sheet_id = os.getenv('GOOGLE_SHEETS_ID')
        if not sheet_id:
            logger.error("❌ .env に GOOGLE_SHEETS_ID が設定されていません")
            return False
        
        sheet = sheets_client.open_by_key(sheet_id)
        logger.info(f"✓ スプレッドシート '{sheet.title}' を開きました")
    except Exception as e:
        logger.error(f"❌ スプレッドシート読み込みエラー: {e}")
        return False
    
    # 3. リサーチデータファイルを読み込む
    research_export_file = SCRIPT_DIR / 'research_export.json'
    
    try:
        if research_export_file.exists():
            with open(research_export_file, 'r', encoding='utf-8') as f:
                export_data = json.load(f)
                research_data = export_data.get('research', [])
                logger.info(f"✓ 保存済みデータを読み込み ({len(research_data)} 件)")
        else:
            logger.warning(f"⚠ {research_export_file} が見つかりません")
            logger.warning("  バーチャルオフィスでリサーチデータをエクスポートしてください")
            return False
    except Exception as e:
        logger.error(f"❌ データ読み込みエラー: {e}")
        return False
    
    # 4. 「リサーチ部」シートを探すか作成
    try:
        worksheets = sheet.worksheets()
        research_ws = None
        for ws in worksheets:
            if 'リサーチ' in ws.title or '研究' in ws.title:
                research_ws = ws
                break
        
        if not research_ws:
            logger.info("📄 新規シート「リサーチ部」を作成中...")
            research_ws = sheet.add_worksheet('リサーチ部', rows=1000, cols=10)
        
        logger.info(f"✓ シート '{research_ws.title}' を使用")
    except Exception as e:
        logger.error(f"❌ シート作成エラー: {e}")
        return False
    
    # 5. ヘッダーを設定
    try:
        headers = ['リサーチ日時', 'カテゴリ', 'タイトル', 'URL', 'メモ', 'タグ']
        research_ws.clear()
        research_ws.insert_row(headers, 1)
        logger.info("✓ ヘッダーを設定")
    except Exception as e:
        logger.error(f"❌ ヘッダー設定エラー: {e}")
        return False
    
    # 6. データを行ごとに書き込む
    try:
        rows_to_insert = []
        for r in research_data:
            # タイムスタンプをフォーマット
            timestamp = r.get('date', 0)
            if isinstance(timestamp, (int, float)) and timestamp > 0:
                dt = datetime.fromtimestamp(timestamp / 1000) if timestamp > 10000000000 else datetime.fromtimestamp(timestamp)
                date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            else:
                date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            category = r.get('category', '未分類')
            title = r.get('title', '')
            url = r.get('url', '')
            memo = r.get('memo', '')
            tags = ', '.join(r.get('tags', []))
            
            row_data = [date_str, category, title, url, memo, tags]
            rows_to_insert.append(row_data)
        
        if rows_to_insert:
            start_row = 2
            end_row = start_row + len(rows_to_insert) - 1
            cell_range = f'A{start_row}:F{end_row}'
            research_ws.update(cell_range, rows_to_insert)
            logger.info(f"✓ {len(rows_to_insert)} 件のデータをGoogle Sheetsに書き込み完了！")
        else:
            logger.warning("⚠ 書き込むリサーチデータがありません")
    except Exception as e:
        logger.error(f"❌ データ書き込みエラー: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    logger.info("✅ リサーチデータのエクスポート完了！")
    return True

def main():
    """メイン処理"""
    print("=" * 60)
    print("📊 リサーチデータ Google Sheets エクスポーター")
    print("=" * 60)
    
    success = export_research_to_sheets()
    
    if success:
        print("\n✅ エクスポートに成功しました！")
        print(f"Google Sheet を確認してください: https://sheets.google.com/")
        return 0
    else:
        print("\n❌ エクスポートに失敗しました")
        print("トラブルシューティング:")
        print("1. .env ファイルに GOOGLE_SHEETS_ID が設定されているか確認")
        print("2. credentials/google_sheets_credentials.json が存在するか確認")
        print("3. バーチャルオフィスでリサーチデータをエクスポートしたか確認")
        return 1

if __name__ == "__main__":
    sys.exit(main())
