from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)
    due_date = Column(DateTime)
    # Add additional fields as needed