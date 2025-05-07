# src/crud/tweets.py
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from typing import List, Optional, Tuple

from src.models.tweet import Tweet
from src.models.interactions import Like, Retweet, Bookmark
from src.models.user import User
from src.tweets.schemas import TweetCreate

# ツイート一覧取得
def get_tweets(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    current_user_id: Optional[str] = None
) -> Tuple[List[dict], int]:
    # ツイート、いいね数、リツイート数、ブックマーク数を取得
    query = (
        db.query(
            Tweet,
            User.user_name,
            func.count(Like.tweet_id.distinct()).label("like_count"),
            func.count(Retweet.tweet_id.distinct()).label("retweet_count"),
            func.count(Bookmark.tweet_id.distinct()).label("bookmark_count")
        )
        .join(User, Tweet.user_id == User.user_id)
        .outerjoin(Like, Tweet.tweet_id == Like.tweet_id)
        .outerjoin(Retweet, Tweet.tweet_id == Retweet.tweet_id)
        .outerjoin(Bookmark, Tweet.tweet_id == Bookmark.tweet_id)
        .group_by(Tweet.tweet_id, User.user_name)
        .order_by(desc(Tweet.created_at))
    )
    
    # 総ツイート数の取得
    total = db.query(func.count(Tweet.tweet_id)).scalar()
    
    # ページネーション適用
    tweets_with_counts = query.offset(skip).limit(limit).all()
    
    # 結果をリストに整形
    result = []
    for tweet, user_name, like_count, retweet_count, bookmark_count in tweets_with_counts:
        # 現在のユーザーのインタラクション状態をチェック
        is_liked = False
        is_retweeted = False
        is_bookmarked = False
        
        if current_user_id:
            # 現在のユーザーがいいねしているかチェック
            is_liked = db.query(Like).filter(
                and_(Like.tweet_id == tweet.tweet_id, Like.user_id == current_user_id)
            ).first() is not None
            
            # 現在のユーザーがリツイートしているかチェック
            is_retweeted = db.query(Retweet).filter(
                and_(Retweet.tweet_id == tweet.tweet_id, Retweet.user_id == current_user_id)
            ).first() is not None
            
            # 現在のユーザーがブックマークしているかチェック
            is_bookmarked = db.query(Bookmark).filter(
                and_(Bookmark.tweet_id == tweet.tweet_id, Bookmark.user_id == current_user_id)
            ).first() is not None
        
        # 結果に追加
        result.append({
            "tweet_id": tweet.tweet_id,
            "user_id": tweet.user_id,
            "user_name": user_name,
            "tweet_content": tweet.tweet_content,
            "created_at": tweet.created_at,
            "updated_at": tweet.updated_at,
            "like_count": like_count,
            "retweet_count": retweet_count,
            "bookmark_count": bookmark_count,
            "is_liked": is_liked,
            "is_retweeted": is_retweeted,
            "is_bookmarked": is_bookmarked
        })
    
    return result, total

# ツイート取得（ID指定）
def get_tweet(db: Session, tweet_id: int, current_user_id: Optional[str] = None) -> Optional[dict]:
    # ツイート、いいね数、リツイート数、ブックマーク数を取得
    query_result = (
        db.query(
            Tweet,
            User.user_name,
            func.count(Like.tweet_id.distinct()).label("like_count"),
            func.count(Retweet.tweet_id.distinct()).label("retweet_count"),
            func.count(Bookmark.tweet_id.distinct()).label("bookmark_count")
        )
        .join(User, Tweet.user_id == User.user_id)
        .outerjoin(Like, Tweet.tweet_id == Like.tweet_id)
        .outerjoin(Retweet, Tweet.tweet_id == Retweet.tweet_id)
        .outerjoin(Bookmark, Tweet.tweet_id == Bookmark.tweet_id)
        .filter(Tweet.tweet_id == tweet_id)
        .group_by(Tweet.tweet_id, User.user_name)
        .first()
    )
    
    if not query_result:
        return None
    
    tweet, user_name, like_count, retweet_count, bookmark_count = query_result
    
    # 現在のユーザーのインタラクション状態をチェック
    is_liked = False
    is_retweeted = False
    is_bookmarked = False
    
    if current_user_id:
        # 現在のユーザーがいいねしているかチェック
        is_liked = db.query(Like).filter(
            and_(Like.tweet_id == tweet.tweet_id, Like.user_id == current_user_id)
        ).first() is not None
        
        # 現在のユーザーがリツイートしているかチェック
        is_retweeted = db.query(Retweet).filter(
            and_(Retweet.tweet_id == tweet.tweet_id, Retweet.user_id == current_user_id)
        ).first() is not None
        
        # 現在のユーザーがブックマークしているかチェック
        is_bookmarked = db.query(Bookmark).filter(
            and_(Bookmark.tweet_id == tweet.tweet_id, Bookmark.user_id == current_user_id)
        ).first() is not None
    
    # 結果の整形
    result = {
        "tweet_id": tweet.tweet_id,
        "user_id": tweet.user_id,
        "user_name": user_name,
        "tweet_content": tweet.tweet_content,
        "created_at": tweet.created_at,
        "updated_at": tweet.updated_at,
        "like_count": like_count,
        "retweet_count": retweet_count,
        "bookmark_count": bookmark_count,
        "is_liked": is_liked,
        "is_retweeted": is_retweeted,
        "is_bookmarked": is_bookmarked
    }
    
    return result

# ツイート作成
def create_tweet(db: Session, tweet: TweetCreate, user_id: str) -> Tweet:
    db_tweet = Tweet(
        user_id=user_id,
        tweet_content=tweet.tweet_content
    )
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet

# ツイート削除
def delete_tweet(db: Session, tweet_id: int, user_id: str) -> bool:
    tweet = db.query(Tweet).filter(
        and_(Tweet.tweet_id == tweet_id, Tweet.user_id == user_id)
    ).first()
    
    if not tweet:
        return False
    
    db.delete(tweet)
    db.commit()
    return True

# いいね追加
def add_like(db: Session, tweet_id: int, user_id: str) -> bool:
    # ツイートの存在確認
    tweet = db.query(Tweet).filter(Tweet.tweet_id == tweet_id).first()
    if not tweet:
        return False
    
    # 既にいいねしているか確認
    existing_like = db.query(Like).filter(
        and_(Like.tweet_id == tweet_id, Like.user_id == user_id)
    ).first()
    
    if existing_like:
        return True  # 既にいいねしていた場合は成功とみなす
    
    # いいね追加
    like = Like(tweet_id=tweet_id, user_id=user_id)
    db.add(like)
    db.commit()
    return True

# いいね削除
def remove_like(db: Session, tweet_id: int, user_id: str) -> bool:
    like = db.query(Like).filter(
        and_(Like.tweet_id == tweet_id, Like.user_id == user_id)
    ).first()
    
    if not like:
        return False
    
    db.delete(like)
    db.commit()
    return True

# リツイート追加
def add_retweet(db: Session, tweet_id: int, user_id: str) -> bool:
    # ツイートの存在確認
    tweet = db.query(Tweet).filter(Tweet.tweet_id == tweet_id).first()
    if not tweet:
        return False
    
    # 既にリツイートしているか確認
    existing_retweet = db.query(Retweet).filter(
        and_(Retweet.tweet_id == tweet_id, Retweet.user_id == user_id)
    ).first()
    
    if existing_retweet:
        return True  # 既にリツイートしていた場合は成功とみなす
    
    # リツイート追加
    retweet = Retweet(tweet_id=tweet_id, user_id=user_id)
    db.add(retweet)
    db.commit()
    return True

# リツイート削除
def remove_retweet(db: Session, tweet_id: int, user_id: str) -> bool:
    retweet = db.query(Retweet).filter(
        and_(Retweet.tweet_id == tweet_id, Retweet.user_id == user_id)
    ).first()
    
    if not retweet:
        return False
    
    db.delete(retweet)
    db.commit()
    return True

# ブックマーク追加
def add_bookmark(db: Session, tweet_id: int, user_id: str) -> bool:
    # ツイートの存在確認
    tweet = db.query(Tweet).filter(Tweet.tweet_id == tweet_id).first()
    if not tweet:
        return False
    
    # 既にブックマークしているか確認
    existing_bookmark = db.query(Bookmark).filter(
        and_(Bookmark.tweet_id == tweet_id, Bookmark.user_id == user_id)
    ).first()
    
    if existing_bookmark:
        return True  # 既にブックマークしていた場合は成功とみなす
    
    # ブックマーク追加
    bookmark = Bookmark(tweet_id=tweet_id, user_id=user_id)
    db.add(bookmark)
    db.commit()
    return True

# ブックマーク削除
def remove_bookmark(db: Session, tweet_id: int, user_id: str) -> bool:
    bookmark = db.query(Bookmark).filter(
        and_(Bookmark.tweet_id == tweet_id, Bookmark.user_id == user_id)
    ).first()
    
    if not bookmark:
        return False
    
    db.delete(bookmark)
    db.commit()
    return True
