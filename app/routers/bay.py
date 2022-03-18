from concurrent.futures.process import _python_exit
from fastapi import  Depends, FastAPI,Response,status,HTTPException,Depends,APIRouter
from pip import List
from sqlalchemy.orm  import Session
from .. import models, schemas , utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix= "/bay",
    tags=['bay'])



@router.post("/admin",status_code=status.HTTP_201_CREATED)
async def bay(user:schemas.bay ,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_admin)):

    new_user = models.bay(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user

@router.delete("/admin{bay_name}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_bay(bay_name:str ,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_admin)):
    bay = db.query(models.bay).filter(models.bay.bay_name == bay_name)
    bay_q=bay.first()

    if bay == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="not found")
    bay.delete(synchronize_session= False)
    db.commit()
    return "Bay successfully deleted"

@router.get("/admin")
def get_bay(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_admin)):
    bay= db.query(models.bay).all()

    if not bay:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="No Bays found")

    return bay

@router.put("/admin{bay_name}",status_code=status.HTTP_202_ACCEPTED)
async def update_bay(bay_name:str,user:schemas.bay_update,db: Session = Depends(get_db) ,current_user : str = Depends(oauth2.get_current_admin)):
    bay_q = db.query(models.bay).filter(models.bay.bay_name == bay_name)
    bay=bay_q.first()

    if bay_name == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="not found")

    bay_q.update(user.dict(),synchronize_session= False)
    db.commit()

    return user




@router.post("/subadmin",status_code=status.HTTP_201_CREATED)
async def bay(user:schemas.bay ,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_subadmin)):

    new_user = models.bay(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user

@router.delete("/subadmin{bay_name}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_bay(bay_name:str ,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_subadmin)):
    bay = db.query(models.bay).filter(models.bay.bay_name == bay_name)
    bay_q=bay.first()

    if bay == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="not found")
    bay.delete(synchronize_session= False)
    db.commit()
    return "Bay successfully deleted"

@router.get("/subadmin")
def get_bay(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_subadmin)):
    bay= db.query(models.bay).all()

    if not bay:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="No Bays found")

    return bay

@router.put("/subadmin{bay_name}",status_code=status.HTTP_202_ACCEPTED)
async def update_bay(bay_name:str,user:schemas.bay_update,db: Session = Depends(get_db) ,current_user : str = Depends(oauth2.get_current_subadmin)):
    bay_q = db.query(models.bay).filter(models.bay.bay_name == bay_name)
    bay=bay_q.first()

    if bay_name == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="not found")

    bay_q.update(user.dict(),synchronize_session= False)
    db.commit()

    return user