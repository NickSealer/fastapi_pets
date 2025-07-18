from fastapi import FastAPI
from app import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.get('/')
def root():
  return {'message': 'API OK!!!!'}
