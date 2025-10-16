"""Example of how to use CRUD functions to interact with the database."""
from crud import create_patient, create_test_type, order_test, list_orders, record_result, most_requested_tests, create_technician, get_patient

# Demonstration of CRUD operations
def run():
    # 1. Create new patient
    print("Creating a new patient...")
    p = create_patient("Fatuma", "Ali", date_of_birth="2000-01-01", gender="F", contact="+254700000099")
    print("Patient created:", p)

    # 2. Create new test type
    print("Creating a test type...")
    tt = create_test_type("LFT", "Liver Function Test", description="Measures liver enzymes")
    print("TestType created:", tt)

    # 3. Create a test order
    print("Placing an order for the patient...")
    o = order_test(p.id, tt.id)
    print("Order placed:", o)

    # 4. List all pending orders
    print("Listing pending orders...")
    pending = list_orders()
    for x in pending:
        print(x)

    # 5. Record a test result for the first order
    if pending:
        first = pending[0]
        tech = create_technician("Demo Tech")
        res = record_result(first.id, tech.id, value="ALT: 25 U/L; AST: 30 U/L")
        print("Result recorded:", res)

    # 6. Show analytics
    print("Most requested tests:")
    print(most_requested_tests())

    # 7. Display patient with orders
    print(get_patient(p.id))

if __name__ == '__main__':
    run()
