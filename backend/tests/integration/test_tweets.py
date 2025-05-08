# tests/integration/test_tweets.py
import pytest
from .utils import (
    create_test_tweet, assert_successful_response,
    get_auth_headers
)

class TestTweets:
    """ツイート機能のテスト"""
    
    def test_create_tweet(self, auth_user, test_tweet_data, client):
        """ツイート作成のテスト"""
        response = create_test_tweet(test_tweet_data, auth_user["headers"])
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert data["tweet_content"] == test_tweet_data["tweet_content"]
        assert data["user_id"] == auth_user["user_data"]["user_id"]
        assert "tweet_id" in data
    
    def test_get_tweets(self, auth_user, test_tweet_data, client, create_tweet):
        """ツイート一覧取得のテスト"""
        # ツイート一覧を取得
        response = client.get(
            "/api/tweets/",
            headers=auth_user["headers"]
        )
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert "tweets" in data
        assert len(data["tweets"]) > 0
        assert data["tweets"][0]["tweet_content"] == test_tweet_data["tweet_content"]
        assert data["total"] > 0
    
    def test_get_tweet(self, auth_user, client, create_tweet):
        """特定ツイートの取得テスト"""
        # 特定のツイートを取得
        response = client.get(
            f"/api/tweets/{create_tweet}",
            headers=auth_user["headers"]
        )
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert data["tweet_id"] == create_tweet
        assert data["user_id"] == auth_user["user_data"]["user_id"]
    
    def test_delete_tweet(self, auth_user, client, create_tweet):
        """ツイート削除のテスト"""
        # ツイートを削除
        response = client.delete(
            f"/api/tweets/{create_tweet}",
            headers=auth_user["headers"]
        )
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert data["success"] is True
        assert data["message"] == "ツイートを削除しました"
        assert data["tweet_id"] == create_tweet
        
        # 削除後、ツイートが存在しないことを確認
        response = client.get(
            f"/api/tweets/{create_tweet}",
            headers=auth_user["headers"]
        )
        assert response.status_code == 404
    
    def test_like_tweet(self, auth_user, client, create_tweet):
        """いいね追加のテスト"""
        # いいねを追加
        response = client.post(
            f"/api/tweets/{create_tweet}/like",
            headers=auth_user["headers"]
        )
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert data["success"] is True
        assert data["message"] == "いいねしました"
        
        # ツイートを取得していいねされているか確認
        response = client.get(
            f"/api/tweets/{create_tweet}",
            headers=auth_user["headers"]
        )
        tweet_data = assert_successful_response(response)
        assert tweet_data["is_liked"] is True
        assert tweet_data["like_count"] == 1
    
    def test_unlike_tweet(self, auth_user, client, create_tweet):
        """いいね削除のテスト"""
        # いいねを追加
        client.post(
            f"/api/tweets/{create_tweet}/like",
            headers=auth_user["headers"]
        )
        
        # いいねを削除
        response = client.delete(
            f"/api/tweets/{create_tweet}/like",
            headers=auth_user["headers"]
        )
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert data["success"] is True
        assert data["message"] == "いいねを取り消しました"
        
        # ツイートを取得していいねが削除されているか確認
        response = client.get(
            f"/api/tweets/{create_tweet}",
            headers=auth_user["headers"]
        )
        tweet_data = assert_successful_response(response)
        assert tweet_data["is_liked"] is False
        assert tweet_data["like_count"] == 0
    
    def test_retweet(self, auth_user, client, create_tweet):
        """リツイート追加のテスト"""
        # リツイートを追加
        response = client.post(
            f"/api/tweets/{create_tweet}/retweet",
            headers=auth_user["headers"]
        )
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert data["success"] is True
        assert data["message"] == "リツイートしました"
        
        # ツイートを取得しリツイートされているか確認
        response = client.get(
            f"/api/tweets/{create_tweet}",
            headers=auth_user["headers"]
        )
        tweet_data = assert_successful_response(response)
        assert tweet_data["is_retweeted"] is True
        assert tweet_data["retweet_count"] == 1
    
    def test_bookmark(self, auth_user, client, create_tweet):
        """ブックマーク追加と削除のテスト"""
        # ブックマークを追加
        response = client.post(
            f"/api/tweets/{create_tweet}/bookmark",
            headers=auth_user["headers"]
        )
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert data["success"] is True
        assert data["message"] == "ブックマークしました"
        
        # ツイートを取得しブックマークされているか確認
        response = client.get(
            f"/api/tweets/{create_tweet}",
            headers=auth_user["headers"]
        )
        tweet_data = assert_successful_response(response)
        assert tweet_data["is_bookmarked"] is True
        
        # ブックマークを削除
        response = client.delete(
            f"/api/tweets/{create_tweet}/bookmark",
            headers=auth_user["headers"]
        )
        data = assert_successful_response(response)
        
        # レスポンスの検証
        assert data["success"] is True
        assert data["message"] == "ブックマークを取り消しました"
