from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/products",
    tags=['products'])


@router.post("/admin", status_code=status.HTTP_201_CREATED)
async def pcreate(data: schemas.product, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_admin)):

    new_product = models.products(**data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get('/admin')
def get_products(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_admin)):
    products = db.query(models.products).all()

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"product not found")

    return products


@router.get('/admin{product}')
def get_product(product: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_admin)):
    product = db.query(models.products.id).filter(
        models.products.product == product).all()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{product} not found")

    return product


@router.delete("/admin{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_admin)):
    product_q = db.query(models.products).filter(models.products.id == id)
    product = product_q.first()

    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    product_q.delete(synchronize_session=False)
    db.commit()
    return "successfully deleted"


@router.put("/admin{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_product(id: int, payload: schemas.product, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_admin)):
    product_q = db.query(models.products).filter(models.products.id == id)
    product = product_q.first()

    if id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="product not found")

    product_q.update(payload.dict(), synchronize_session=False)
    db.commit()

    return product_q.first()


@router.post("/subadmin", status_code=status.HTTP_201_CREATED)
async def pcreate(data: schemas.product, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_subadmin)):

    new_product = models.products(**data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get('/subadmin')
def get_products(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_subadmin)):
    products = db.query(models.products).all()

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"product not found")

    return products


@router.get('/subadmin{product}')
def get_product(product: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_subadmin)):
    product = db.query(models.products.id).filter(
        models.products.product == product).all()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{product} not found")

    return product


@router.delete("/subadmin{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_subadmin)):
    product_q = db.query(models.products).filter(models.products.id == id)
    product = product_q.first()

    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    product_q.delete(synchronize_session=False)
    db.commit()
    return "successfully deleted"


@router.put("/subadmin{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_product(id: int, payload: schemas.product, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_subadmin)):
    product_q = db.query(models.products).filter(models.products.id == id)
    product = product_q.first()
    print(payload)
    if id == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="product not found")

    product_q.update(payload.dict(), synchronize_session=False)
    db.commit()

    return product_q.first()
