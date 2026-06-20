from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Projects
from dependencies import get_db
from pydantic import BaseModel 

class Project(BaseModel):
    name:str
    description:str
    tech_stack:str
    github_url:str
    live_link:str
    

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.post("/")
def add_project(project: Project,db: Session = Depends(get_db)):
    
    data = Projects(
        name=project.name,
        description=project.description,
        tech_stack = project.tech_stack,
        github_url = project.github_url,
        live_link = project.live_link
    )
    db.add(data)
    db.commit()
    db.refresh(data)

    return data
