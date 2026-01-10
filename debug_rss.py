#!/usr/bin/env python3
"""
RSSフィードのデバッグスクリプト - 記事の日付を確認
"""

import feedparser
from datetime import datetime, timedelta

rss_feeds = [
    {
        "url": "https://xtech.nikkei.com/rss/xtech-it.rdf",
        "name": "日経クロステック",
    },
    {
        "url": "http://toyokeizai.net/list/feed/rss",
        "name": "東洋経済オンライン",
    },
    {
        "url": "https://diamond.jp/feed.xml",
        "name": "ダイヤモンド・オンライン",
    },
    {
        "url": "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml",
        "name": "ITmedia AI+",
    },
]

now = datetime.now()
print(f"現在時刻: {now}\n")

for feed_info in rss_feeds:
    feed_url = feed_info["url"]
    feed_name = feed_info["name"]

    print(f"=== {feed_name} ===")
    try:
        feed = feedparser.parse(feed_url)
        print(f"総記事数: {len(feed.entries)}件\n")

        if len(feed.entries) > 0:
            print("最新5件の記事と日付:")
            for i, entry in enumerate(feed.entries[:5], 1):
                title = entry.title

                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                    age = now - published
                    print(f"{i}. [{age}前] {title}")
                    print(f"   公開日時: {published}")
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6])
                    age = now - published
                    print(f"{i}. [{age}前] {title}")
                    print(f"   更新日時: {published}")
                else:
                    print(f"{i}. [日付不明] {title}")
                print()
        else:
            print("記事が取得できませんでした\n")

    except Exception as e:
        print(f"エラー: {e}\n")

    print()
