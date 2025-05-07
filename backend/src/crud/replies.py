from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc, case
from typing import List, Optional, Tuple

from src.models.reply import Reply
from src.models.user import User
from src.models.tweet import Tweet
from src.replies.schemas import ReplyCreate

# ツイートに対するリプライ一覧を取得
def get_replies_for_tweet(
    db: Session,
    tweet_id: int,
    parent_reply_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20
) -> Tuple[List[dict], int]:
    """
    指定したツイートに対するリプライ一覧を取得
    parent_reply_id=None の場合は、ツイートへの直接リプライのみ取得
    parent_reply_id が指定されている場合は、そのリプライへのリプライを取得
    """
    # メインクエリを準備
    query = (
        db.query(
            Reply,
            User.user_name
        )
        .join(User, Reply.user_id == User.user_id)
        .filter(Reply.tweet_id == tweet_id)
        .filter(Reply.parent_reply_id == parent_reply_id)
        .group_by(Reply.reply_id, User.user_name)
        .order_by(desc(Reply.created_at))
    )
    
    # 総リプライ数の取得
    total = db.query(func.count(Reply.reply_id))\
        .filter(Reply.tweet_id == tweet_id)\
        .filter(Reply.parent_reply_id == parent_reply_id)\
        .scalar()
    
    # ページネーション適用
    replies_with_user = query.offset(skip).limit(limit).all()
    
    # 結果をリストに整形
    result = []
    for reply, user_name in replies_with_user:
        # 子リプライの数を個別に取得
        child_reply_count = db.query(func.count(Reply.reply_id))\
            .filter(Reply.parent_reply_id == reply.reply_id)\
            .scalar()
        
        result.append({
            "reply_id": reply.reply_id,
            "user_id": reply.user_id,
            "user_name": user_name,
            "tweet_id": reply.tweet_id,
            "parent_reply_id": reply.parent_reply_id,
            "reply_content": reply.reply_content,
            "created_at": reply.created_at,
            "updated_at": reply.updated_at,
            "child_reply_count": child_reply_count
        })
    
    return result, total

# リプライを取得（ID指定）
def get_reply(db: Session, reply_id: int) -> Optional[dict]:
    reply_data = (
        db.query(Reply, User.user_name)
        .join(User, Reply.user_id == User.user_id)
        .filter(Reply.reply_id == reply_id)
        .first()
    )
    
    if not reply_data:
        return None
    
    reply, user_name = reply_data
    
    # 子リプライの数を取得
    child_reply_count = db.query(func.count(Reply.reply_id))\
        .filter(Reply.parent_reply_id == reply_id)\
        .scalar()
    
    return {
        "reply_id": reply.reply_id,
        "user_id": reply.user_id,
        "user_name": user_name,
        "tweet_id": reply.tweet_id,
        "parent_reply_id": reply.parent_reply_id,
        "reply_content": reply.reply_content,
        "created_at": reply.created_at,
        "updated_at": reply.updated_at,
        "child_reply_count": child_reply_count
    }

# リプライを作成
def create_reply(
    db: Session,
    reply: ReplyCreate,
    tweet_id: int,
    user_id: str
) -> Reply:
    # 親リプライがある場合、存在確認
    if reply.parent_reply_id:
        parent_reply = db.query(Reply).filter(Reply.reply_id == reply.parent_reply_id).first()
        if not parent_reply or parent_reply.tweet_id != tweet_id:
            raise ValueError("親リプライが存在しないか、指定されたツイートに属していません")
    
    # ツイートの存在確認
    tweet = db.query(Tweet).filter(Tweet.tweet_id == tweet_id).first()
    if not tweet:
        raise ValueError("ツイートが存在しません")
    
    # リプライの作成
    db_reply = Reply(
        user_id=user_id,
        tweet_id=tweet_id,
        parent_reply_id=reply.parent_reply_id,
        reply_content=reply.reply_content
    )
    
    db.add(db_reply)
    db.commit()
    db.refresh(db_reply)
    
    return db_reply

# リプライを削除
def delete_reply(db: Session, reply_id: int, user_id: str) -> bool:
    # リプライの存在と所有権を確認
    reply = db.query(Reply).filter(
        and_(Reply.reply_id == reply_id, Reply.user_id == user_id)
    ).first()
    
    if not reply:
        return False
    
    # リプライを削除（カスケード削除で子リプライも削除される）
    db.delete(reply)
    db.commit()
    
    return True
