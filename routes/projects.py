from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Projects,User
from dependencies import get_db
from pydantic import BaseModel 
from auth.dependencies import get_current_user

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
def get_all_projects(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    query = select(Projects).where(Projects.user_uuid == current_user)
    projects = db.scalars(query).all()
    return {"projects":projects}
    
# to get a individual projects
@router.get("/{project_id}")
def get_project(project_id:int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    project = db.get(Projects,project_id)
    if not project:
        raise HTTPException(status_code=404,detail="Project not found for the given id")
    if project.user_uuid != current_user.user_uuid:
        raise HTTPException(status_code=403,detail="You are not allowed to view this project")
    return project

# to add completely a new project to db
@router.post("/add-project")
def add_project(project:Project,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    new_project = Projects(name=project.name,description=project.description,tech_stack=project.tech_stack,github_url=project.github_url,live_link=project.live_link,user_uuid=current_user.user_uuid)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return {"message":f"Project: {project.name} have been added successfully"}


#to edit things in the projects
@router.put("/edit-project/{project_id}")
def edit_project(project:Project,project_id:int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    curr_project = db.query(Projects).filter(Projects.id==project_id).first()
    
    if not curr_project:
        raise HTTPException(status_code=404,detail="The project with this id is not available")
    if curr_project.user_uuid != current_user.user_uuid:
        raise HTTPException(status_code=403,detail="You are not allowed to edit this project")
    curr_project.name = project.name
    curr_project.description = project.description
    curr_project.tech_stack = project.tech_stack
    curr_project.github_url = project.github_url
    curr_project.live_link = project.live_link
    db.commit()
    db.refresh(curr_project)
    
    return {"message":f"Project: {project.name} has been updated successfully"}    
    
    
#to delete a project in the db
@router.delete("/delete-project/{project_id}")
def delete_project(project_id:int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    project = db.get(Projects,project_id)
    if not project:
        raise HTTPException(status_code=404,detail="Project not found for the given id")
    if project.user_uuid != current_user.user_uuid:
        raise HTTPException(status_code=403,detail="You are not allowed to delete this project")
    db.delete(project)
    db.commit()
    return {"message":f"Project:{project.name} have been deleted successfully"}

