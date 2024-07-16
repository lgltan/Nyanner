from sqlalchemy import create_engine, Column, Integer, String, BigInteger, ForeignKey, TIMESTAMP, LargeBinary, Boolean, DATE, DATETIME, BLOB, SmallInteger
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(100), nullable=False)
    content = Column(LargeBinary(), nullable=False)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(BigInteger, unique=True, autoincrement=True, primary_key=True)
    user_type = Column(Integer, nullable=False, default=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(16), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(13), unique=True, nullable=False)
    photo_id = Column(Integer, ForeignKey('photos.id'))
    password = Column(LargeBinary(256), nullable=False)
    birthday = Column(DATE)
    
    photo = relationship("Photo")

class Session(Base):
    __tablename__ = 'sessions'
    session_id = Column(BigInteger, unique=True, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'))
    user = relationship("User")
    ban_bool = Column(Boolean, default=False)
    ban_timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())
    ban_time = Column(BigInteger, default=0)

class AdminLog(Base):
    __tablename__ = 'admin_logs'
    admin_log_id = Column(BigInteger, unique=True, primary_key=True, autoincrement=True)
    description = Column(String(256), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())


class Game(Base):
    __tablename__ = 'games'
    game_id = Column(BigInteger, unique=True, primary_key=True, autoincrement=True)
    p1_id = Column(BigInteger, ForeignKey('users.user_id'))
    p2_id = Column(BigInteger, ForeignKey('users.user_id'))
    p3_id = Column(BigInteger, ForeignKey('users.user_id'))
    p4_id = Column(BigInteger, ForeignKey('users.user_id'))

class Move(Base):
    __tablename__ = 'moves'
    moves_id = Column(BigInteger, unique=True, primary_key=True, autoincrement=True)
    game_id = Column(BigInteger, ForeignKey('games.game_id'))
    game = relationship("Game")
    p1_board = Column(String(32))
    p2_board = Column(String(32))
    p3_board = Column(String(32))
    p4_board = Column(String(32))

class IssuedToken(Base):
    __tablename__ = "issued_tokens"
    token_id = Column(String(256), unique=True, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'))
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