from src.config.settings import Settings

class TestSettings(Settings):
    # テスト用データベース設定
    DB_HOST: str = "twitter-test-db"  # Dockerコンテナ名
    DB_PORT: int = 3306  # テスト用ポート
    DB_USER: str = "test_user"
    DB_PASSWORD: str = "test_password"
    DB_NAME: str = "test_app_db"
    
    # セッション設定
    SECRET_KEY: str = "test-secret-key"  # 本番環境では安全な値に変更すること
    SESSION_COOKIE_NAME: str = "session_id"  # クッキー名
    SESSION_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 7日間(セッション有効期間)

    # テスト用API設定
    API_PREFIX: str = "/api"

test_settings = TestSettings()
