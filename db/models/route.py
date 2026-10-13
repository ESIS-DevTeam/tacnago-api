from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db.base import Base
from sqlalchemy.orm import relationship

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    distance_km = Column(Float, nullable=False)
    duration_min = Column(Integer, nullable=False)
    fare = Column(Float, default=0.0)
    rating = Column(Float, default=0.0)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    creator = relationship("User", back_populates="routes")
    category = relationship("Category", back_populates="routes")
    points = relationship("RoutePoint", back_populates="route", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="route", cascade="all, delete-orphan")
    travel_records = relationship("TravelHistory", back_populates="route")
    notifications = relationship("Notification", back_populates="route")
