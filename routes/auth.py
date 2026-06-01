from core import security
import collections
from datetime import time
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User 
from schemas.user import UserCreate,UserResponse,LoginRequest,UserUpdate
from core.security import hash_password, verify_password  
# pyrefly: ignore [missing-import]
from fastapi.security import OAuth2PasswordBearer
# pyrefly: ignore [missing-import]
from jose import jwt
from datetime import datetime,timedelta,timezone
from fastapi.security import OAuth2PasswordRequestForm


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=30)

    to_encode.update({"exp":expire})

    encoded_token=jwt.encode (
       to_encode,
       SECRET_KEY,
       algorithm=ALGORITHM
    )
    return encoded_token
    
router=APIRouter(
    prefix="/auth",
    tags=["Auth"]
)
from fastapi.security import OAuth2PasswordBearer
# from fastapi import Depends, HTTPException
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)
def verify_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return email

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    return verify_token(token)

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
# def login(user:LoginRequest,db: Session = Depends(get_db)):
#     db_user=db.query(User).filter(user.email==User.email).first()
#     if not db_user:
#         raise HTTPException(status_code=401,detail="Invalid Credential")
#     elif not verify_password(user.password,db_user.password):
#         raise HTTPException(status_code=401,detail="Invalid Credential")
#     else:
#         token=create_access_token({
#             "sub":db_user.email
#         })
#         return{
#             "access_token":token,
#             "token_type":"bearer"
#         }
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )

    if not verify_password(
        form_data.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_access_token(
        {"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }