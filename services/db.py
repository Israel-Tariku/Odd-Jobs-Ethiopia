# services/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///data/jobs.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def init_db():
    from models.job import Job
    from models.applicant import Applicant
    Base.metadata.create_all(bind=engine)

def save_job(poster_id, title, description, pay, deadline):
    from models.job import Job
    session = SessionLocal()
    job = Job(
        poster_id=poster_id,
        title=title,
        description=description,
        pay=pay,
        deadline=deadline,
        status="pending"
    )
    session.add(job)
    session.commit()
    job_id = job.id
    session.close()
    return job_id

def save_applicant(job_id, applicant_id):
    from models.applicant import Applicant
    session = SessionLocal()
    applicant = Applicant(job_id=job_id, applicant_id=applicant_id)
    session.add(applicant)
    session.commit()
    session.close()
