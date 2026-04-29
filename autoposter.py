import os
import json
import openai
from requests_oauthlib import OAuth1Session

# --- 設定 ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
X_CONSUMER_KEY = os.getenv("X_CONSUMER_KEY")
X_CONSUMER_SECRET = os.getenv("X_CONSUMER_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

def generate_content():
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    prompt = """
あなたはhermes-agentというAI自動化・副業の専門家です。
以下の条件で、実用的で有益なtipsをX（旧Twitter）に投稿するテキストを作成してください。

テーマ：「hermes-agent × 自動化・副業」

条件：
- 読んだ人がすぐに使えるor試せる具体的なtipsにすること
- 「へー知らなかった」「これ使えそう」と思わせる内容にすること
- 毎回違うテーマ・切り口で作成すること（例：時間短縮術、収益化アイデア、ツール活用法、ワークフロー改善など）
- 文章はハッシュタグを含めて200〜230文字になるよう調整すること（短すぎず長すぎず）
- 絵文字を適度に使って視認性を上げること
- 以下の構成で改行を入れること：
  【構成】
  1行目：タイトル（絵文字＋キャッチーな一言）
  （空行）
  2〜4行目：本文（tips の内容を2〜3文で）
  （空行）
  最終行：ハッシュタグ2〜3個

出力は以下のJSON形式のみで返してください。改行は\nで表現してください。
{
  "x_post": "Xに投稿する文章（\nで改行を含む）"
}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)

def post_to_x(text):
    oauth = OAuth1Session(
        X_CONSUMER_KEY,
        client_secret=X_CONSUMER_SECRET,
        resource_owner_key=X_ACCESS_TOKEN,
        resource_owner_secret=X_ACCESS_TOKEN_SECRET,
    )

    payload = {"text": text}
    response = oauth.post("https://api.twitter.com/2/tweets", json=payload)

    if response.status_code != 201:
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")

    print("Successfully posted to X!")

if __name__ == "__main__":
    print("Generating content...")
    content = generate_content()

    print("Post:", content["x_post"])
    print("Posting to X...")
    post_to_x(content["x_post"])
