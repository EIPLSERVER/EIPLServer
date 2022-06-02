
from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/clients_products",
    tags=['clients_products'])


@router.post("/admin", status_code=status.HTTP_201_CREATED)
async def bay(user: schemas.clients_products, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_admin)):

    new_user = models.clients_products(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete("/admin{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bay(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_admin)):
    bay = db.query(models.clients_products).filter(
        models.clients_products.id == id)
    bay_q = bay.first()

    if bay == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    bay.delete(synchronize_session=False)
    db.commit()
    return "Bay successfully deleted"


@router.get("/admin")
def get_bay(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_admin)):
    bay = db.query(models.clients_products).all()

    if not bay:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No Bays found")

    return bay


@router.put("/admin{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_bay(id: int, user: schemas.clients_products, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_admin)):
    bay_q = db.query(models.clients_products).filter(
        models.clients_products.id == id)
    bay = bay_q.first()

    if bay_q == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")

    bay_q.update(user.dict(), synchronize_session=False)
    db.commit()

    return user


@router.post("/subadmin", status_code=status.HTTP_201_CREATED)
async def bay(user: schemas.clients_products, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_subadmin)):

    new_user = models.clients_products(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete("/subadmin{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bay(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_subadmin)):
    bay = db.query(models.clients_products).filter(
        models.clients_products.id == id)
    bay_q = bay.first()

    if bay == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    bay.delete(synchronize_session=False)
    db.commit()
    return "Bay successfully deleted"


@router.get("/subadmin")
def get_bay(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_subadmin)):
    bay = db.query(models.clients_products).all()

    if not bay:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No Bays found")

    return bay


@router.put("/subadmin{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_bay(id: int, user: schemas.clients_products, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_subadmin)):
    bay_q = db.query(models.clients_products).filter(
        models.clients_products.id == id)
    bay = bay_q.first()

    if bay_q == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")

    bay_q.update(user.dict(), synchronize_session=False)
    db.commit()

    return user


@router.get('/admin{client}')
def get_clients_products(client: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_admin)):
    client = db.query(models.clients.id).filter(
        models.clients.client == client).first()
    print(client.id)
    products_id = db.query(models.clients_products.product_id).filter(
        models.clients_products.client_id == client.id).all()
    print(products_id)
    # products = db.query(models.products.product).filter(models.clients_products.product_id == products_id.id).all()
    # print(products)

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{client} not found")

    return products_id
