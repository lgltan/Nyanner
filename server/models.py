from sqlalchemy import create_engine, Column, Integer, String, BigInteger, ForeignKey, TIMESTAMP, LargeBinary, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_type = Column(String(5), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(16), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(13), unique=True, nullable=False)
    # photo = Column(LargeBinary, nullable=True)
    password = Column(LargeBinary(32), nullable=False)

class Session(Base):
    __tablename__ = 'sessions'
    session_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'))
    user = relationship("User")
    ban_bool = Column(Boolean, default=False)
    ban_timestamp = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    ban_time = Column(BigInteger, default=0)

class AdminLog(Base):
    __tablename__ = 'admin_logs'
    admin_log_id = Column(BigInteger, primary_key=True, autoincrement=True)

class Game(Base):
    __tablename__ = 'games'
    game_id = Column(BigInteger, primary_key=True, autoincrement=True)
    p1_id = Column(BigInteger, ForeignKey('users.user_id'))
    p2_id = Column(BigInteger, ForeignKey('users.user_id'))
    p3_id = Column(BigInteger, ForeignKey('users.user_id'))
    p4_id = Column(BigInteger, ForeignKey('users.user_id'))

class Move(Base):
    __tablename__ = 'moves'
    moves_id = Column(BigInteger, primary_key=True, autoincrement=True)
    game_id = Column(BigInteger, ForeignKey('games.game_id'))
    game = relationship("Game")
    p1_board = Column(String(32))
    p2_board = Column(String(32))
    p3_board = Column(String(32))
    p4_board = Column(String(32))



