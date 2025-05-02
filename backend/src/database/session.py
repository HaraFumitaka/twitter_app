from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config.settings import settings

# MySQLデータベース接続URL
DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# SQLAlchemyエンジンとセッションの作成
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# DBセッションの依存関係（FastAPIのDependsで使用）
def get_db():
    db = SessionLocal()
    try:
        yield db  # リクエスト処理中はセッションを維持
    finally:
        db.close()  # リクエスト完了後にセッションを閉じる
