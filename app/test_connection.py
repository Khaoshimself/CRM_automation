from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Confirm connection and database name
        result = db.session.execute(text('SELECT current_database()')).scalar()
        print(f"Connected to database: {result}")

        # Attempt to create tables
        db.create_all()
        print("Tables created successfully.")

        # Check if tables exist
        tables = db.session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        table_list = tables.fetchall()
        print("Tables in the database:", table_list)
    except Exception as e:
        print(f"Error during table creation: {e}")
