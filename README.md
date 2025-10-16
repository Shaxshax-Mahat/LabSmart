# LabSmart Backend

A simple backend-only Laboratory Management System using Python, PostgreSQL, and SQLAlchemy.

## Files
- requirements.txt → Required dependencies
- README.md → Setup guide
- .env.example → Example environment variables
- db.py → Database connection setup
- models.py → SQLAlchemy models for the lab entities
- crud.py → CRUD functions for all entities
- init_db.py → Creates tables and seeds sample data
- sample_usage.py → Demonstrates how to use CRUD functions

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a PostgreSQL database and set the DATABASE_URL environment variable:

   ```bash
   export DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/labsmart
   ```

   Or copy `.env.example` to `.env` and update the DATABASE_URL.

3. Initialize the database and load sample data:

   ```bash
   python init_db.py
   ```

4. Run sample usage to test CRUD operations:

   ```bash
   python sample_usage.py
   ```
