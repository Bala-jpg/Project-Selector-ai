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
    skills = db.execute(select(Skills)).scalars().all()
    return skills

# to get a individual skills
@router.get("/{skill_id}")
def get_skill(skill_id:int,db: Session = Depends(get_db)):
    skill=db.get(Skills,skill_id)
    if not skill:
        raise HTTPException(status_code=404,detail="Skill not found for the given id")
    return skill

# to add completely a new skill to db
@router.post("/add-skill")
def add_skill(skill:Skill,db: Session = Depends(get_db)):
    skill=Skills(name=skill.name,description=skill.description)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return {"Skill added successfully":skill}

#to edit things in the skill
@router.put("/edit-skill/{skill_id}")
def edit_skill(skill_data:Skill,skill_id:int,db: Session = Depends(get_db)):
    skill=db.get(Skills,skill_id)
    if not skill:
        raise HTTPException(status_code=404,detail="Skill not found for the given id")
    skill.name=skill_data.name
    skill.description=skill_data.description
    db.commit()
    db.refresh(skill)
    return {"Skill updated":skill}

#to delete a skill in the db
@router.delete("/delete-skill/{skill_id}")
def delete_skill(skill_id:int,db: Session = Depends(get_db)):
    skill=db.get(Skills,skill_id)
    if not skill:
        raise HTTPException(status_code=404,detail="Skill not found")
    db.delete(skill)
    db.commit()
    return {"Skill deleted":skill}

