#!/usr/bin/env python3
"""
日本の主要メディアからAIニュースをRSSで取得してDiscordに通知するスクリプト（Gemini API版）
対象メディア: 日経クロステック、東洋経済オンライン、ダイヤモンド・オンライン、ITmedia AI+
"""

import os
import re
import time
import feedparser
import requests
from google import genai
from datetime import datetime, timedelta
from typing import List, Dict
from dotenv import load_dotenv


def fetch_ai_news_from_rss() -> List[Dict]:
    """
    RSSフィードからAI関連のニュースを取得（36時間以内の記事を全て取得）
    """
    # 日本の主要メディアのRSSフィード
    rss_feeds = [
        {
            "url": "https://xtech.nikkei.com/rss/xtech-it.rdf",
            "name": "日経クロステック",
            "keywords": [
                # AI関連キーワード（基本）
                "AI", "ai", "Ai", "人工知能", "エーアイ",
                # 機械学習関連
                "機械学習", "マシンラーニング", "ML", "ディープラーニング", "深層学習",
                # 生成AI関連
                "生成AI", "生成ＡＩ", "ジェネレーティブAI", "ChatGPT", "GPT", "Claude",
                "Gemini", "Copilot", "Bard",
                # モデル・技術
                "LLM", "大規模言語モデル", "言語モデル", "Transformer", "ニューラルネット",
                # 画像・動画AI
                "画像生成", "Stable Diffusion", "Midjourney", "DALL-E", "Sora",
                # 企業・サービス
                "OpenAI", "Google AI", "Microsoft AI", "Meta AI", "Anthropic",
                # ビジネス活用
                "AI活用", "AI導入", "AIツール", "AIサービス", "AI搭載", "AI技術",
                # その他
                "ロボット", "自動運転", "音声認識", "自然言語処理", "NLP", "画像認識"
            ]
        },
        {
            "url": "http://toyokeizai.net/list/feed/rss",
            "name": "東洋経済オンライン",
            "keywords": [
                "AI", "ai", "Ai", "人工知能", "エーアイ",
                "機械学習", "マシンラーニング", "ML", "ディープラーニング", "深層学習",
                "生成AI", "生成ＡＩ", "ジェネレーティブAI", "ChatGPT", "GPT", "Claude",
                "Gemini", "Copilot", "Bard",
                "LLM", "大規模言語モデル", "言語モデル", "Transformer", "ニューラルネット",
                "画像生成", "Stable Diffusion", "Midjourney", "DALL-E", "Sora",
                "OpenAI", "Google AI", "Microsoft AI", "Meta AI", "Anthropic",
                "AI活用", "AI導入", "AIツール", "AIサービス", "AI搭載", "AI技術",
                "ロボット", "自動運転", "音声認識", "自然言語処理", "NLP", "画像認識"
            ]
        },
        {
            "url": "https://diamond.jp/feed.xml",
            "name": "ダイヤモンド・オンライン",
            "keywords": [
                "AI", "ai", "Ai", "人工知能", "エーアイ",
                "機械学習", "マシンラーニング", "ML", "ディープラーニング", "深層学習",
                "生成AI", "生成ＡＩ", "ジェネレーティブAI", "ChatGPT", "GPT", "Claude",
                "Gemini", "Copilot", "Bard",
                "LLM", "大規模言語モデル", "言語モデル", "Transformer", "ニューラルネット",
                "画像生成", "Stable Diffusion", "Midjourney", "DALL-E", "Sora",
                "OpenAI", "Google AI", "Microsoft AI", "Meta AI", "Anthropic",
                "AI活用", "AI導入", "AIツール", "AIサービス", "AI搭載", "AI技術",
                "ロボット", "自動運転", "音声認識", "自然言語処理", "NLP", "画像認識"
            ]
        },
        {
            "url": "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml",
            "name": "ITmedia AI+",
            "keywords": []  # AI専用フィードなのでキーワードフィルタ不要
        },
    ]

    articles = []

    for feed_info in rss_feeds:
        feed_url = feed_info["url"]
        feed_name = feed_info["name"]
        keywords = feed_info["keywords"]

        try:
            print(f"  {feed_name} を取得中...")
            feed = feedparser.parse(feed_url)
            print(f"    総記事数: {len(feed.entries)}件")

            feed_articles_count = 0
            for entry in feed.entries:
                # 36時間以内の記事のみ取得
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6])
                else:
                    continue  # 日付情報がない場合はスキップ

                if datetime.now() - published > timedelta(hours=36):
                    continue  # 36時間より古い記事はスキップ

                # キーワードフィルタ（キーワードリストが空の場合は全件取得）
                if keywords:
                    title = entry.title
                    summary = entry.summary if hasattr(entry, 'summary') else ''
                    text = f"{title} {summary}".lower()  # 小文字に変換して検索しやすく

                    # いずれかのキーワードが含まれているかチェック（大文字小文字を区別しない）
                    if not any(keyword.lower() in text for keyword in keywords):
                        continue  # AI関連でない記事はスキップ

                articles.append({
                    'title': entry.title,
                    'url': entry.link,
                    'source': feed_name,
                    'summary': entry.summary if hasattr(entry, 'summary') else '',
                    'published': published,
                    'is_japanese': True  # 日本語記事フラグ
                })
                feed_articles_count += 1

            print(f"    → {feed_name}から{feed_articles_count}件のAI関連記事を取得")
        except Exception as e:
            print(f"RSS取得エラー ({feed_name}): {e}")

    # 公開日時でソート（新しい順）
    articles.sort(key=lambda x: x['published'], reverse=True)

    # 最新10件のみに制限（Gemini API無料プランは1日20リクエストまで）
    return articles[:10]


def summarize_with_gemini(article: Dict, client, model_name: str) -> Dict[str, str]:
    """
    Gemini APIを使って記事を要約（日本語記事用）
    """
    summary = article.get('summary', '')
    title = article.get('title', '')

    # HTMLタグを除去
    summary = re.sub('<[^>]+>', '', summary)

    # HTML特殊文字をデコード
    summary = summary.replace('&nbsp;', ' ')
    summary = summary.replace('&amp;', '&')
    summary = summary.replace('&lt;', '<')
    summary = summary.replace('&gt;', '>')
    summary = summary.replace('&quot;', '"')
    summary = summary.replace('&#39;', "'")

    # 余分な空白を削除
    summary = re.sub(r'\s+', ' ', summary).strip()

    # 要約がない場合
    if not summary:
        return {
            "title": title,
            "summary": "要約なし"
        }

    # Gemini APIで要約を生成（日本語記事なので翻訳不要）
    try:
        prompt = f"""以下のニュース記事を2〜3行に要約してください。要点を押さえた簡潔な要約をお願いします。

タイトル: {title}
本文: {summary[:1500]}

要約のみを返してください。"""

        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )

        return {
            "title": title,  # 日本語記事なのでタイトルはそのまま
            "summary": response.text.strip()
        }
    except Exception as e:
        print(f"要約エラー: {e}")
        return {
            "title": title,
            "summary": "要約を生成できませんでした。"
        }


def post_to_discord(webhook_url: str, articles: List[Dict], results: List[Dict]):
    """
    Discord Webhookに記事を投稿（Discordの制限に合わせて10件ずつ分割）
    """
    if not articles:
        print("投稿する記事がありません")
        return

    # Discordの埋め込みメッセージを構築
    all_embeds = []

    for article, result in zip(articles, results):
        embed = {
            "title": result['title'][:256],  # Discordのタイトル文字数制限
            "description": result['summary'][:4096],  # Discordの説明文字数制限
            "url": article['url'],
            "color": 3447003,  # 青色
            "fields": [
                {
                    "name": "引用元",
                    "value": article['source'],
                    "inline": True
                }
            ],
            "timestamp": article['published'].isoformat()
        }
        all_embeds.append(embed)

    # Discordは1メッセージに最大10個のembedsまでなので、10件ずつ分割して投稿
    max_embeds_per_message = 10
    total_messages = (len(all_embeds) + max_embeds_per_message - 1) // max_embeds_per_message

    for i in range(0, len(all_embeds), max_embeds_per_message):
        batch_embeds = all_embeds[i:i + max_embeds_per_message]
        message_num = (i // max_embeds_per_message) + 1

        # 最初のメッセージだけヘッダーをつける
        if i == 0:
            content = f"**AIニュース {datetime.now().strftime('%Y-%m-%d')}** ({len(articles)}件)"
        else:
            content = f"**AIニュース 続き ({message_num}/{total_messages})**"

        payload = {
            "content": content,
            "embeds": batch_embeds
        }

        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            print(f"  メッセージ {message_num}/{total_messages} を投稿しました")

            # Discord APIのレート制限を避けるため、次のメッセージまで1秒待つ
            if i + max_embeds_per_message < len(all_embeds):
                time.sleep(1)
        except Exception as e:
            print(f"Discord投稿エラー (メッセージ {message_num}): {e}")

    print("Discordへの投稿が完了しました")


def main():
    """
    メイン処理
    """
    # .envファイルから環境変数を読み込み
    load_dotenv()

    # 環境変数から設定を読み込み
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not gemini_api_key:
        print("エラー: GEMINI_API_KEYが設定されていません")
        return

    if not discord_webhook_url:
        print("エラー: DISCORD_WEBHOOK_URLが設定されていません")
        return

    # Gemini APIクライアントを作成
    client = genai.Client(api_key=gemini_api_key)
    model = 'models/gemini-2.5-flash'

    print("AIニュースを取得中...")
    articles = fetch_ai_news_from_rss()

    if not articles:
        print("新しいニュースが見つかりませんでした")
        # 記事がない場合でもDiscordに通知
        print("Discordに「ニュースなし」を投稿中...")
        payload = {
            "content": f"**AIニュース {datetime.now().strftime('%Y-%m-%d')}**\n\n今日は新しいAI関連ニュースがありませんでした。"
        }
        try:
            response = requests.post(discord_webhook_url, json=payload)
            response.raise_for_status()
            print("投稿完了")
        except Exception as e:
            print(f"Discord投稿エラー: {e}")
        return

    print(f"{len(articles)}件の記事を取得しました")

    print("Gemini APIで記事を要約中...")
    print("（Gemini API無料プランのレート制限に対応するため、各要約間に待機時間が入ります）")
    results = []

    # Gemini API無料プランのレート制限: 1分あたり5リクエストまで
    # 安全のため、各リクエスト間に13秒待つ（60秒 / 5リクエスト = 12秒 + バッファ1秒）
    rate_limit_delay = 13

    for i, article in enumerate(articles, 1):
        print(f"  {i}/{len(articles)}: {article['title']}")

        result = summarize_with_gemini(article, client, model)
        results.append(result)

        # 最後の記事以外は待機時間を入れる
        if i < len(articles):
            # 5件ごとに60秒待つ（1分あたり5リクエストの制限に対応）
            if i % 5 == 0:
                print(f"    ⏳ レート制限のため60秒待機中... (次: {i+1}/{len(articles)})")
                time.sleep(60)
            else:
                time.sleep(1)  # API負荷軽減のため短い待機

    print("Discordに投稿中...")
    post_to_discord(discord_webhook_url, articles, results)

    print("完了しました")


if __name__ == "__main__":
    main()
