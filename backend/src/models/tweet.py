from sqlalchemy import Column, String, Text, TIMESTAMP, text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from src.database.session import Base

class Tweet(Base):
    __tablename__ = "Tweets"  # DBのテーブル名と一致

    tweet_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("Users.user_id"), nullable=False)
    tweet_content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # リレーションシップの定義
    user = relationship("User", back_populates="tweets")
    likes = relationship("Like", back_populates="tweet", cascade="all, delete-orphan")
    retweets = relationship("Retweet", back_populates="tweet", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="tweet", cascade="all, delete-orphan")
