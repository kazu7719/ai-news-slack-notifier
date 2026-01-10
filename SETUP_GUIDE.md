# セットアップガイド

このガイドに従って、AIニュース通知システムを完成させましょう。

## 現在の状態

✅ Python仮想環境の作成完了
✅ 依存パッケージのインストール完了
✅ スクリプトファイルの作成完了
✅ 実行権限の設定完了
✅ .envファイルの作成完了

## 次に必要な手順

### ステップ1: Anthropic API Keyの取得

1. ブラウザで以下のURLを開く:
   ```
   https://console.anthropic.com/settings/keys
   ```

2. Anthropicアカウントでログイン（未登録の場合は新規登録）

3. 「Create Key」ボタンをクリック

4. キー名を入力（例: AI News Notifier）

5. 作成されたAPI Keyをコピー（`sk-ant-api03-...`で始まる文字列）

### ステップ2: LINE Notify Tokenの取得

1. ブラウザで以下のURLを開く:
   ```
   https://notify-bot.line.me/my/
   ```

2. LINEアカウントでログイン

3. 「トークンを発行する」をクリック

4. トークン名を入力（例: AIニュース通知）

5. 通知を送信するトークルームを選択
   - おすすめ: 「1:1でLINE Notifyから通知を受け取る」

6. 「発行する」をクリック

7. 表示されたトークンをコピー
   - ⚠️ **重要**: このトークンはこの画面でしか表示されません！必ずコピーしてください

### ステップ3: .envファイルに認証情報を設定

1. エディタで.envファイルを開く:
   ```bash
   cd /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier
   nano .env
   ```

   または

   ```bash
   open -e .env
   ```

2. 以下のように編集（取得したキーを貼り付け）:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   LINE_NOTIFY_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

3. 保存して閉じる
   - nanoの場合: `Ctrl+X` → `Y` → `Enter`
   - TextEditの場合: `Command+S` → ウィンドウを閉じる

### ステップ4: 動作テスト

1. スクリプトを実行:
   ```bash
   cd /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier
   source venv/bin/activate
   python main.py
   ```

2. 成功すると:
   - コンソールに「LINEへの投稿が完了しました」と表示される
   - LINEに通知が届く

3. エラーが出た場合:
   - 「エラー: ANTHROPIC_API_KEYが設定されていません」
     → .envファイルのAPI Keyを確認

   - 「エラー: LINE_NOTIFY_TOKENが設定されていません」
     → .envファイルのLINE Tokenを確認

   - 「LINE投稿エラー」
     → LINE Notify Tokenが正しいか確認

   - 「要約エラー」
     → Anthropic API Keyが正しいか確認

### ステップ5: 自動実行の設定（毎朝8時）

動作テストが成功したら、cronで自動実行を設定します。

1. crontabを編集:
   ```bash
   crontab -e
   ```

2. 以下の行を追加:
   ```
   0 8 * * * /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier/run_news_notifier.sh
   ```

3. 保存して閉じる
   - viエディタの場合: `i`キーで編集モード → 上記をペースト → `Esc` → `:wq` → `Enter`

4. 設定を確認:
   ```bash
   crontab -l
   ```

5. 手動でcron用スクリプトをテスト:
   ```bash
   /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier/run_news_notifier.sh
   ```

6. ログを確認:
   ```bash
   cat /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier/logs/cron.log
   ```

### ステップ6: macOSの権限設定（必要な場合）

macOS Catalina以降では、cronに権限を与える必要がある場合があります。

1. システム環境設定（システム設定） → セキュリティとプライバシー

2. 「プライバシー」タブ → 「フルディスクアクセス」

3. 鍵アイコンをクリックして変更を許可

4. 「+」ボタンをクリック

5. `Cmd+Shift+G`を押して、以下のパスを入力:
   ```
   /usr/sbin/cron
   ```

6. 「開く」をクリック

## カスタマイズ例

### 平日のみ実行したい場合

crontabを以下のように変更:
```
0 8 * * 1-5 /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier/run_news_notifier.sh
```

### 朝8時と夜8時の2回実行したい場合

```
0 8,20 * * * /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier/run_news_notifier.sh
```

### 取得する記事数を増やしたい場合

main.pyを編集（144行目付近）:
```python
articles = fetch_ai_news_from_rss(max_articles=5)  # 3 → 5に変更
```

## トラブルシューティング

### Q: cronが実行されない

A: 以下を確認してください:
1. crontabにパスが絶対パスで設定されているか
2. run_news_notifier.shに実行権限があるか（`ls -l`で確認）
3. ログファイルにエラーが出ていないか（`cat logs/cron.log`）
4. macOSの権限設定（ステップ6）

### Q: LINEに通知が届かない

A: 以下を確認してください:
1. LINE Notify Tokenが正しいか
2. 手動実行（`python main.py`）で成功するか
3. LINE Notify APIのレート制限（1時間1000回）に達していないか

### Q: 「新しいニュースが見つかりませんでした」と表示される

A: 以下の可能性があります:
1. 24時間以内に新しい記事がない（正常）
2. RSSフィードが取得できていない（インターネット接続を確認）

main.pyの対象期間を変更して試してみてください:
```python
if datetime.now() - published < timedelta(days=2):  # 1日 → 2日に変更
```

## 完了チェックリスト

- [ ] Anthropic API Keyを取得して.envに設定
- [ ] LINE Notify Tokenを取得して.envに設定
- [ ] `python main.py`で動作確認（LINEに通知が届く）
- [ ] crontabに設定を追加
- [ ] run_news_notifier.shで動作確認
- [ ] ログファイル（logs/cron.log）で正常に実行されているか確認

## サポート

詳細なドキュメント:
- README.md - 基本的な使い方
- CRON_SETUP.md - cron設定の詳細

すべてのステップが完了すれば、毎朝8時に自動的にLINEでAIニュースが届くようになります！
