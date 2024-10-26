from app import create_app, db
from models import User  # Ensure this imports correctly
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Attempt to create tables
        db.create_all()
        print("Tables created successfully.")

        # Explicitly use `text()` for raw SQL
        tables = db.session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        table_list = tables.fetchall()
        print("Tables in the database after create_all:", table_list)
    except Exception as e:
        print(f"Error during table creation: {e}")
