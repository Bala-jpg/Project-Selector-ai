from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Skills
from dependencies import get_db
from pydantic import BaseModel 

class Skill(BaseModel):
    name:str
    description:str
    

router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)

# to get all the skills
@router.get("/")
def get_all_skills(db: Session = Depends(get_db)):
    pass

# to get a individual skills
@router.get("/{skill_id}")
def get_skill(skill_id:int,db: Session = Depends(get_db)):
    pass

# to add completely a new skill to db
@router.post("/add-skill")
def add_skill(skill:Skill,db: Session = Depends(get_db)):
    pass

#to edit things in the skill
@router.put("/edit-skill/{skill_id}")
def edit_skill(skill:Skill,skill_di_id:int,db: Session = Depends(get_db)):
    pass

#to delete a skill in the db
@router.delete("/delete-skill/{skill_id}")
def delete_skill(skill_id:int,db: Session = Depends(get_db)):
    pass

