from fastapi import APIRouter

from src.auth.router import router as auth_router
from src.tweets.router import router as tweets_router

# メインAPIルーターを作成
api_router = APIRouter()

# 各ルーターを登録
api_router.include_router(auth_router, prefix="/auth", tags=["認証"])
api_router.include_router(tweets_router, prefix="/tweets", tags=["ツイート"])
