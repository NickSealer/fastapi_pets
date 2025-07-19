from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.utils import secure_password

router = APIRouter(prefix='/users', tags=['users'])

@router.get('/', response_model=List[schemas.UserResponse], status_code=200)
def users(db: Session = Depends(get_db)):
  return db.query(models.User).all()

@router.get('/{id}', response_model=schemas.UserResponse, status_code=200)
def user(id: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
    raise HTTPException(status_code=404, detail='User not found')

  return user

@router.post('/', response_model=schemas.UserResponse, status_code=201)
def create(user: schemas.CreateUser, db: Session = Depends(get_db)):  
  new_user = models.User(
    username = user.username,
    email = user.email,
    birthdate = user.birthdate,
    password = secure_password.hash_password(user.password)
  )
  
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  
  return new_user