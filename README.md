# AI News LINE Notifier

AIに関する最新ニュースをRSSフィードから取得し、Claude APIで要約してLINEに通知するCLIツールです。

毎朝8時に自動実行して、最新のAIニュースを自動的にLINEで受け取ることができます。

## 機能

- TechCrunch AI、VentureBeat AIなどの公式RSSフィードからAIニュースを取得
- Claude APIを使用して各記事を2〜3行に自動要約
- LINEに整形されたメッセージとして投稿（記事名・引用元・要約・URL）
- 24時間以内の新しい記事のみを対象
- cronで自動実行設定可能（毎朝8時など）

## 必要なもの

- Python 3.8以上
- Anthropic API Key（Claude API用）
- LINE Notify Token

## セットアップ

### 1. ディレクトリへの移動

```bash
cd ai-news-slack-notifier
```

### 2. 仮想環境の作成と有効化

```bash
python3 -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

`.env.example`をコピーして`.env`ファイルを作成：

```bash
cp .env.example .env
```

`.env`ファイルを編集して、以下の値を設定：

```
ANTHROPIC_API_KEY=your_actual_api_key_here
LINE_NOTIFY_TOKEN=your_line_notify_token_here
```

#### API Key/Tokenの取得方法

**Anthropic API Key:**
1. [Anthropic Console](https://console.anthropic.com/settings/keys)にアクセス
2. APIキーを作成してコピー

**LINE Notify Token:**
1. [LINE Notify](https://notify-bot.line.me/my/)にアクセス
2. 「トークンを発行する」をクリック
3. トークン名を入力（例：AIニュース通知）
4. 通知を送信するトークルームを選択（「1:1でLINE Notifyから通知を受け取る」など）
5. 発行されたトークンをコピー（この画面でしか表示されないので注意！）

## 使い方

### 手動実行

```bash
python main.py
```

実行すると、以下の処理が行われます：

1. RSSフィードから24時間以内のAIニュースを取得（最大3件）
2. Claude APIで各記事を要約
3. LINEに通知を投稿

### 自動実行（毎朝8時に実行）

#### セットアップ手順

1. **crontabを編集**

```bash
crontab -e
```

2. **以下の行を追加**（パスは実際のプロジェクトパスに置き換えてください）

```
0 8 * * * /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier/run_news_notifier.sh
```

3. **保存して終了**

詳しい設定方法は [CRON_SETUP.md](CRON_SETUP.md) を参照してください。

#### 平日のみ実行したい場合

```
0 8 * * 1-5 /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier/run_news_notifier.sh
```

#### 朝8時と夜8時の2回実行したい場合

```
0 8,20 * * * /Users/yoshida_antlerspirits/projects/ai-news-slack-notifier/run_news_notifier.sh
```

#### 実行ログの確認

```bash
tail -f logs/cron.log
```

## 出力例

LINEには以下のような形式で投稿されます：

```
【AIニュース 2026-01-09】
==============================

■ 記事タイトル

要約内容が2〜3行で表示されます。
AIに関する重要なポイントが簡潔にまとめられています。

引用元: TechCrunch
https://techcrunch.com/article/...

------------------------------

■ 次の記事タイトル

...
```

## カスタマイズ

### 取得する記事数を変更

`main.py`の該当行を編集：

```python
articles = fetch_ai_news_from_rss(max_articles=5)  # 3 → 5に変更
```

### RSSフィードを追加

`main.py`の該当行を編集：

```python
rss_feeds = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "追加のRSSフィードURL",
]
```

### 対象期間を変更

`main.py`の該当行を編集：

```python
if datetime.now() - published < timedelta(days=2):  # 1日 → 2日に変更
```

### 実行時刻を変更

crontabを編集：

```bash
crontab -e
```

```
# 毎朝7時に変更
0 7 * * * /path/to/run_news_notifier.sh

# 毎日正午に変更
0 12 * * * /path/to/run_news_notifier.sh
```

## トラブルシューティング

### 環境変数が読み込まれない

- `.env`ファイルがプロジェクトルートにあることを確認
- 環境変数の名前が正しいか確認（`LINE_NOTIFY_TOKEN`）

### RSS取得エラー

- インターネット接続を確認
- RSSフィードのURLが有効か確認

### LINE投稿エラー

- LINE Notify Tokenが正しいか確認
- トークンが有効期限内か確認
- LINE Notify APIの制限に引っかかっていないか確認

### cronが実行されない

- パスが絶対パスになっているか確認
- `run_news_notifier.sh`に実行権限があるか確認（`chmod +x`）
- ログを確認（`cat logs/cron.log`）
- 手動実行でテスト（`./run_news_notifier.sh`）

詳しくは [CRON_SETUP.md](CRON_SETUP.md) を参照してください。

## ファイル構成

```
ai-news-slack-notifier/
├── main.py                  # メインスクリプト
├── run_news_notifier.sh     # cron実行用ラッパースクリプト
├── requirements.txt         # 依存パッケージ
├── .env                     # 環境変数（要設定）
├── .env.example             # 環境変数のサンプル
├── .gitignore              # Git除外設定
├── README.md               # このファイル
├── CRON_SETUP.md           # cron設定詳細ガイド
├── venv/                   # Python仮想環境
└── logs/                   # 実行ログ
    └── cron.log            # cronの実行ログ
```

## ライセンス

MIT

## 注意事項

- このツールはRSSフィードの公式APIのみを使用しており、スクレイピングは行いません
- Claude APIの利用料金が発生します（1回の実行で数円程度）
- LINE Notify APIには[レート制限](https://notify-bot.line.me/doc/ja/)があります（1時間に1000回まで）
- 個人利用を想定しています

## 今後の改善案

- [ ] 記事の重複チェック機能
- [ ] より多くのRSSフィード対応
- [ ] カテゴリ別のフィルタリング
- [ ] 既読管理機能
- [ ] Docker対応
