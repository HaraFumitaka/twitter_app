# src/crud/users.py
from sqlalchemy.orm import Session
from typing import Optional

from ..models.user import User
from ..auth.schemas import UserCreate
from ..auth.utils import get_password_hash, verify_password

# ユーザー取得（メールアドレスで）
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.e_mail == email).first()

# ユーザー取得（ユーザーIDで）
def get_user_by_user_id(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.user_id == user_id).first()

# ユーザー作成
def create_user(db: Session, user: UserCreate) -> User:
    # パスワードをハッシュ化して安全に保存
    hashed_password = get_password_hash(user.password)
    
    # ユーザーオブジェクト作成
    db_user = User(
        e_mail=user.e_mail,
        password=hashed_password,  # ハッシュ化したパスワードを保存
        user_id=user.user_id,
        user_name=user.user_name,
        phone_number=user.phone_number,
        self_introduction=user.self_introduction,
        place=user.place,
        birthday=user.birthday,
        profile_img=user.profile_img,
        avatar_img=user.avatar_img
    )
    
    # DBに追加
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# ユーザー認証
def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    
    # パスワード検証
    if not verify_password(password, user.password):
        return None
    
    return user
