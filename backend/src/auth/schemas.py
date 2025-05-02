# src/auth/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime

# ユーザー登録用スキーマ
class UserCreate(BaseModel):
    e_mail: EmailStr  # EmailStrを使用してバリデーション
    password: str = Field(..., min_length=8)  # 8文字以上のパスワード
    user_id: str = Field(..., min_length=3, max_length=50)
    user_name: str = Field(..., min_length=1, max_length=100)
    phone_number: Optional[str] = None
    self_introduction: Optional[str] = None
    place: Optional[str] = None
    birthday: Optional[date] = None
    profile_img: Optional[str] = None
    avatar_img: Optional[str] = None

# ログイン用スキーマ
class UserLogin(BaseModel):
    e_mail: EmailStr
    password: str

# セッション情報スキーマ (クッキー内に保存するデータ)
class SessionData(BaseModel):
    user_id: str  # セッションにはユーザーIDのみ保存

# ユーザー情報レスポンス用スキーマ (パスワードを除く)
class UserResponse(BaseModel):
    id: int
    e_mail: str
    user_id: str
    user_name: str
    phone_number: Optional[str] = None
    self_introduction: Optional[str] = None
    place: Optional[str] = None
    birthday: Optional[date] = None
    profile_img: Optional[str] = None
    avatar_img: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # ORMモデルからの変換を可能に
