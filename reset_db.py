from database import Base, engine
import app.models

from app.models.user import User 
print("Dropping all existing tables...")
Base.metadata.drop_all(bind=engine)

print("Recreating tables with the updated schema...")
Base.metadata.create_all(bind=engine)

print("Database successfully reset!")
