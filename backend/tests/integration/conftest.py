import pytest
from .database import setup_test_db, teardown_test_db, reset_test_db, get_test_db_session
from .app import test_client
from src.auth.utils import get_password_hash

import sys
import os
from pathlib import Path

# プロジェクトルートディレクトリをPythonパスに追加
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))


# テスト開始前にデータベースをセットアップ
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    setup_test_db()
    yield
    teardown_test_db()

# 各テスト前にデータベースをリセット
@pytest.fixture(autouse=True)
def reset_db():
    reset_test_db()

# テストクライアントのフィクスチャ
@pytest.fixture
def client():
    return test_client

# テストユーザーデータ
@pytest.fixture
def test_user_data():
    return {
        "e_mail": "test@example.com",
        "password": "password123",
        "user_id": "testuser",
        "user_name": "Test User"
    }

# テストユーザーをDBに作成し、認証情報を返すフィクスチャ
@pytest.fixture
def auth_user(test_user_data):
    # テストユーザーをDBに作成
    from src.models.user import User
    
    with get_test_db_session() as db:
        hashed_password = get_password_hash(test_user_data["password"])
        db_user = User(
            e_mail=test_user_data["e_mail"],
            password=hashed_password,
            user_id=test_user_data["user_id"],
            user_name=test_user_data["user_name"]
        )
        db.add(db_user)
        db.commit()
    
    # クライアントでログイン
    response = test_client.post(
        "/api/auth/login",
        json={
            "e_mail": test_user_data["e_mail"],
            "password": test_user_data["password"]
        }
    )
    
    # クッキーを含むクライアントセッション情報を返す
    cookies = response.cookies
    headers = {"Cookie": f"session_id={cookies.get('session_id')}"}
    
    return {
        "user_data": test_user_data,
        "headers": headers,
        "cookies": cookies
    }

# テストツイートデータ
@pytest.fixture
def test_tweet_data():
    return {
        "tweet_content": "これはテスト用のツイートです。"
    }

# テストリプライデータ
@pytest.fixture
def test_reply_data():
    return {
        "reply_content": "これはテスト用のリプライです。"
    }

# テストツイートをDBに作成し、IDを返すフィクスチャ
@pytest.fixture
def create_tweet(auth_user, test_tweet_data):
    response = test_client.post(
        "/api/tweets/",
        json=test_tweet_data,
        headers=auth_user["headers"]
    )
    
    assert response.status_code == 200
    tweet_id = response.json()["tweet_id"]
    
    return tweet_id
