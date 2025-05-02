from fastapi import APIRouter

from ...auth.router import router as auth_router

# メインAPIルーターを作成
api_router = APIRouter()

# 各ルーターを登録
api_router.include_router(auth_router, prefix="/auth", tags=["認証"])
