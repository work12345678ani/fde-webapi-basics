from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class JobBoard(Base):
  __tablename__ = 'job_boards'
  id = Column(Integer, primary_key=True)
  slug = Column(String, nullable=False, unique=True) # Represents the company name
  logo_url = Column(String, nullable=True, unique=False)
  job_posts = relationship("JobPosts", cascade="all, delete-orphan")


class JobPosts(Base):
  __tablename__ = 'job_posts'
  id = Column(Integer, primary_key=True, autoincrement=True)
  description = Column(String, nullable=False, unique=True) # Represents the company name
  title = Column(String, nullable=False)
  company_id = Column(Integer, ForeignKey('job_boards.id'), nullable=False)
  isOpen = Column(Boolean, nullable=True)
  location = Column(String, nullable=True)
  job_board = relationship("JobBoard")
  applications = relationship("JobApplications", cascade="all, delete-orphan")


class JobApplications(Base):
  __tablename__ = 'job_applications'
  id = Column(Integer, primary_key=True, autoincrement=True)
  job_post_id = Column(Integer, ForeignKey('job_posts.id'), nullable=False)
  first_name = Column(String)
  last_name = Column(String)
  email = Column(String)
  resume_loc = Column(String)