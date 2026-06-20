from sqlalchemy import Column, Integer, String,Float
from database import Base

class UserDetails(Base):
    
    __tablename__ = "user_details"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    mobile_number = Column(String(20), index=True)
    email_id = Column(String(40), index=True)
    github_url = Column(String(40), index=True)
    Linkedin_url = Column(String(40), index=True)
    portfolio_link = Column(String(40), index=True)
    Location = Column(String(40), index=True)
    profession_summary = Column(String(255), index=True)

class Education(Base):
    
    __tablename__ = "education"
    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String(50),index=True)
    cgpa = Column(Float,index=True)
    start_year = Column(Integer,index=True)
    End_year = Column(Integer,index=True)
    college_name = Column(String(50), index=True)
    location = Column(String(50),index=True)
    
class Certificate(Base):
    
    __tablename__= "certificate"
    id = Column(Integer, primary_key=True, index=True)
    certificate_issuer = Column(String(255),index=True)
    certificate_name = Column(String(50), index=True)
    
class Internship(Base):
    
    __tablename__="internship"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(50), index=True)
    role = Column(String(20), index=True)
    description = Column(String(255),index=True)
    Duration = Column(String(20),index=True)
    
class Achievement(Base):
    
    __tablename__="achievements"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255),index=True)
    

class Projects(Base):
    
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), index=True)
    tech_stack = Column(String(50),index=True)
    github_url = Column(String(255), index=True)
    live_link = Column(String(255), index=True)
    
class Skills(Base):

    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), index=True)
