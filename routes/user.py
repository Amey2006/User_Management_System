from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User 
from schemas.user import UserResponse,UserUpdate
from core.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


    
@router.get("/view_users",response_model=list[UserResponse])
def view_user(db:Session=Depends(get_db)):
    all=db.query(User).all()
    return all


@router.get("/{id}",response_model=UserResponse)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user

@router.delete("/remove/{id}")
def remove_user(id:int,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=404,detail="ID not found")
    db.delete(user)
    db.commit()
    return{
        "msg":"User Deleted Successfully...."
    }

@router.put("/{id}",response_model=UserResponse)
def update_user(id:int,user:UserUpdate,db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.id==id).first()
    if not db_user:
        raise HTTPException(status_code=404,detail="User not found")
    db_user.email=user.email
    db_user.password=hash_password(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user
    

    

    