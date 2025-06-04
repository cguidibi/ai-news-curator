import requests
import os

site_url = os.getenv("WP_SITE_URL")
username = os.getenv("WP_USERNAME")
password = os.getenv("WP_PASSWORD")

print(f"🔐 Authenticating to {site_url} as {username}...")

try:
    auth_response = requests.post(
        f"{site_url}/wp-json/jwt-auth/v1/token",
        data={"username": username, "password": password}
    )

    print(f"🔄 Auth response status: {auth_response.status_code}")
    print(f"📦 Raw auth response: {auth_response.text}")

    if auth_response.status_code != 200:
        print("❌ Authentication failed")
        exit(1)

    token = auth_response.json().get("token")
    print("✅ Auth successful.")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    post_data = {
        "title": "🧠 Top AI News – Auto Summary",
        "content": """
            <p>Here are today’s top AI stories:</p>
            <ul>
              <li><a href="https://example.com/news1">AI beats humans at strategy game</a></li>
              <li><a href="https://example.com/news2">Regulators examine AI ethics</a></li>
            </ul>
        """,
        "status": "publish"
    }

    print("📝 Sending post to WordPress...")
    post_response = requests.post(
        f"{site_url}/wp-json/wp/v2/posts",
        headers=headers,
        json=post_data
    )

    print(f"🟦 Post response status: {post_response.status_code}")
    print(f"📦 Post response: {post_response.text}")

    if post_response.status_code == 201:
        print("✅ Post published:", post_response.json().get("link"))
    else:
        print("❌ Post failed to publish")

except Exception as e:
    print("🔥 Script crashed with exception:")
    print(str(e))
