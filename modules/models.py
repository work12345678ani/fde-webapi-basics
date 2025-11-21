from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class JobBoard(Base):
  __tablename__ = 'job_boards'
  id = Column(Integer, primary_key=True)
  slug = Column(String, nullable=False, unique=True) # Represents the company name


class JobPosts(Base):
  __tablename__ = 'job_posts'
  id = Column(Integer, primary_key=True, autoincrement=True)
  description = Column(String, nullable=False, unique=True) # Represents the company name
  title = Column(String, nullable=False)
  company_id = Column(Integer, ForeignKey('job_boards.id'), nullable=False)
  location = Column(String, nullable=True)
  job_board = relationship("JobBoard")

