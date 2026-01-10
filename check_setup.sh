#!/bin/bash
# セットアップ状態チェックスクリプト

echo "========================================="
echo "AIニュース通知 セットアップチェック"
echo "========================================="
echo ""

# カレントディレクトリ
echo "📁 プロジェクトディレクトリ:"
pwd
echo ""

# Python仮想環境
echo "🐍 Python仮想環境:"
if [ -d "venv" ]; then
    echo "  ✅ 仮想環境が存在します"
else
    echo "  ❌ 仮想環境が見つかりません"
fi
echo ""

# 依存パッケージ
echo "📦 依存パッケージ:"
if [ -d "venv" ]; then
    source venv/bin/activate
    if pip show feedparser requests python-dotenv > /dev/null 2>&1; then
        echo "  ✅ すべてのパッケージがインストールされています"
        pip list | grep -E "(feedparser|requests|python-dotenv)" | sed 's/^/    /'
    else
        echo "  ⚠️  一部のパッケージが不足しています"
    fi
    deactivate
else
    echo "  ⚠️  仮想環境が存在しないため確認できません"
fi
echo ""

# .envファイル
echo "🔑 環境変数設定:"
if [ -f ".env" ]; then
    echo "  ✅ .envファイルが存在します"

    # Gemini API Key確認
    if grep -q "GEMINI_API_KEY=your_gemini_api_key_here" .env; then
        echo "  ❌ GEMINI_API_KEYが未設定です"
    elif grep -q "GEMINI_API_KEY=.*[a-zA-Z0-9]" .env; then
        echo "  ✅ GEMINI_API_KEYが設定されています"
    else
        echo "  ⚠️  GEMINI_API_KEYの形式を確認してください"
    fi

    # Discord Webhook URL確認
    if grep -q "DISCORD_WEBHOOK_URL=your_discord_webhook_url_here" .env; then
        echo "  ❌ DISCORD_WEBHOOK_URLが未設定です"
    elif grep -q "DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/" .env; then
        echo "  ✅ DISCORD_WEBHOOK_URLが設定されています"
    else
        echo "  ⚠️  DISCORD_WEBHOOK_URLの形式を確認してください"
    fi
else
    echo "  ❌ .envファイルが見つかりません"
fi
echo ""

# 実行権限
echo "⚙️  実行権限:"
if [ -x "main.py" ]; then
    echo "  ✅ main.pyに実行権限があります"
else
    echo "  ⚠️  main.pyに実行権限がありません"
fi

if [ -x "run_news_notifier.sh" ]; then
    echo "  ✅ run_news_notifier.shに実行権限があります"
else
    echo "  ⚠️  run_news_notifier.shに実行権限がありません"
fi
echo ""

# cron設定
echo "⏰ cron設定:"
if crontab -l 2>/dev/null | grep -q "run_news_notifier.sh"; then
    echo "  ✅ crontabに設定されています"
    echo "  設定内容:"
    crontab -l | grep "run_news_notifier.sh" | sed 's/^/    /'
else
    echo "  ⚠️  crontabに未設定です"
fi
echo ""

# 次のステップ
echo "========================================="
echo "次のステップ"
echo "========================================="

# 認証情報が未設定の場合
if grep -q "your_gemini_api_key_here" .env 2>/dev/null || grep -q "your_discord_webhook_url_here" .env 2>/dev/null; then
    echo ""
    echo "📝 認証情報を設定してください:"
    echo ""
    if grep -q "your_gemini_api_key_here" .env 2>/dev/null; then
        echo "  1. Gemini API Keyを取得"
        echo "     https://aistudio.google.com/app/apikey"
        echo ""
    fi
    if grep -q "your_discord_webhook_url_here" .env 2>/dev/null; then
        echo "  2. Discord Webhook URLを取得"
        echo "     Discordチャンネル設定 → 連携サービス → ウェブフック"
        echo ""
    fi
    echo "  3. .envファイルに設定"
    echo "     nano .env"
    echo ""
else
    # cron未設定の場合
    if ! crontab -l 2>/dev/null | grep -q "run_news_notifier.sh"; then
        echo ""
        echo "🧪 まず動作テストを実行してください:"
        echo ""
        echo "  source venv/bin/activate"
        echo "  python main.py"
        echo ""
        echo "✅ テストが成功したら、cron設定を追加してください:"
        echo ""
        echo "  crontab -e"
        echo ""
        echo "  以下の行を追加:"
        echo "  0 8 * * * $(pwd)/run_news_notifier.sh"
        echo ""
    else
        echo ""
        echo "✅ セットアップ完了！"
        echo ""
        echo "毎朝8時にLINEに通知が届きます。"
        echo ""
        echo "📊 ログを確認:"
        echo "  tail -f logs/cron.log"
        echo ""
    fi
fi

echo "詳細なガイドは SETUP_GUIDE.md を参照してください。"
echo ""
