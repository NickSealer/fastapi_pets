from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas, database, models
from app.utils import auth

router = APIRouter(prefix='', tags=['auth'])

@router.post('/login', response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
  user = auth.authenticate_user(form_data.username, form_data.password, db)
  if not user:
    raise HTTPException(status_code=400, detail='Invalid username or password')
  
  access_token = auth.create_access_token(payload={'username': user.username})
  return {'access_token': access_token, 'token_type': 'bearer'}

@router.get('/me', response_model=schemas.UserResponse)
def who_am_i(current_user: models.User = Depends(auth.current_user)):
  """
  Example, to require auth in some EP.\n
  This ins importan as argument in your EP:\n
  current_user: models.User = Depends(auth.current_user)
  """
  return current_user