# クイックスタート

このファイルは、最速でAIニュース通知を始めるための手順をまとめています。

## 3ステップで開始

### ステップ1: 現在の状態を確認

```bash
cd /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier
./check_setup.sh
```

このスクリプトが、何が完了していて何が必要かを教えてくれます。

### ステップ2: 認証情報を取得して設定

#### 2-1. Anthropic API Keyを取得

1. https://console.anthropic.com/settings/keys を開く
2. 「Create Key」でキーを作成
3. `sk-ant-api03-...` で始まるキーをコピー

#### 2-2. LINE Notify Tokenを取得

1. https://notify-bot.line.me/my/ を開く
2. 「トークンを発行する」をクリック
3. トークン名: `AIニュース通知`
4. 通知先: `1:1でLINE Notifyから通知を受け取る`
5. 発行されたトークンをコピー（⚠️ この画面でしか表示されません！）

#### 2-3. .envファイルに設定

```bash
nano .env
```

以下のように編集:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
LINE_NOTIFY_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxx
```

保存: `Ctrl+X` → `Y` → `Enter`

### ステップ3: 動作テスト

```bash
source venv/bin/activate
python main.py
```

LINEに通知が届けば成功です！

## 自動実行を設定（オプション）

毎朝8時に自動実行したい場合:

```bash
crontab -e
```

以下を追加:
```
0 8 * * * /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier/run_news_notifier.sh
```

保存して終了。

## トラブルシューティング

エラーが出た場合は `./check_setup.sh` を実行して、何が不足しているか確認してください。

詳細なガイド:
- **SETUP_GUIDE.md** - 詳細な手順とトラブルシューティング
- **CRON_SETUP.md** - cron設定の詳細
- **README.md** - 完全なドキュメント

## よくある質問

**Q: お金はかかりますか？**
A: Anthropic APIの利用料金がかかります（1回の実行で数円程度）。LINE Notifyは無料です。

**Q: 通知の頻度を変更できますか？**
A: はい。crontabの設定を変更してください（CRON_SETUP.mdを参照）。

**Q: 取得するニュースの数を変更できますか？**
A: はい。main.pyの `max_articles=3` を変更してください。

**Q: macOS以外でも動きますか？**
A: はい。Linux、Windowsでも動作します（Windowsの場合、cronの代わりにタスクスケジューラを使用）。
