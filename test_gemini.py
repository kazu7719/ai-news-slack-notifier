#!/usr/bin/env python3
"""
Gemini APIのテストスクリプト - 利用可能なモデルを確認
"""

import os
from google import genai
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    print("エラー: GEMINI_API_KEYが設定されていません")
    exit(1)

print(f"API Key: {gemini_api_key[:20]}...")
print("\n利用可能なモデルを確認中...\n")

try:
    # クライアントを作成
    client = genai.Client(api_key=gemini_api_key)

    # モデル一覧を取得
    models = client.models.list()

    print("=== 利用可能なモデル ===")
    for model in models:
        print(f"- {model.name}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"  サポートメソッド: {model.supported_generation_methods}")

    print("\n=== テスト: 簡単な生成 ===")
    # テキスト生成に適したモデルでテスト
    test_model = "models/gemini-2.5-flash"
    print(f"テストモデル: {test_model}")

    response = client.models.generate_content(
        model=test_model,
        contents="こんにちは、と日本語で返してください"
    )
    print(f"レスポンス: {response.text}")

except Exception as e:
    print(f"\nエラー: {e}")
    print("\nAPI Keyが無効か、Gemini APIが有効になっていない可能性があります。")
    print("\n確認事項:")
    print("1. Google AI Studio (https://aistudio.google.com/) にアクセス")
    print("2. APIキーが正しく表示されるか確認")
    print("3. 必要に応じてAPIキーを再生成")
