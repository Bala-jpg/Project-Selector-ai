from sqlalchemy import Column, Integer, String
from database import Base

class Projects(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), index=True)
    
class Skills(Base):
    __tablename__ = "Skills"
    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(255), index=True)
    how_much_known = Column(String(255), index=True)