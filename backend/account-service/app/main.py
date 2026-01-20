from fastapi import FastAPI
from app.db.db import Base, engine
from app.models.models import Account
from app.api.routes import router as account_router

app = FastAPI(
    title="Accounts Service",
    description="Modern microservice-based banking application",
    version="1.0.0",
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:  
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def health():
    return {"status": "Accounts service of banking application is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
app.include_router(account_router)