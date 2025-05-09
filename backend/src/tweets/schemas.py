# src/tweets/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ツイート作成用スキーマ
class TweetCreate(BaseModel):
    tweet_content: str = Field(..., min_length=1, max_length=280)  # 最大280文字に制限

# ツイート基本情報レスポンス用スキーマ
class TweetBase(BaseModel):
    tweet_id: int
    user_id: str
    tweet_content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# いいね数、リツイート数、ブックマーク数などを含むツイート詳細スキーマ
class TweetDetail(TweetBase):
    user_name: str  # ユーザー名を含める
    like_count: int = 0
    retweet_count: int = 0
    bookmark_count: int = 0
    is_liked: bool = False  # 現在のユーザーがいいねしているか
    is_retweeted: bool = False  # 現在のユーザーがリツイートしているか
    is_bookmarked: bool = False  # 現在のユーザーがブックマークしているか

# ツイート一覧レスポンス用スキーマ
class TweetList(BaseModel):
    tweets: List[TweetDetail]
    total: int
    page: int
    page_size: int
    
# インタラクション結果レスポンス用スキーマ
class InteractionResponse(BaseModel):
    success: bool
    message: str
    tweet_id: int
