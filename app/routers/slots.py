from sys import api_version
from fastapi import  Depends, FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm  import Session
from typing import  List, Optional

from app import oauth2
from .. import models, schemas , oauth2
from ..database import get_db
from sqlalchemy import func
from datetime import date

router = APIRouter(
    prefix="/slots",
    tags=['slots']
)



#@router.get("/", response_model= List[schemas.Post])
@router.get("/all")
async def posts(db: Session = Depends(get_db),limit:int = 10,skip:int = 0, search : Optional[str]=""):
    print(limit)
    post =db.query(models.slots).filter(models.slots.truck.contains(search)).limit(limit).offset(offset=skip).all()
    return  post

#,response_model= List[schemas.returnbooked]
@router.get("/empty/{product}/{date}")
async def filled(product :str,date : date ,db: Session = Depends(get_db)):
    post = []
    product_id = db.query(models.products.id).filter(models.products.product == product).all()
    bay = db.query(models.bay.id).filter(models.bay.product_id == product_id[0][0]).all()
    for i in bay:
        post = post + db.query(models.days_10.id,models.days_10.bay_id,models.days_10.slot,models.days_10.slot).filter(models.days_10.bay_id == i[0],models.days_10.date == date,models.days_10.booked == False).all()
    return  post

@router.post("/", status_code=status.HTTP_201_CREATED)
async def screate(payload:schemas.createslot,slot_id:schemas.createslot_id,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    print(slot_id.slot_id)
    new_post = models.slots(phone = current_user.phone,client_id=current_user.client_id, **payload.dict())
    post_update =  db.query(models.days_10).filter(models.days_10.id == slot_id.slot_id)
    post = post_update.first()
    print(post.booked)

    # post_update.update(booked = True,synchronize_session= False)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post
    



@router.delete("/{truck}",status_code=status.HTTP_204_NO_CONTENT)
def delete_slot(truck:str,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_admin)):
    
    post_q = db.query(models.slots).filter(models.slots.truck == truck)
    post=post_q.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="not found")
    print(post.owner_id, current_user.id)
   
    if (post.owner_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="Cant  perform opp")

    post_q.delete(synchronize_session= False)
    db.commit()
    return "successfully deleted"




@router.put("/slot{id}",status_code=status.HTTP_202_ACCEPTED)
async def update_slot(id:int,user:schemas.update_slot,db: Session = Depends(get_db) ,current_user : str = Depends(oauth2.get_current_admin)):
    bay_q = db.query(models.slots).filter(models.slots.id== id)
    bay=bay_q.first()

    if id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="slot not found")

    bay_q.update(user.dict(),synchronize_session= False)
    db.commit()

    return user