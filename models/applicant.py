# models/applicant.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from services.db import Base

class Applicant(Base):
    __tablename__ = "applicants"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    applicant_id = Column(Integer)
    status = Column(String, default="applied")

    job = relationship("Job", back_populates="applicants")
