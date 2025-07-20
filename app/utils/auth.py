from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app import models, database
from decouple import config as env_config

SECRET_KEY = env_config('SECRET_KEY')
ALGORITHM = env_config('ALGORITHM')
ACCESS_TOKEN_EXPIRATION = int(env_config('ACCESS_TOKEN_EXPIRATION'))

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
bearer_scheme = HTTPBearer()

def verify_password(plain_password, hashed_password):
  return password_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str, db: Session = Depends(database.get_db)):
  user = db.query(models.User).filter(models.User.username == username).first()
  if not user or not verify_password(password, user.password):
    return None
  
  return user

def create_access_token(payload: dict):
  payload.update({'exp': datetime.now().astimezone() + (timedelta(minutes=ACCESS_TOKEN_EXPIRATION))})
  return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(database.get_db)):
  credentials_exception  = HTTPException( status_code=401, detail='Invalid credentials', headers={"WWW-Authenticate": "Bearer"})
  
  try:
    result = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=ALGORITHM)
    username: str = result.get('username')
    if not username:
      raise credentials_exception
  except JWTError:
    raise credentials_exception
  
  user = db.query(models.User).filter(models.User.username == username).first()
  if not user:
    raise credentials_exception
  
  return user
