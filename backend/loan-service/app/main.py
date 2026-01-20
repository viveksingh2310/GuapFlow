from fastapi import FastAPI
from app.db.db import Base, engine
from app.models.models import Loan
from app.api.routes import router as loan_router

app = FastAPI(
    title="Loans Service",
    description="Modern microservice-based banking application",
    version="1.0.0",
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:  
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def health():
    return {"status": "Loans service of banking application is running"}

app.include_router(loan_router)