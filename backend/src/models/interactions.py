from sqlalchemy import Column, String, BigInteger, ForeignKey, TIMESTAMP, text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from src.database.session import Base

class Like(Base):
    __tablename__ = "Likes"

    user_id = Column(String(50), ForeignKey("Users.user_id"), nullable=False)
    tweet_id = Column(BigInteger, ForeignKey("Tweets.tweet_id"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # 複合主キーの設定
    __table_args__ = (PrimaryKeyConstraint('user_id', 'tweet_id'),)

    # リレーションシップの定義
    user = relationship("User", back_populates="likes")
    tweet = relationship("Tweet", back_populates="likes")

class Retweet(Base):
    __tablename__ = "Retweets"

    user_id = Column(String(50), ForeignKey("Users.user_id"), nullable=False)
    tweet_id = Column(BigInteger, ForeignKey("Tweets.tweet_id"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # 複合主キーの設定
    __table_args__ = (PrimaryKeyConstraint('user_id', 'tweet_id'),)

    # リレーションシップの定義
    user = relationship("User", back_populates="retweets")
    tweet = relationship("Tweet", back_populates="retweets")

class Bookmark(Base):
    __tablename__ = "Bookmarks"

    user_id = Column(String(50), ForeignKey("Users.user_id"), nullable=False)
    tweet_id = Column(BigInteger, ForeignKey("Tweets.tweet_id"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # 複合主キーの設定
    __table_args__ = (PrimaryKeyConstraint('user_id', 'tweet_id'),)

    # リレーションシップの定義
    user = relationship("User", back_populates="bookmarks")
    tweet = relationship("Tweet", back_populates="bookmarks")
