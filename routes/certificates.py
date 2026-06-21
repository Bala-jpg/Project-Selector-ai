from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Certificate
from dependencies import get_db
from pydantic import BaseModel 

class Certificates(BaseModel):
    certificate_issuer: str
    certificate_name: str
    
router=APIRouter(
    prefix="/certificates",
    tags=["Certificates"]
)

@router.get("/")
def get_all_certificates(db: Session = Depends(get_db)):
    query = select(Certificate)
    certificates = db.scalars(query).all()
    return {"certificates": certificates}

@router.get("/get-certificate/{certificate_id}")
def get_certificate(certificate_id:int,db: Session = Depends(get_db)):
    certificate=db.get(Certificate,certificate_id)
    if not certificate:
        raise HTTPException(status_code=404,detail="Certificate not found for the given id")
    return certificate

@router.post("/add-certificate")
def add_certificate(certificate:Certificates,db: Session = Depends(get_db)):
    certificate=Certificate(certificate_issuer=certificate.certificate_issuer,certificate_name=certificate.certificate_name)
    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    return {"Certificate added successfully": certificate}

@router.put("/edit-certificate/{certificate_id}")
def edit_certificate(certificate:Certificates,certificate_id:int,db: Session = Depends(get_db)):        
    curr_certificate=db.get(Certificate,certificate_id)
    if not certificate:
        raise HTTPException(status_code=404,detail="Certificate not found for the given id")
    curr_certificate.certificate_issuer=certificate.certificate_issuer
    curr_certificate.certificate_name=certificate.certificate_name
    db.commit()
    db.refresh(curr_certificate)
    return {"Certificate updated": curr_certificate}
@router.delete("/delete-certificate/{certificate_id}")    
def delete_certificate(certificate_id:int,db: Session = Depends(get_db)):
    certificate=db.get(Certificate,certificate_id)
    if not certificate:
        raise HTTPException(status_code=404,detail="Certificate not found for the given id")
    db.delete(certificate)
    db.commit()
    return {"Certificate deleted": certificate}