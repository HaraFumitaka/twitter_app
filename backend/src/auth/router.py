from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.crud.users import create_user, authenticate_user, get_user_by_email, get_user_by_user_id
from src.auth.schemas import UserCreate, UserLogin, UserResponse, SessionData
from src.auth.utils import set_session_cookie, delete_session_cookie, get_current_user_session, require_authenticated_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """ユーザー登録エンドポイント"""
    # メールアドレスが既に使用されているか確認
    db_user = get_user_by_email(db, email=user.e_mail)
    if db_user:
        raise HTTPException(status_code=400, detail="このメールアドレスは既に登録されています")
    
    # ユーザーIDが既に使用されているか確認
    db_user = get_user_by_user_id(db, user_id=user.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="このユーザーIDは既に使用されています")
    
    # ユーザー作成
    return create_user(db=db, user=user)

@router.post("/login")
def login(response: Response, user_login: UserLogin, db: Session = Depends(get_db)):
    """ログインエンドポイント"""
    user = authenticate_user(db, user_login.e_mail, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # セッションデータを作成
    session_data = SessionData(user_id=user.user_id)
    
    # セッションクッキーを設定
    set_session_cookie(response, user.user_id, session_data)
    
    return {"message": "ログインに成功しました"}

@router.post("/logout")
def logout(response: Response):
    """ログアウトエンドポイント"""
    delete_session_cookie(response)
    return {"message": "ログアウトしました"}

@router.get("/me", response_model=UserResponse)
def get_current_user(
    db: Session = Depends(get_db), 
    session_data: SessionData = Depends(require_authenticated_user)
):
    """現在ログインしているユーザーの情報を取得するエンドポイント"""
    user = get_user_by_user_id(db, user_id=session_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    return user
