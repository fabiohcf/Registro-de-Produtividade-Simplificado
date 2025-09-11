from app.database import engine, Base
from app.models import *

def init_db():
    print("Creating tables in the database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully.")

if __name__ == "__main__":
    init_db()
