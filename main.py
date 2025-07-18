from fastapi import FastAPI
from app import models

app = FastAPI()

@app.get('/')
def root():
  return {'message': 'API OK!!!!'}
