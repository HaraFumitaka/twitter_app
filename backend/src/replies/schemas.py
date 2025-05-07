# src/replies/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# リプライ作成用スキーマ
class ReplyCreate(BaseModel):
    reply_content: str = Field(..., min_length=1, max_length=280)
    parent_reply_id: Optional[int] = None  # 親リプライID（ない場合はツイートに対する直接リプライ）

# リプライ基本情報スキーマ
class ReplyBase(BaseModel):
    reply_id: int
    user_id: str
    tweet_id: int
    parent_reply_id: Optional[int] = None
    reply_content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# リプライ詳細スキーマ（ユーザー名などの追加情報を含む）
class ReplyDetail(ReplyBase):
    user_name: str
    child_reply_count: int = 0

# リプライ一覧レスポンススキーマ
class ReplyList(BaseModel):
    replies: List[ReplyDetail]
    total: int
    page: int
    page_size: int

# リプライ操作結果レスポンス用スキーマ
class ReplyResponse(BaseModel):
    success: bool
    message: str
    reply_id: int
