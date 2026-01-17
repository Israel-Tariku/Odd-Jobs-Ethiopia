# models/job.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from services.db import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    poster_id = Column(Integer)
    title = Column(String)
    description = Column(String)
    pay = Column(String)
    deadline = Column(String)
    status = Column(String, default="pending")

    applicants = relationship("Applicant", back_populates="job")
