from sqlalchemy import Column, String, Text, TIMESTAMP, text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from src.database.session import Base

class Reply(Base):
    __tablename__ = "Replies"

    reply_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("Users.user_id"), nullable=False)
    tweet_id = Column(BigInteger, ForeignKey("Tweets.tweet_id"), nullable=False)
    parent_reply_id = Column(BigInteger, ForeignKey("Replies.reply_id"), nullable=True)
    reply_content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # リレーションシップの定義
    user = relationship("User", back_populates="replies")
    tweet = relationship("Tweet", back_populates="replies")

    # 自己参照リレーションシップ
    parent_reply = relationship("Reply", remote_side=[reply_id], backref="child_replies")
