"""Initializes the database and seeds with example data."""
from db import engine
from models import Base
from crud import create_patient, create_technician, create_test_type, order_test, record_result

def init():
    print("Creating tables...")
    # Create all tables defined in models
    Base.metadata.create_all(bind=engine)

    print("Seeding sample data...")
    # Create example patients
    p1 = create_patient("Amina", "Mohamed", date_of_birth="1990-05-10", gender="F", contact="+254700000001")
    p2 = create_patient("John", "Karanja", date_of_birth="1985-08-22", gender="M", contact="+254700000002")

    # Create technicians
    t1 = create_technician("Grace W.", role="Lab Technician", contact="+254700000010")
    t2 = create_technician("Sam O.", role="Senior Technician", contact="+254700000011")

    # Create test types
    tt1 = create_test_type("CBC", "Complete Blood Count", description="Full blood count")
    tt2 = create_test_type("BMP", "Basic Metabolic Panel", description="Electrolytes and metabolites")

    # Create test orders
    o1 = order_test(p1.id, tt1.id)
    o2 = order_test(p2.id, tt2.id)

    # Record a test result
    record_result(o1.id, t1.id, value="WBC: 5.6 x10^9/L; RBC: 4.6 x10^12/L; Hb: 13.8 g/dL")

    print("Initialization complete.")

if __name__ == '__main__':
    init()
