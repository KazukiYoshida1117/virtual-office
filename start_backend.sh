#!/bin/bash
# バーチャルオフィス バックエンドサーバー起動スクリプト

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 バーチャルオフィス バックエンドサーバーを起動中..."
echo ""

# Python環境の確認
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 がインストールされていません"
    exit 1
fi

# 必要なパッケージの確認と作成
if [ ! -f ".env" ]; then
    echo "⚠ .env ファイルが見つかりません"
    echo "  → .env.example をコピーして設定してください："
    echo "  cp .env.example .env"
    echo ""
fi

# バックエンドサーバーを起動
echo "📝 ログファイル: $SCRIPT_DIR/server.log"
echo "🌐 ブラウザを開いて: http://localhost:8888/status"
echo ""
echo "Ctrl+C で停止"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 "$SCRIPT_DIR/backend_server.py"
