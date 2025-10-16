"""Provides CRUD and reporting functions for all LabSmart models."""
from db import get_session
from models import Patient, Technician, TestType, TestOrder, TestResult, OrderStatus
from sqlalchemy.orm import joinedload
from sqlalchemy import func

# -------- PATIENTS --------

def create_patient(first_name, last_name, date_of_birth=None, gender=None, contact=None):
    """Add a new patient record to the database."""
    db = get_session()
    try:
        p = Patient(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, gender=gender, contact=contact)
        db.add(p)
        db.commit()
        db.refresh(p)
        return p
    finally:
        db.close()

# Retrieve a patient and their test orders
def get_patient(patient_id):
    db = get_session()
    try:
        return db.query(Patient).options(joinedload(Patient.orders)).filter(Patient.id == patient_id).one_or_none()
    finally:
        db.close()

# -------- TECHNICIANS --------

def create_technician(name, role=None, contact=None):
    """Register a new technician."""
    db = get_session()
    try:
        t = Technician(name=name, role=role, contact=contact)
        db.add(t)
        db.commit()
        db.refresh(t)
        return t
    finally:
        db.close()

# -------- TEST TYPES --------

def create_test_type(code, name, description=None):
    """Create a new type of laboratory test."""
    db = get_session()
    try:
        tt = TestType(code=code, name=name, description=description)
        db.add(tt)
        db.commit()
        db.refresh(tt)
        return tt
    finally:
        db.close()

# -------- TEST ORDERS --------

def order_test(patient_id, test_type_id):
    """Create a new test order for a patient."""
    db = get_session()
    try:
        order = TestOrder(patient_id=patient_id, test_type_id=test_type_id, status=OrderStatus.PENDING)
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    finally:
        db.close()

# List all test orders (optionally filtered by status)
def list_orders(status=None):
    db = get_session()
    try:
        q = db.query(TestOrder).options(joinedload(TestOrder.patient), joinedload(TestOrder.test_type))
        if status:
            q = q.filter(TestOrder.status == status)
        return q.order_by(TestOrder.ordered_at.desc()).all()
    finally:
        db.close()

# -------- TEST RESULTS --------

def record_result(order_id, technician_id, value):
    """Record a test result and mark the order as completed."""
    db = get_session()
    try:
        order = db.query(TestOrder).filter(TestOrder.id == order_id).one_or_none()
        if not order:
            raise ValueError("Order not found")
        if order.status == OrderStatus.COMPLETED:
            raise ValueError("Order already completed")

        result = TestResult(order_id=order_id, technician_id=technician_id, value=value)
        order.status = OrderStatus.COMPLETED
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
    finally:
        db.close()

# -------- REPORTS --------

def total_tests_between(start_dt, end_dt):
    """Count total tests within a specific time period."""
    db = get_session()
    try:
        return db.query(func.count(TestOrder.id)).filter(TestOrder.ordered_at >= start_dt, TestOrder.ordered_at <= end_dt).scalar()
    finally:
        db.close()

def most_requested_tests(limit=10):
    """Return the most requested tests."""
    db = get_session()
    try:
        q = (
            db.query(TestType.name, func.count(TestOrder.id).label("count"))
            .join(TestOrder, TestOrder.test_type_id == TestType.id)
            .group_by(TestType.id)
            .order_by(func.count(TestOrder.id).desc())
            .limit(limit)
        )
        return q.all()
    finally:
        db.close()

def tests_by_technician(technician_id):
    """List all results performed by a specific technician."""
    db = get_session()
    try:
        return db.query(TestResult).options(joinedload(TestResult.order).joinedload(TestOrder.test_type)).filter(TestResult.technician_id == technician_id).all()
    finally:
        db.close()
