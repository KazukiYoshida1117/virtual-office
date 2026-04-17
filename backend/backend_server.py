#!/usr/bin/env python3
"""
バーチャルオフィス バックエンドサーバー
HTMLからのリクエストを受け取ってPythonスクリプトを実行
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import logging
from datetime import datetime
from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR   = SCRIPT_DIR.parent
DATA_DIR   = ROOT_DIR / 'data'
load_dotenv(DATA_DIR / '.env')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(SCRIPT_DIR / 'server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VirtualOfficeHandler(BaseHTTPRequestHandler):
    """HTTP リクエストハンドラー"""
    
    def do_GET(self):
        """GET リクエスト処理"""
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            status = {
                'status': 'running',
                'timestamp': datetime.now().isoformat(),
                'version': '1.0'
            }
            self.wfile.write(json.dumps(status, ensure_ascii=False).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """POST リクエスト処理"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
        except:
            data = {}
        
        path = self.path
        logger.info(f"📨 POST {path} からのリクエスト受け取り")
        
        response = {'success': True, 'message': '処理中...', 'data': {}}
        
        if path == '/api/sync-research-to-sheets':
            response = self._sync_research_to_sheets(data)
        
        elif path == '/api/export-research':
            response = self._export_research(data)
        
        else:
            response = {'success': False, 'message': 'エンドポイントが見つかりません'}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
        logger.info(f"✓ レスポンス: {response.get('message', 'OK')}")
    
    def do_OPTIONS(self):
        """CORS プリフライトリクエスト"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _sync_research_to_sheets(self, data):
        """リサーチデータをGoogle Sheetsに同期"""
        logger.info("🚀 リサーチデータのGoogle Sheets同期開始...")
        
        try:
            # export_research_to_sheets.py を実行
            script_path = SCRIPT_DIR / 'export_research_to_sheets.py'
            
            if not script_path.exists():
                return {
                    'success': False,
                    'message': f'❌ スクリプトが見つかりません: {script_path}'
                }
            
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info("✅ リサーチデータのGoogle Sheets同期完了！")
                return {
                    'success': True,
                    'message': '✅ リサーチデータをGoogle Sheetsに同期しました！',
                    'output': result.stdout
                }
            else:
                error_msg = result.stderr or result.stdout
                logger.error(f"❌ 同期エラー: {error_msg}")
                return {
                    'success': False,
                    'message': f'❌ 同期処理でエラーが発生: {error_msg}',
                    'error': error_msg
                }
        
        except subprocess.TimeoutExpired:
            logger.error("❌ タイムアウト")
            return {
                'success': False,
                'message': '❌ 処理がタイムアウトしました（30秒以上）'
            }
        
        except Exception as e:
            logger.error(f"❌ エラー: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'message': f'❌ エラーが発生しました: {str(e)}'
            }
    
    def _export_research(self, data):
        """リサーチデータをファイルに保存"""
        logger.info("💾 リサーチデータをファイルに保存...")
        
        try:
            research_data = data.get('research', [])
            timestamp = data.get('timestamp', datetime.now().isoformat())
            
            export_data = {
                'timestamp': timestamp,
                'count': len(research_data),
                'research': research_data
            }
            
            # research_export.json に保存
            export_file = SCRIPT_DIR / 'research_export.json'
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✓ {len(research_data)} 件のデータをファイルに保存")
            
            return {
                'success': True,
                'message': f'✓ {len(research_data)} 件のデータを保存しました',
                'file': str(export_file),
                'count': len(research_data)
            }
        
        except Exception as e:
            logger.error(f"❌ 保存エラー: {e}")
            return {
                'success': False,
                'message': f'❌ ファイル保存でエラー: {str(e)}'
            }
    
    def log_message(self, format, *args):
        """ログ出力をカスタマイズ"""
        logger.info(f"{format % args}")

def main():
    """メインサーバー処理"""
    port = int(os.getenv('BACKEND_PORT', 8888))
    
    print("=" * 60)
    print("🚀 バーチャルオフィス バックエンドサーバー")
    print("=" * 60)
    print(f"📍 リッスン: http://localhost:{port}")
    print("ログ: virtual-office/server.log")
    print()
    print("利用可能なエンドポイント:")
    print(f"  • GET  http://localhost:{port}/status")
    print(f"  • POST http://localhost:{port}/api/sync-research-to-sheets")
    print(f"  • POST http://localhost:{port}/api/export-research")
    print()
    print("Ctrl+C で終了")
    print("=" * 60)
    
    try:
        server = HTTPServer(('localhost', port), VirtualOfficeHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("\n🛑 サーバーを停止しました")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ サーバーエラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
