"""Defines all SQLAlchemy ORM models for the LabSmart system."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum

# Base class for all models
Base = declarative_base()

# Enum for tracking test order status
class OrderStatus(str, enum.Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"

# Patient model stores patient details
class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(String(32))
    gender = Column(String(16))
    contact = Column(String(64))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: one patient → many test orders
    orders = relationship("TestOrder", back_populates="patient", cascade="all, delete-orphan")

# Technician model stores lab staff information
class Technician(Base):
    __tablename__ = "technicians"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    role = Column(String(100))
    contact = Column(String(64))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: one technician → many test results
    results = relationship("TestResult", back_populates="technician")

# TestType model lists available lab tests
class TestType(Base):
    __tablename__ = "test_types"
    id = Column(Integer, primary_key=True)
    code = Column(String(32), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)

    # Relationship: one test type → many orders
    orders = relationship("TestOrder", back_populates="test_type")

# TestOrder links patients with requested tests
class TestOrder(Base):
    __tablename__ = "test_orders"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    test_type_id = Column(Integer, ForeignKey("test_types.id"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    ordered_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="orders")
    test_type = relationship("TestType", back_populates="orders")
    result = relationship("TestResult", back_populates="order", uselist=False, cascade="all, delete-orphan")

# TestResult stores results for each order
class TestResult(Base):
    __tablename__ = "test_results"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("test_orders.id"), nullable=False, unique=True)
    technician_id = Column(Integer, ForeignKey("technicians.id"), nullable=False)
    value = Column(Text, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("TestOrder", back_populates="result")
    technician = relationship("Technician", back_populates="results")
