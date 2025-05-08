from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.settings import settings
from src.api.routes.router import api_router

app = FastAPI(
    title="Twitter App API",
    description="Twitter App API with FastAPI",
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では特定のオリジンのみ許可すること
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIルーターを登録
app.include_router(api_router, prefix=settings.API_PREFIX)

# ルートエンドポイント
@app.get("/")
def root():
    return {"message": "Welcome to Twitter Clone API"}

# アプリケーション起動時のイベント
@app.on_event("startup")
async def startup_event():
    # 起動時の処理があれば追加
    pass

# アプリケーション終了時のイベント
@app.on_event("shutdown")
async def shutdown_event():
    # 終了時の処理があれば追加
    pass

if __name__ == "__main__":
    import uvicorn
    # main.pyから直接起動する場合の設定
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
