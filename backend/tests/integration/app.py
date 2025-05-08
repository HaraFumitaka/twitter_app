import sys
import os
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

# src パッケージをインポートできるようにパスを追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# テスト用の設定をインポート
from .database import get_test_db_session
from .config import test_settings

# 本番用のAPIルーターをインポート
from src.api.routes.router import api_router

# テスト用のDBセッション依存関係をオーバーライド
def override_get_db():
    with get_test_db_session() as session:
        yield session

# テスト用アプリケーションを作成
def create_test_app():
    app = FastAPI(
        title="Test Twitter Clone API",
        description="Test instance of Twitter Clone API",
    )
    
    # APIルーターを登録
    app.include_router(api_router, prefix=test_settings.API_PREFIX)
    
    # DBセッション依存関係をオーバーライド
    from src.database.session import get_db
    app.dependency_overrides[get_db] = override_get_db
    
    return app

# テスト用クライアントを作成
test_app = create_test_app()
test_client = TestClient(test_app)
