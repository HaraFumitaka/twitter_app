from sqlalchemy import Column, String, Text, Date, TIMESTAMP, text, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from ..database.session import Base

class User(Base):
    __tablename__ = "Users"  # DBのテーブル名と一致させる

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    e_mail = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # ハッシュ化されたパスワードを保存
    user_id = Column(String(50), unique=True, nullable=False)
    user_name = Column(String(100), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=True)
    self_introduction = Column(Text, nullable=True)
    place = Column(String(100), nullable=True)
    birthday = Column(Date, nullable=True)
    profile_img = Column(String(255), nullable=True)
    avatar_img = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
