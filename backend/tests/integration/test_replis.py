import pytest
from .utils import (
    create_test_reply, assert_successful_response
)

class TestReplies:
    """リプライ機能のテスト"""
    
    def test_create_reply(self, auth_user, test_reply_data, client, create_tweet):
        """リプライ作成のテスト"""
        response = create_test_reply(create_tweet, test_reply_data, auth_user["headers"])
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert data["reply_content"] == test_reply_data["reply_content"]
        assert data["user_id"] == auth_user["user_data"]["user_id"]
        assert data["tweet_id"] == create_tweet
        assert "reply_id" in data
    
    def test_get_tweet_replies(self, auth_user, test_reply_data, client, create_tweet):
        """ツイートのリプライ一覧取得のテスト"""
        # リプライを作成
        create_test_reply(create_tweet, test_reply_data, auth_user["headers"])
        
        # リプライ一覧を取得
        response = client.get(
            f"/api/tweets/{create_tweet}/replies",
            headers=auth_user["headers"]
        )
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert "replies" in data
        assert len(data["replies"]) > 0
        assert data["replies"][0]["reply_content"] == test_reply_data["reply_content"]
        assert data["total"] > 0
    
    def test_get_reply(self, auth_user, test_reply_data, client, create_tweet):
        """特定リプライの取得テスト"""
        # リプライを作成
        response = create_test_reply(create_tweet, test_reply_data, auth_user["headers"])
        reply_data = assert_successful_response(response)
        reply_id = reply_data["reply_id"]
        
        # 特定のリプライを取得
        response = client.get(
            f"/api/replies/{reply_id}",
            headers=auth_user["headers"]
        )
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert data["reply_id"] == reply_id
        assert data["user_id"] == auth_user["user_data"]["user_id"]
        assert data["tweet_id"] == create_tweet
    
    def test_nested_replies(self, auth_user, test_reply_data, client, create_tweet):
        """ネストされたリプライのテスト"""
        # 親リプライを作成
        response = create_test_reply(create_tweet, test_reply_data, auth_user["headers"])
        parent_reply = assert_successful_response(response)
        parent_reply_id = parent_reply["reply_id"]
        
        # 子リプライを作成
        child_reply_data = {
            "reply_content": "これは子リプライのテストです。",
            "parent_reply_id": parent_reply_id
        }
        response = client.post(
            f"/api/tweets/{create_tweet}/replies",
            json=child_reply_data,
            headers=auth_user["headers"]
        )
        child_reply = assert_successful_response(response)
        
        # 親リプライに対するリプライ一覧を取得
        response = client.get(
            f"/api/tweets/{create_tweet}/replies?parent_reply_id={parent_reply_id}",
            headers=auth_user["headers"]
        )
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert "replies" in data
        assert len(data["replies"]) > 0
        assert data["replies"][0]["reply_content"] == child_reply_data["reply_content"]
        assert data["replies"][0]["parent_reply_id"] == parent_reply_id
    
    def test_delete_reply(self, auth_user, test_reply_data, client, create_tweet):
        """リプライ削除のテスト"""
        # リプライを作成
        response = create_test_reply(create_tweet, test_reply_data, auth_user["headers"])
        reply_data = assert_successful_response(response)
        reply_id = reply_data["reply_id"]
        
        # リプライを削除
        response = client.delete(
            f"/api/replies/{reply_id}",
            headers=auth_user["headers"]
        )
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert data["success"] is True
        assert data["message"] == "リプライを削除しました"
        assert data["reply_id"] == reply_id
        
        # 削除後、リプライが存在しないことを確認
        response = client.get(
            f"/api/replies/{reply_id}",
            headers=auth_user["headers"]
        )
        assert response.status_code == 404
