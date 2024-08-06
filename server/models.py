from sqlalchemy import create_engine, Column, Integer, String, BigInteger, ForeignKey, TIMESTAMP, LargeBinary, Boolean, DATE, DATETIME, BLOB, SmallInteger, Enum
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BIGINT

Base = declarative_base()

class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(100), nullable=False)
    content = Column(LargeBinary(), nullable=False)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(BIGINT(unsigned=True), unique=True, autoincrement=True, primary_key=True)
    user_type = Column(Integer, nullable=False, default=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(16), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(13), unique=True, nullable=False)
    photo_id = Column(Integer, ForeignKey('photos.id'))
    user_password = Column(LargeBinary(256), nullable=False)
    birthday = Column(DATE)
    
    photo = relationship("Photo")

class BannedUsers(Base):
    __tablename__ = 'bannedusers'
    bannedusers_id = Column(BigInteger, unique=True, primary_key=True, autoincrement=True)
    key_to_user_id = Column(BIGINT(unsigned=True), ForeignKey('users.user_id'))
    key_to_user_id = relationship("User")
    ban_bool = Column(Boolean, default=False)
    ban_timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())
    ban_time = Column(BigInteger, default=0)

class AdminLog(Base):
    __tablename__ = 'admin_logs'
    admin_log_id = Column(BigInteger, unique=True, primary_key=True, autoincrement=True)
    admin_description = Column(String(256), nullable=False)
    admin_timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())


class Lobby(Base):
    __tablename__ = 'lobby'
    lobby_id = Column(BigInteger, unique=True, primary_key=True, autoincrement=True)
    lobby_code = Column(String(6), nullable=False)
    lobby_status = Column("lobby_status", Enum("Waiting", "Ongoing", "Archive"), nullable=False)
    p1_id = Column(BIGINT(unsigned=True), ForeignKey('users.user_id'))
    p2_id = Column(BIGINT(unsigned=True), ForeignKey('users.user_id'))

class Move(Base):
    __tablename__ = 'moves'
    moves_id = Column(BigInteger, unique=True, primary_key=True, autoincrement=True)
    lobby_id = Column(BigInteger, ForeignKey('lobby.lobby_id'))
    lobby = relationship("Lobby")
    board = Column(String(256), nullable=False)

class IssuedToken(Base):
    __tablename__ = "issued_tokens"
    token_id = Column(String(256), unique=True, primary_key=True)
    user_id = Column(BIGINT(unsigned=True), ForeignKey('users.user_id'))
    user = relationship("User")
    issued_at = Column(DATETIME, nullable=False)
    invalidated = Column(Boolean, default=False)
    
# class Lobby(Base):
#     __tablename__ = "game"
#     lobby_name = Column(String(24))
#     p1_id = Column(String(24), nullable=False)
#     p2_id = Column(String(24))
#     p3_id = Column(String(24))
#     p4_id = Column(String(24))
#     p1_pos = Column(SmallInteger(4))
#     p2_pos = Column(SmallInteger(4))
#     p3_pos = Column(SmallInteger(4))
#     p4_pos = Column(SmallInteger(4))
#     p1_board = Column(Integer(120))
#     p2_board = Column(Integer(120))
#     p3_board = Column(Integer(120))
#     p4_board = Column(Integer(120))