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

# to get all the projects
@router.get("/")
def get_all_projects(db: Session = Depends(get_db)):
    pass

# to get a individual projects
@router.get("/{project_id}")
def get_project(project_id:int,db: Session = Depends(get_db)):
    pass

# to add completely a new project to db
@router.post("/add-project")
def add_project(project:Project,db: Session = Depends(get_db)):
    pass

#to edit things in the projects
@router.put("/edit-project/{project_id}")
def edit_project(project:Project,project_id:int,db: Session = Depends(get_db)):
    pass

#to delete a project in the db
@router.delete("/delete-project/{project_id}")
def delete_project(project_id:int,db: Session = Depends(get_db)):
    pass

