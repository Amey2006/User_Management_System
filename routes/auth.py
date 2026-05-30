from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User 
from schemas.user import UserCreate,UserResponse,LoginRequest,UserUpdate
from core.security import hash_password, verify_password  

router=APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user=db.query(User).filter(User.email==user.email).first()   
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user=User(
        email=user.email,
        password=hash_password(user.password)   
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
@router.post("/login")
def login(user:LoginRequest,db: Session = Depends(get_db)):
    db_user=db.query(User).filter(user.email==User.email).first()
    if not db_user:
        raise HTTPException(status_code=401,detail="Invalid Credential")
    elif not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=401,detail="Invalid Credential")
    else:
        return {"message":"Login Sucessfully"}