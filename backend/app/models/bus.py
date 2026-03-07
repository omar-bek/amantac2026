"""
Bus model and tracking
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)
    bus_number = Column(String, unique=True, nullable=False)
    license_plate = Column(String, unique=True)
    driver_name = Column(String)
    driver_phone = Column(String)
    capacity = Column(Integer, default=50)
    has_camera = Column(Boolean, default=False)
    camera_stream_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    students = relationship("Student", back_populates="bus")
    routes = relationship("BusRoute", back_populates="bus", cascade="all, delete-orphan")
    locations = relationship("BusLocation", back_populates="bus")

class BusRoute(Base):
    __tablename__ = "bus_routes"

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    route_name = Column(String, nullable=False)
    start_location = Column(String)
    end_location = Column(String)
    waypoints = Column(JSON)  # List of waypoints
    estimated_duration = Column(Integer)  # in minutes
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    bus = relationship("Bus", back_populates="routes")

class BusLocation(Base):
    __tablename__ = "bus_locations"

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed = Column(Float)  # km/h
    heading = Column(Float)  # degrees
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    bus = relationship("Bus", back_populates="locations")





