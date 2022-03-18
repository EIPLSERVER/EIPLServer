from concurrent.futures.process import _python_exit
from fastapi import  Depends, FastAPI,Response,status,HTTPException,Depends,APIRouter
from pip import List
from sqlalchemy.orm  import Session
from .. import models, schemas , utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix= "/clients",
    tags=['clients'])

@router.post("/admin",status_code=status.HTTP_201_CREATED)
async def client_create(data:schemas.client,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_admin)):

    new_client = models.clients(**data.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return  new_client

@router.get('/admin')
def get_clients(db: Session = Depends(get_db), current_admin : int = Depends(oauth2.get_current_admin)):
    clients= db.query(models.clients).all()

    if not clients:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"No clients found")

    return clients

@router.get('/admin{client}')
def get_client(client:str,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_admin)):
    client= db.query(models.clients.id).filter(models.clients.client== client).all()

    if not client:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"{client} not found")

    return client

@router.delete("/admin{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(id:str ,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_admin)):
    client_q = db.query(models.clients).filter(models.clients.id == id)
    product=client_q.first()

    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="not found")
    client_q.delete(synchronize_session= False)
    db.commit()
    return "successfully deleted"


@router.put("/admin{id}",status_code=status.HTTP_202_ACCEPTED)
async def update_client(id:int,payload:schemas.client,db: Session = Depends(get_db) ,current_user : str = Depends(oauth2.get_current_admin)):
    client_q = db.query(models.clients).filter(models.clients.id == id)
    client=client_q.first()

    if id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="client not found")

    client_q.update(payload.dict(),synchronize_session= False)
    db.commit()


    return client_q.first()



#subadmins

@router.post("/subadmin",status_code=status.HTTP_201_CREATED)
async def client_create(data:schemas.client,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_subadmin)):

    new_client = models.clients(**data.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return  new_client

@router.get('/subadmin')
def get_clients(db: Session = Depends(get_db), current_admin : int = Depends(oauth2.get_current_subadmin)):
    clients= db.query(models.clients).all()

    if not clients:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"No clients found")

    return clients

@router.get('/subadmin{client}')
def get_client(client:str,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_subadmin)):
    client= db.query(models.clients.id).filter(models.clients.client== client).all()

    if not client:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"{client} not found")

    return client

@router.delete("/subadmin{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(id:str ,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_subadmin)):
    client_q = db.query(models.clients).filter(models.clients.id == id)
    product=client_q.first()

    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="not found")
    client_q.delete(synchronize_session= False)
    db.commit()
    return "successfully deleted"


@router.put("/subadmin{id}",status_code=status.HTTP_202_ACCEPTED)
async def update_client(id:int,payload:schemas.client,db: Session = Depends(get_db) ,current_user : str = Depends(oauth2.get_current_subadmin)):
    client_q = db.query(models.clients).filter(models.clients.id == id)
    client=client_q.first()

    if id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="client not found")

    client_q.update(payload.dict(),synchronize_session= False)
    db.commit()


    return client_q.first()