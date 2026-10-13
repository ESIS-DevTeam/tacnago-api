from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db.base import Base
from sqlalchemy.orm import relationship

class RoutePoint(Base):
    __tablename__ = "route_points"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    order = Column(Integer, nullable=False)

    route = relationship("Route", back_populates="points")
