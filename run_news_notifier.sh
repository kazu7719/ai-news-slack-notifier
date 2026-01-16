#!/bin/bash
# AIニュース通知スクリプトの実行ラッパー

# エラーが発生したら即座に終了
set -e

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# ログファイルの絶対パス
LOG_FILE="$(pwd)/logs/cron.log"

# 実行開始をログに記録
echo "===========================================" >> "$LOG_FILE"
echo "実行開始: $(date)" >> "$LOG_FILE"

# ネットワーク接続を待機（スリープ復帰直後対策）
echo "ネットワーク接続を確認中..." >> "$LOG_FILE"
MAX_RETRY=30
RETRY_COUNT=0
while ! ping -c 1 8.8.8.8 > /dev/null 2>&1; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -ge $MAX_RETRY ]; then
        echo "ネットワーク接続タイムアウト" >> "$LOG_FILE"
        exit 1
    fi
    sleep 2
done
echo "ネットワーク接続OK" >> "$LOG_FILE"

# 仮想環境をアクティベート
source venv/bin/activate

# Pythonスクリプトを実行
python main.py >> "$LOG_FILE" 2>&1

# 実行日時をログに記録
echo "実行完了: $(date)" >> "$LOG_FILE"
echo "===========================================" >> "$LOG_FILE"
