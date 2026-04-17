#!/bin/bash
# バーチャルオフィス バックエンドサーバー起動スクリプト

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
DATA_DIR="$ROOT_DIR/data"

echo "🚀 バーチャルオフィス バックエンドサーバーを起動中..."
echo ""

# Python環境の確認
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 がインストールされていません"
    exit 1
fi

# .env ファイルの確認
if [ ! -f "$DATA_DIR/.env" ]; then
    echo "⚠ .env ファイルが見つかりません"
    echo "  → .env.example をコピーして設定してください："
    echo "  cp $DATA_DIR/.env.example $DATA_DIR/.env"
    echo ""
fi

# バックエンドサーバーを起動
echo "📝 ログファイル: $BACKEND_DIR/server.log"
echo "🌐 ブラウザを開いて: http://localhost:8888/status"
echo ""
echo "Ctrl+C で停止"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd "$BACKEND_DIR"
python3 "$BACKEND_DIR/backend_server.py"
