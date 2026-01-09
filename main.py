#!/usr/bin/env python3
"""
AIニュースをRSSから取得してSlackに通知するスクリプト
"""

import os
import feedparser
import anthropic
import requests
from datetime import datetime, timedelta
from typing import List, Dict


def fetch_ai_news_from_rss(max_articles: int = 5) -> List[Dict]:
    """
    RSSフィードからAI関連のニュースを取得
    """
    # AI関連のRSSフィード（公式フィード）
    rss_feeds = [
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        "https://venturebeat.com/category/ai/feed/",
    ]

    articles = []

    for feed_url in rss_feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:max_articles]:
                # 24時間以内の記事のみ取得
                published = datetime(*entry.published_parsed[:6])
                if datetime.now() - published < timedelta(days=1):
                    articles.append({
                        'title': entry.title,
                        'url': entry.link,
                        'source': feed.feed.title if hasattr(feed.feed, 'title') else feed_url,
                        'summary': entry.summary if hasattr(entry, 'summary') else '',
                        'published': published
                    })
        except Exception as e:
            print(f"RSS取得エラー ({feed_url}): {e}")

    # 公開日時でソート（新しい順）
    articles.sort(key=lambda x: x['published'], reverse=True)
    return articles[:max_articles]


def summarize_article(article: Dict, api_key: str) -> str:
    """
    Claude APIを使って記事を2〜3行に要約
    """
    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""以下のニュース記事を2〜3行で簡潔に要約してください。

タイトル: {article['title']}
本文抜粋: {article['summary'][:500]}

日本語で、要点を押さえた要約をお願いします。"""

    try:
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=200,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"要約エラー: {e}")
        return "要約を生成できませんでした。"


def post_to_slack(webhook_url: str, articles: List[Dict], summaries: List[str]):
    """
    Slack Webhookに記事を投稿
    """
    if not articles:
        print("投稿する記事がありません")
        return

    # メッセージを構築
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"AIニュース ({datetime.now().strftime('%Y-%m-%d')})"
            }
        },
        {
            "type": "divider"
        }
    ]

    for article, summary in zip(articles, summaries):
        blocks.extend([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{article['title']}*\n\n{summary}\n\n引用元: {article['source']}\n<{article['url']}|記事を読む>"
                }
            },
            {
                "type": "divider"
            }
        ])

    payload = {
        "blocks": blocks
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Slackへの投稿が完了しました")
    except Exception as e:
        print(f"Slack投稿エラー: {e}")


def main():
    """
    メイン処理
    """
    # 環境変数から設定を読み込み
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    if not anthropic_api_key:
        print("エラー: ANTHROPIC_API_KEYが設定されていません")
        return

    if not slack_webhook_url:
        print("エラー: SLACK_WEBHOOK_URLが設定されていません")
        return

    print("AIニュースを取得中...")
    articles = fetch_ai_news_from_rss(max_articles=3)

    if not articles:
        print("新しいニュースが見つかりませんでした")
        return

    print(f"{len(articles)}件の記事を取得しました")

    print("記事を要約中...")
    summaries = []
    for i, article in enumerate(articles, 1):
        print(f"  {i}/{len(articles)}: {article['title']}")
        summary = summarize_article(article, anthropic_api_key)
        summaries.append(summary)

    print("Slackに投稿中...")
    post_to_slack(slack_webhook_url, articles, summaries)

    print("完了しました")


if __name__ == "__main__":
    main()
