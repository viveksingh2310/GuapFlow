from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import database_models

#START UP COMMAND =>  py -m uvicorn main:app --reload
#db confg
database_url="postgresql+psycopg2://postgres:vivek@localhost:5432/guapflow"
engine= create_engine(database_url)
SessionLocal =sessionmaker(autoflush=False, autocommit=False,bind=engine)
database_models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Simple Banking API",
    description="A basic API for banking operations",
    version="0.1.0",
)

@app.get('/isDBconnected')
def isDBconnected():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@app.get("/")
def read_root():
    """Welcome endpoint"""
    return {"message": "Welcome to the Simple Banking API"}