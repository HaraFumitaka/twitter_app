import contextlib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

from .config import test_settings
from src.models.user import User
from src.models.tweet import Tweet
from src.models.interactions import Like, Retweet, Bookmark
from src.models.reply import Reply

# テスト用データベース接続URL
TEST_DATABASE_URL = f"mysql+pymysql://{test_settings.DB_USER}:{test_settings.DB_PASSWORD}@{test_settings.DB_HOST}:{test_settings.DB_PORT}/{test_settings.DB_NAME}"

# テスト用エンジンとセッション
test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base = declarative_base()

# テスト用データベースのセットアップ関数
def setup_test_db():
    """テスト用データベースをセットアップ"""
    # データベースが存在しない場合は作成
    if not database_exists(test_engine.url):
        create_database(test_engine.url)
    
    # 全てのテーブルを作成
    Base.metadata.create_all(bind=test_engine)

# テスト用データベースのクリーンアップ関数
def teardown_test_db():
    """テスト用データベースをクリーンアップ"""
    # すべてのテーブルをドロップ
    Base.metadata.drop_all(bind=test_engine)

# データベースをリセットする関数
def reset_test_db():
    """テスト用データベースをリセット"""
    teardown_test_db()
    setup_test_db()

# テスト用DBセッションを提供するコンテキストマネージャ
@contextlib.contextmanager
def get_test_db_session():
    """テスト用DBセッションを取得"""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
