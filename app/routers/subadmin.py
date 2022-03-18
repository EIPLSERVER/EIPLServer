from concurrent.futures.process import _python_exit
from fastapi import  Depends, FastAPI,Response,status,HTTPException,Depends,APIRouter
from pydantic import PathNotExistsError
from sqlalchemy.orm  import Session
from .. import models, schemas , utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix= "/subadmin",
    tags=['SubAdmin'])

@router.post("/ucreate",status_code=status.HTTP_201_CREATED)
async def ucreate(user:schemas.ucreate ,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_subadmin)):
    #hast the password - user.password
    
    hasdhed_password = utils.hash(user.password)
    user.password = hasdhed_password

    new_user = models.user(created_by = current_user.id,**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user

@router.delete("/udelete",status_code=status.HTTP_204_NO_CONTENT)
async def udelete(phone:int ,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_subadmin)):
    post_q = db.query(models.user).filter(models.user.phone == phone)
    post=post_q.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="not found")
    post_q.delete(synchronize_session= False)
    db.commit()
    return "successfully deleted"

@router.get('/user{phone}')
def get_user(phone:int,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_subadmin)):
    user= db.query(models.user).filter(models.user.phone== phone).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"user with id: {phone} not found")

    return user

@router.get('/users')
def get_user(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_subadmin)):
    user= db.query(models.user).all()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"No users found")

    return user

