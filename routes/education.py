from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Educations
from dependencies import get_db
from pydantic import BaseModel 

class Education(BaseModel):
    course_name:str
    cgpa: float
    start_year:int
    end_year:int
    college_name:str
    location:str
    
    
router=APIRouter(
    prefix="/education",
    tags=["Education"]
)

# to get all the educations
@router.get("/")
def get_all_education(db: Session = Depends(get_db)):
    query = select(Educations)
    educations = db.scalars(query).all()
    return {"Educations": educations}


# to get a particular education using id
@router.get("/get-education/{education_id}")
def get_achievement(education_id:int,db: Session = Depends(get_db)):
    education=db.get(Educations,education_id)
    if not education:
        raise HTTPException(status_code=404,detail="Certificate not found for the given id")
    return education


# to add a education
@router.post("/add-education")
def add_certificate(education:Education,db: Session = Depends(get_db)):
    new_education=Educations(course_name=education.course_name,cgpa=education.cgpa,start_year=education.start_year,end_year=education.end_year,college_name=education.college_name,location=education.location)
    db.add(new_education)
    db.commit()
    db.refresh(new_education)
    return {"message": f"new education added successfully {education.course_name}"}


# to edit the education using achievement_id
@router.put("/edit-education/{education_id}")
def edit_achievement(education:Education,education_id:int,db: Session = Depends(get_db)):        
    curr_education=db.get(Educations,education_id)
    if not curr_education:
        raise HTTPException(status_code=404,detail="Certificate not found for the given id")
    curr_education.course_name = education.course_name
    curr_education.cgpa = education.cgpa
    curr_education.start_year = education.start_year
    curr_education.end_year = education.end_year
    curr_education.college_name = education.college_name
    curr_education.location = education.location
    db.commit()
    db.refresh(curr_education)
    return {"message": f"education edited successfully {curr_education.course_name}"}


# to delete a education
@router.delete("/delete-education/{education_id}")    
def delete_achievement(education_id:int,db: Session = Depends(get_db)):
    education=db.get(Educations,education_id)
    if not education:
        raise HTTPException(status_code=404,detail="Education not found for the given id")
    db.delete(education)
    db.commit()
    return {"message": f"education deleted successfully {education.course_name}"}