import pytest
from .utils import register_user, login_user, get_auth_headers, assert_successful_response

class TestAuth:
    """認証機能のテスト"""
    
    def test_register_user(self, test_user_data, client):
        """ユーザー登録のテスト"""
        # 新しいユーザーデータ
        new_user = {
            "e_mail": "newuser@example.com",
            "password": "newpassword123",
            "user_id": "newuser",
            "user_name": "New User"
        }
        
        # ユーザー登録
        response = register_user(new_user)
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert data["e_mail"] == new_user["e_mail"]
        assert data["user_id"] == new_user["user_id"]
        assert data["user_name"] == new_user["user_name"]
        assert "password" not in data  # パスワードは返されない
    
    def test_login_user(self, test_user_data, client):
        """ユーザーログインのテスト"""
        # ユーザー登録
        register_user(test_user_data)
        
        # ログイン
        response = login_user(test_user_data["e_mail"], test_user_data["password"])
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert data["message"] == "ログインに成功しました"
        assert "session_id" in response.cookies  # セッションクッキーが設定されている
    
    def test_get_current_user(self, auth_user, client):
        """現在のユーザー情報取得のテスト"""
        # 現在のユーザー情報を取得
        response = client.get(
            "/api/auth/me",
            headers=auth_user["headers"]
        )
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert data["e_mail"] == auth_user["user_data"]["e_mail"]
        assert data["user_id"] == auth_user["user_data"]["user_id"]
        assert data["user_name"] == auth_user["user_data"]["user_name"]
    
    def test_logout(self, auth_user, client):
        """ログアウトのテスト"""
        # ログアウト
        response = client.post(
            "/api/auth/logout",
            headers=auth_user["headers"]
        )
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert data["message"] == "ログアウトしました"
        
        # ログアウト後はユーザー情報が取得できないことを確認
        response = client.get(
            "/api/auth/me",
            headers=auth_user["headers"]
        )
        assert response.status_code == 401  # 認証エラー
