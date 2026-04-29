import os
import json
import openai
from requests_oauthlib import OAuth1Session

# --- 設定 ---
# GitHubのSecretsから読み込みます
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
X_CONSUMER_KEY = os.getenv("X_CONSUMER_KEY")
X_CONSUMER_SECRET = os.getenv("X_CONSUMER_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

def generate_content():
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = """
    以下の条件で、AI副業をテーマにしたギャグ系のショートストーリーと、
    それを元にしたX投稿用のテキストを作成してください。

    1. 小説（300文字程度）: AIを使い始めて失敗するが、最後にクスッとするオチがある話。
    2. 漫画構成（4コマ分）: 小説を元にした各コマの描写。
    3. X投稿文: 読者の共感を呼び、noteへ誘導するような200文字程度の文章。
    
    出力は以下のJSON形式のみで返してください。
    {
        "story": "小説の内容",
        "storyboard": "4コマの構成内容",
        "x_post": "Xに投稿する文章（ハッシュタグ含む）"
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
    
    print("Story:", content["story"])
    print("Posting to X...")
    post_to_x(content["x_post"])
