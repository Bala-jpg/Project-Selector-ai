from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Achievements
from dependencies import get_db
from pydantic import BaseModel 

class Achievement(BaseModel):
    description:str
    
router=APIRouter(
    prefix="/achievement",
    tags=["Achievement"]
)

# to get all the achievements
@router.get("/")
def get_all_achievement(db: Session = Depends(get_db)):
    query = select(Achievements)
    achievements = db.scalars(query).all()
    return {"Achievements": achievements}


# to get a particular achievement using id
@router.get("/get-achievement/{achievement_id}")
def get_achievement(achievement_id:int,db: Session = Depends(get_db)):
    achievement=db.get(Achievements,achievement_id)
    if not achievement:
        raise HTTPException(status_code=404,detail="achievement not found for the given id")
    return achievement

# to add a achievement
@router.post("/add-achievement")
def add_certificate(achievement:Achievement,db: Session = Depends(get_db)):
    new_achievement=Achievements(description=achievement.description)
    db.add(new_achievement)
    db.commit()
    db.refresh(new_achievement)
    return {"message": f"new achievement added successfully {achievement.description}"}


# to edit the achievement using achievement_id
@router.put("/edit-achievement/{achievement_id}")
def edit_achievement(achievement:Achievement,achievement_id:int,db: Session = Depends(get_db)):        
    curr_achievement=db.get(Achievements,achievement_id)
    if not curr_achievement:
        raise HTTPException(status_code=404,detail="achievement not found for the given id")
    curr_achievement.description=achievement.description
    db.commit()
    db.refresh(curr_achievement)
    return {"message": f"achivement edited successfully {curr_achievement.description}"}

# to delete a achievement
@router.delete("/delete-achievement/{achievement_id}")    
def delete_achievement(achievement_id:int,db: Session = Depends(get_db)):
    achievement=db.get(Achievements,achievement_id)
    if not achievement:
        raise HTTPException(status_code=404,detail="achievement not found for the given id")
    db.delete(achievement)
    db.commit()
    return {"message": f"achievement deleted successfully {achievement.description}"}