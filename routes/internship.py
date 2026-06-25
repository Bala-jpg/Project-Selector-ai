from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Internship,User
from dependencies import get_db
from pydantic import BaseModel
from auth.dependencies import get_current_user

class InternData(BaseModel):
    company_name:str
    role:str
    description:str
    duration:str
    

router = APIRouter(
    prefix="/internship",
    tags=["Internship"]
)

# to get all the internship data
@router.get("/")
def get_internship_data(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    query = select(Internship).where(Internship.user_uuid == current_user.user_uuid)
    internship = db.scalars(query).all()
    return {"internship":internship}
    
# to get a individual internship
@router.get("/{internship_id}")
def get_internship(internship_id:int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    internship = db.get(Internship,internship_id)
    if not internship:
        raise HTTPException(status_code=404,detail="Internship not found for the given id")
    if internship.user_uuid != current_user.user_uuid:
        raise HTTPException(status_code=403,detail="You are now allowed to view this internship")
    return {"company":internship.company_name,"role":internship.role,"description":internship.description,"duration":internship.Duration}

# to add completely a new internship to db
@router.post("/add-internship")
def add_internship(internship:InternData,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    new_intern = Internship(company_name=internship.company_name,role=internship.role,description=internship.description,Duration=internship.duration,user_uuid=current_user.user_uuid)
    db.add(new_intern)
    db.commit()
    db.refresh(new_intern)
    return {"message":f"Internship: {new_intern.company_name} have been added successfully"}


#to edit things in the internships
@router.put("/edit-internship/{internship_id}")
def edit_internship(internship:InternData,internship_id:int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    curr_internship = db.query(Internship).filter(Internship.id==internship_id).first()
    if not curr_internship:
        raise HTTPException(status_code=404,detail="The internship with that id doesnt exists")
    if curr_internship.user_uuid != current_user.user_uuid:
        raise HTTPException(status_code=403,detail="You are not allowed to view this internship")
    curr_internship.company_name = internship.company_name
    curr_internship.description = internship.description
    curr_internship.role = internship.role
    curr_internship.Duration = internship.duration
    db.commit()
    db.refresh(curr_internship)
    
    return {"message":f"Internship:{internship.company_name} has been updated successfully"}    
    
    
#to delete a internship in the db
@router.delete("/delete-internship/{internship_id}")
def delete_internship(internship_id:int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    internship = db.get(Internship,internship_id)
    if not internship:
        raise HTTPException(status_code=404,detail="Internship not found for the given id")
    if internship.user_uuid != current_user.user_uuid:
        raise HTTPException(status_code=403,detail="You are not allowed to delete this internship")
    db.delete(internship)
    db.commit()
    return {"message":f"Internship:{internship.company_name} have been deleted successfully"}

