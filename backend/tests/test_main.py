import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_root():
    """ルートエンドポイントのテスト"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_read_item():
    """item_idパラメータを使用したエンドポイントのテスト"""
    item_id = 123
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json() == {"item_id": item_id, "q": None}

def test_read_item_with_query():
    """item_idとクエリパラメータqを使用したエンドポイントのテスト"""
    item_id = 123
    q = "test-query"
    response = client.get(f"/items/{item_id}?q={q}")
    assert response.status_code == 200
    assert response.json() == {"item_id": item_id, "q": q}

def test_read_item_invalid_id():
    """無効なitem_idでの動作確認テスト"""
    response = client.get("/items/invalid")
    assert response.status_code == 422  # FastAPIのバリデーションエラー
