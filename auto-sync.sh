#!/bin/bash

export PATH="/opt/homebrew/bin:$PATH"
REPO="/Users/kazukiyoshida/Desktop/claude/virtual-office"

echo "自動同期を開始しました。ファイルを保存すると自動でGitHubに反映されます。"
echo "停止するには Ctrl+C を押してください。"

fswatch -o "$REPO/index.html" | while read; do
  cd "$REPO"
  git add index.html
  git commit -m "update"
  git push
  echo "✓ GitHubに同期しました $(date '+%H:%M:%S')"
done
