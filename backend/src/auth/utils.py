from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Request, Response
from uuid import uuid4
from datetime import datetime, timedelta
from typing import Optional
import json

from src.config.settings import settings
from src.auth.schemas import SessionData

# パスワードハッシュ化のコンテキスト
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# セッションの有効期限を計算する関数
def get_session_expiry():
    return datetime.utcnow() + timedelta(seconds=settings.SESSION_EXPIRE_SECONDS)

# パスワードをハッシュ化する関数
def get_password_hash(password):
    return pwd_context.hash(password)

# パスワードを検証する関数
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# セッションデータをJWTに暗号化する
def encrypt_session_data(session_data: SessionData) -> str:
    to_encode = session_data.dict()
    to_encode.update({"exp": get_session_expiry()})  # 有効期限を追加
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

# 暗号化されたセッションデータを検証し復号化する
def decrypt_session_data(encrypted_data: str) -> Optional[SessionData]:
    try:
        payload = jwt.decode(encrypted_data, settings.SECRET_KEY, algorithms=["HS256"])
        return SessionData(**payload)
    except JWTError:
        return None  # 無効な場合はNoneを返す

# セッションIDを生成する関数
def create_session_id() -> str:
    return str(uuid4())  # UUIDを使用したユニークなID

# セッションをクッキーに設定する関数
def set_session_cookie(response: Response, session_id: str, session_data: SessionData) -> None:
    encrypted_data = encrypt_session_data(session_data)
    # クッキーに暗号化されたセッションデータを設定
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=encrypted_data,
        max_age=settings.SESSION_EXPIRE_SECONDS,
        httponly=True,  # JavaScriptからアクセスできないように
        secure=True,    # HTTPS接続の場合のみ送信
        samesite="lax"  # CSRF対策
    )

# セッションクッキーを削除する関数
def delete_session_cookie(response: Response) -> None:
    response.delete_cookie(settings.SESSION_COOKIE_NAME)

# リクエストからセッションデータを取得する依存関係
def get_current_user_session(request: Request) -> Optional[SessionData]:
    cookie_value = request.cookies.get(settings.SESSION_COOKIE_NAME)
    if not cookie_value:
        return None
    
    # クッキーからセッションデータを復号化
    session_data = decrypt_session_data(cookie_value)
    return session_data

# 認証済みユーザーを要求する依存関係
def require_authenticated_user(session_data: Optional[SessionData] = Depends(get_current_user_session)):
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="認証が必要です",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return session_data
