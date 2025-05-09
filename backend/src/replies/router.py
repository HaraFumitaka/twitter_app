from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import Optional

from src.database.session import get_db
from src.auth.schemas import SessionData
from src.auth.utils import require_authenticated_user
from src.replies.schemas import ReplyCreate, ReplyList, ReplyDetail, ReplyResponse
from src.crud.replies import get_replies_for_tweet, get_reply, create_reply, delete_reply

router = APIRouter()

@router.get("/tweets/{tweet_id}/replies", response_model=ReplyList)
def read_tweet_replies(
    tweet_id: int = Path(..., title="対象ツイートID"),
    parent_reply_id: Optional[int] = Query(None, title="親リプライID"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    session_data: SessionData = Depends(require_authenticated_user)
):
    """
    ツイートに対するリプライ一覧を取得
    parent_reply_id が指定されていれば、そのリプライへのリプライを取得
    """
    skip = (page - 1) * page_size
    replies, total = get_replies_for_tweet(
        db=db,
        tweet_id=tweet_id,
        parent_reply_id=parent_reply_id,
        skip=skip,
        limit=page_size
    )
    
    return {
        "replies": replies,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.get("/replies/{reply_id}", response_model=ReplyDetail)
def read_reply(
    reply_id: int = Path(..., title="リプライID"),
    db: Session = Depends(get_db),
    session_data: SessionData = Depends(require_authenticated_user)
):
    """指定したIDのリプライを取得"""
    reply = get_reply(db=db, reply_id=reply_id)
    if not reply:
        raise HTTPException(status_code=404, detail="リプライが見つかりません")
    return reply

@router.post("/tweets/{tweet_id}/replies", response_model=ReplyDetail)
def post_reply(
    tweet_id: int = Path(..., title="対象ツイートID"),
    reply: ReplyCreate = None,
    db: Session = Depends(get_db),
    session_data: SessionData = Depends(require_authenticated_user)
):
    """ツイートまたはリプライに対して新しいリプライを投稿"""
    try:
        db_reply = create_reply(
            db=db,
            reply=reply,
            tweet_id=tweet_id,
            user_id=session_data.user_id
        )
        
        # 新しく作成したリプライの詳細情報を取得して返す
        result = get_reply(db=db, reply_id=db_reply.reply_id)
        if not result:
            raise HTTPException(status_code=404, detail="リプライの取得に失敗しました")
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/replies/{reply_id}", response_model=ReplyResponse)
def remove_reply(
    reply_id: int = Path(..., title="リプライID"),
    db: Session = Depends(get_db),
    session_data: SessionData = Depends(require_authenticated_user)
):
    """リプライを削除（自分のリプライのみ）"""
    success = delete_reply(db=db, reply_id=reply_id, user_id=session_data.user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="リプライが見つからないか、削除権限がありません")
    
    return {
        "success": True,
        "message": "リプライを削除しました",
        "reply_id": reply_id
    }
