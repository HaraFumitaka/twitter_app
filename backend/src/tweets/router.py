from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from src.database.session import get_db
from src.auth.schemas import SessionData
from src.auth.utils import require_authenticated_user
from src.tweets.schemas import TweetCreate, TweetList, TweetDetail, InteractionResponse
from src.crud.tweets import (
    get_tweets, get_tweet, create_tweet, delete_tweet, 
    add_like, remove_like, add_retweet, remove_retweet,
    add_bookmark, remove_bookmark
)

router = APIRouter()

@router.get("/", response_model=TweetList)
def read_tweets(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    session_data: Optional[SessionData] = Depends(require_authenticated_user)
):
    """ツイート一覧を取得"""
    skip = (page - 1) * page_size
    tweets, total = get_tweets(
        db=db, 
        skip=skip, 
        limit=page_size,
        current_user_id=session_data.user_id
    )
    
    return {
        "tweets": tweets,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.get("/{tweet_id}", response_model=TweetDetail)
def read_tweet(
    tweet_id: int,
    db: Session = Depends(get_db),
    session_data: Optional[SessionData] = Depends(require_authenticated_user)
):
    """指定したIDのツイートを取得"""
    tweet = get_tweet(db=db, tweet_id=tweet_id, current_user_id=session_data.user_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="ツイートが見つかりません")
    return tweet

@router.post("/", response_model=TweetDetail)
def post_tweet(
    tweet: TweetCreate,
    db: Session = Depends(get_db),
    session_data: SessionData = Depends(require_authenticated_user)
):
    """新しいツイートを投稿"""
    db_tweet = create_tweet(db=db, tweet=tweet, user_id=session_data.user_id)
    
    # 新しく作成したツイートの詳細情報を取得して返す
    result = get_tweet(db=db, tweet_id=db_tweet.tweet_id, current_user_id=session_data.user_id)
    if not result:
        raise HTTPException(status_code=404, detail="ツイートの取得に失敗しました")
    
    return result

@router.delete("/{tweet_id}", response_model=InteractionResponse)
def remove_tweet(
    tweet_id: int,
    db: Session = Depends(get_db),
    session_data: SessionData = Depends(require_authenticated_user)
):
    """ツイートを削除"""
    success = delete_tweet(db=db, tweet_id=tweet_id, user_id=session_data.user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="ツイートが見つからないか、削除権限がありません")
    
    return {
        "success": True,
        "message": "ツイートを削除しました",
        "tweet_id": tweet_id
    }

@router.post("/{tweet_id}/like", response_model=InteractionResponse)
def like_tweet(
    tweet_id: int,
    db: Session = Depends(get_db),
    session_data: SessionData = Depends(require_authenticated_user)
):
    """ツイートにいいねを追加"""
    success = add_like(db=db, tweet_id=tweet_id, user_id=session_data.user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="ツイートが見つかりません")
    
    return {
        "success": True,
        "message": "いいねしました",
        "tweet_id": tweet_id
    }

@router.delete("/{tweet_id}/like", response_model=InteractionResponse)
def unlike_tweet(
    tweet_id: int,
    db: Session = Depends(get_db),
    session_data: SessionData = Depends(require_authenticated_user)
):
    """ツイートのいいねを削除"""
    success = remove_like(db=db, tweet_id=tweet_id, user_id=session_data.user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="いいねが見つかりません")
    
    return {
        "success": True,
        "message": "いいねを取り消しました",
        "tweet_id": tweet_id
    }

@router.post("/{tweet_id}/retweet", response_model=InteractionResponse)
def retweet_tweet(
    tweet_id: int,
    db: Session = Depends(get_db),
    session_data: SessionData = Depends(require_authenticated_user)
):
    """ツイートをリツイート"""
    success = add_retweet(db=db, tweet_id=tweet_id, user_id=session_data.user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="ツイートが見つかりません")
    
    return {
        "success": True,
        "message": "リツイートしました",
        "tweet_id": tweet_id
    }

@router.delete("/{tweet_id}/retweet", response_model=InteractionResponse)
def undo_retweet(
    tweet_id: int,
    db: Session = Depends(get_db),
    session_data: SessionData = Depends(require_authenticated_user)
):
    """ツイートのリツイートを取り消し"""
    success = remove_retweet(db=db, tweet_id=tweet_id, user_id=session_data.user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="リツイートが見つかりません")
    
    return {
        "success": True,
        "message": "リツイートを取り消しました",
        "tweet_id": tweet_id
    }

@router.post("/{tweet_id}/bookmark", response_model=InteractionResponse)
def bookmark_tweet(
    tweet_id: int,
    db: Session = Depends(get_db),
    session_data: SessionData = Depends(require_authenticated_user)
):
    """ツイートをブックマーク"""
    success = add_bookmark(db=db, tweet_id=tweet_id, user_id=session_data.user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="ツイートが見つかりません")
    
    return {
        "success": True,
        "message": "ブックマークしました",
        "tweet_id": tweet_id
    }

@router.delete("/{tweet_id}/bookmark", response_model=InteractionResponse)
def unbookmark_tweet(
    tweet_id: int,
    db: Session = Depends(get_db),
    session_data: SessionData = Depends(require_authenticated_user)
):
    """ツイートのブックマークを取り消し"""
    success = remove_bookmark(db=db, tweet_id=tweet_id, user_id=session_data.user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="ブックマークが見つかりません")
    
    return {
        "success": True,
        "message": "ブックマークを取り消しました",
        "tweet_id": tweet_id
    }
