from concurrent.futures.process import _python_exit
from fastapi import  Depends, FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm  import Session
from .. import models, schemas , utils, oauth2
from ..database import get_db
import calendar
import datetime

router = APIRouter(
    prefix= "/admin",
    tags=['Admin'])

@router.post("/acreate",status_code=status.HTTP_201_CREATED, response_model= schemas.createreturn)
async def acreate(user:schemas.acreate ,db: Session = Depends(get_db)):
    #hast the password - user.password
    
    hasdhed_password = utils.hash(user.password)
    user.password = hasdhed_password

    new_user = models.admin(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user


@router.post("/screate",status_code=status.HTTP_201_CREATED, response_model= schemas.createreturn)
async def sacreate(user:schemas.sacreate ,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_admin)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.subadmin(created_by = current_user.id,**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user

@router.get('/subadmins')
def get_subadmins(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_admin)):
    user= db.query(models.subadmin).all()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"subadmin not found")

    return user

@router.get('/subadmin{phone}',response_model= schemas.get_subadmin)
def get_subadmins(phone:int,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_admin)):
    user= db.query(models.subadmin).filter(models.subadmin.phone== phone).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"subadmin with phone: {phone} not found")

    return user

@router.delete("/sdelete",status_code=status.HTTP_204_NO_CONTENT)
async def sadelete(phone:int ,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_admin)):
    post_q = db.query(models.subadmin).filter(models.subadmin.phone == phone)
    post=post_q.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="not found")
    post_q.delete(synchronize_session= False)
    db.commit()
    return "successfully deleted"

@router.post("/ucreate",status_code=status.HTTP_201_CREATED, response_model= schemas.createreturn)
async def ucreate(user:schemas.ucreate ,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_admin)):
    #hast the password - user.password
    
    hasdhed_password = utils.hash(user.password)
    user.password = hasdhed_password

    new_user = models.user(created_by = current_user.id,**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user

@router.get('/users')
def get_user(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_admin)):
    user= db.query(models.user).all()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"No users found")

    return user

@router.get('/user{phone}', response_model = schemas.get_user)
def get_user(phone:int,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_admin)):
    user= db.query(models.user).filter(models.user.phone== phone).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"user with id: {phone} not found")

    return user

@router.delete("/udelete",status_code=status.HTTP_204_NO_CONTENT)
async def udelete(phone:int ,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_admin)):
    post_q = db.query(models.user).filter(models.user.phone == phone)
    post=post_q.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="not found")
    post_q.delete(synchronize_session= False)
    db.commit()
    return "successfully deleted"






@router.post("/slot_60create",status_code=status.HTTP_201_CREATED, response_model= schemas.slot_60)
async def slot_60create(slot:schemas.slot_60 ,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_admin)):

    new_slot = models.slot_60(**slot.dict())#created_by = current_user.id,**user.dict())
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    return  new_slot

@router.post("/slot_30create",status_code=status.HTTP_201_CREATED, response_model= schemas.slot_30)
async def slot_30create(slot:schemas.slot_30 ,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_admin)):

    new_slot = models.slot_30(**slot.dict())#created_by = current_user.id,**user.dict())
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    return  new_slot

@router.get('/slots_60')
def get_slots_60(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_admin)):
    user= db.query(models.slot_60).all()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"No slots found")

    return user

@router.get('/slots_30')
def get_slots_30(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_admin)):
    user= db.query(models.slot_30).all()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"No slots found")

    return user


@router.post("/month_create",status_code=status.HTTP_201_CREATED, response_model= schemas.month)
async def month_create(slot:schemas.month ,db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_admin)):

    new_slot = models.month(**slot.dict())#created_by = current_user.id,**user.dict())
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    return  new_slot

@router.get('/month')
def month(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_admin)):
    user= db.query(models.month).all()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"No dates found")

    return user

@router.post("/days_10",status_code=status.HTTP_201_CREATED)
async def days_10(db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_admin)):

    new_slot = db.query(models.month.date,models.bay.id,models.slot_30.slot).filter(models.bay.product_id == 1,models.month.working == True).order_by(models.month.date).all()
    new_slot = new_slot + db.query(models.month.date,models.bay.id,models.slot_60.slot).filter(models.bay.product_id != 1,models.month.working == True).order_by(models.month.date).all()
    
    n = len(new_slot)
    test_keys = ['date','bay_id','slot']
    res = dict(zip(test_keys, new_slot[0]))
    for i in range(n):
        res = dict(zip(test_keys, new_slot[i]))
        new_user = models.days_10(**res)
        db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return  new_slot

@router.get("/month_create",status_code=status.HTTP_201_CREATED)
async def month_create(db: Session = Depends(get_db) ,current_user : int = Depends(oauth2.get_current_admin)):
    today = datetime.date.today()
    print(today.month)
    print("Today's date:", today)

    my_cal= calendar.Calendar()
    year = today.year
    month = today.month
    dates = list(my_cal.itermonthdays3(year,month))
    my_dates=[]
    for i in dates:
        if i[1] == month:
            my_dates.append(i)
    keys = ["date","working","E"]
    for j in my_dates:
        res = dict(zip(keys, [str(datetime.date(*j)),True,False]))
        print(res)
        new_user = models.month(**res)
        db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return  new_user