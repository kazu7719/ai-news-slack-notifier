#!/bin/bash
# AIニュース通知スクリプトの実行ラッパー

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# 仮想環境をアクティベート
source venv/bin/activate

# Pythonスクリプトを実行
python main.py >> logs/cron.log 2>&1

# 実行日時をログに記録
echo "実行完了: $(date)" >> logs/cron.log
