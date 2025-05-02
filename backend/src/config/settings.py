from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # データベース設定
    DB_HOST: str = "twitter-db"  # Dockerコンテナ名
    DB_PORT: int = 3306
    DB_USER: str = "my_app_user"
    DB_PASSWORD: str = "your_password"
    DB_NAME: str = "my_app_db"
    
    # セッション設定
    SECRET_KEY: str = "your-secret-key-for-session-encryption"  # 本番環境では安全な値に変更すること
    SESSION_COOKIE_NAME: str = "session_id"  # クッキー名
    SESSION_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 7日間(セッション有効期間)
    
    # FastAPI設定
    API_PREFIX: str = "/api"
    
    class Config:
        env_file = ".env"  # 環境変数ファイルからも読み込み可能

settings = Settings()
