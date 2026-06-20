from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Internship
from dependencies import get_db
from pydantic import BaseModel 

class InternData(BaseModel):
    companyname:str
    role:str
    description:str
    duration:str
    

router = APIRouter(
    prefix="/internship",
    tags=["internship"]
)

# to get all the internship data
@router.get("/")
def get_internshipdata(db: Session = Depends(get_db)):
    query = select(Internship)
    internship = db.scalars(query).all()
    return {"internship":internship}
    
# to get a individual internship
@router.get("/{internship_id}")
def get_internship(internship_id:int,db: Session = Depends(get_db)):
    internship = db.get(Internship,internship_id)
    return {"company":internship.company_name,"role":internship.role,"description":internship.description,"duration":internship.Duration}

# to add completely a new internship to db
@router.post("/add-internship")
def add_internship(internship:InternData,db: Session = Depends(get_db)):
    new_intern = Internship(company_name=internship.companyname,role=internship.role,description=internship.description,Duration=internship.duration)
    db.add(new_intern)
    db.commit()
    db.refresh(new_intern)
    return {"message":f"Internship:{new_intern.company_name} have been added successfully"}


#to edit things in the internships
@router.put("/edit-internship/{internship_id}")
def edit_internship(internship:InternData,internship_id:int,db: Session = Depends(get_db)):
    curr_internship = db.query(Internship).filter(Internship.id==internship_id).first()
    curr_internship.company_name = internship.companyname
    curr_internship.description = internship.description
    curr_internship.role = internship.role
    curr_internship.Duration = internship.duration
    db.commit()
    db.refresh(curr_internship)
    
    return {"message":f"Internship:{internship.companyname} has been updated successfully"}    
    
    
#to delete a internship in the db
@router.delete("/delete-internship/{internship_id}")
def delete_internship(internship_id:int,db: Session = Depends(get_db)):
    internship = db.get(Internship,internship_id)
    db.delete(internship)
    db.commit()
    return {"message":f"Internship:{internship.company_name} have been deleted successfully"}

