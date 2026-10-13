from sqlalchemy import Column, Integer, String, Boolean
from db.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    routes = relationship("Route", back_populates="creator")
    reviews = relationship("Review", back_populates="user")
    travel_history = relationship("TravelHistory", back_populates="user")
    notifications = relationship("Notification", back_populates="user", foreign_keys="Notification.user_id")
    following = relationship("Follower", back_populates="follower", foreign_keys="Follower.follower_id")
    followers = relationship("Follower", back_populates="followed", foreign_keys="Follower.followed_id")
