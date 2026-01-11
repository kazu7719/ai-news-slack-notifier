#!/bin/bash
# AIニュース通知スクリプトの実行ラッパー

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# ログファイルの絶対パス
LOG_FILE="$(pwd)/logs/cron.log"

# 実行開始をログに記録
echo "===========================================" >> "$LOG_FILE"
echo "実行開始: $(date)" >> "$LOG_FILE"

# 仮想環境をアクティベート
source venv/bin/activate

# Pythonスクリプトを実行
python main.py >> "$LOG_FILE" 2>&1

# 実行日時をログに記録
echo "実行完了: $(date)" >> "$LOG_FILE"
echo "===========================================" >> "$LOG_FILE"
