from .app import test_client
import json

def register_user(user_data):
    """ユーザー登録を行う"""
    return test_client.post(
        "/api/auth/register",
        json=user_data
    )

def login_user(email, password):
    """ユーザーログインを行う"""
    return test_client.post(
        "/api/auth/login",
        json={
            "e_mail": email,
            "password": password
        }
    )

def get_auth_headers(cookies):
    """認証ヘッダーを取得"""
    return {"Cookie": f"session_id={cookies.get('session_id')}"}

def create_test_tweet(tweet_data, headers):
    """テストツイートを作成"""
    return test_client.post(
        "/api/tweets/",
        json=tweet_data,
        headers=headers
    )

def create_test_reply(tweet_id, reply_data, headers, parent_reply_id=None):
    """テストリプライを作成"""
    if parent_reply_id:
        reply_data["parent_reply_id"] = parent_reply_id
    
    return test_client.post(
        f"/api/tweets/{tweet_id}/replies",
        json=reply_data,
        headers=headers
    )

def assert_successful_response(response, status_code=200):
    """レスポンスが成功したことを検証"""
    assert response.status_code == status_code
    return response.json()
