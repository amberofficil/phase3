from sqlmodel import SQLModel
from database.engine import engine
from models.user import User
from models.task import Task

# Sab tables create kar do
SQLModel.metadata.create_all(engine)
print("✅ All tables created successfully!")
