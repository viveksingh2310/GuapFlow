from fastapi import FastAPI
from app.db.db import engine,Base
from app.api.routes import router as transaction_router

app=FastAPI(
    title="Transaction Service",
     description="Modern microservice-based banking application",
    version="1.0.0",
)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:  
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def health():
    return {"status": "Transaction services of banking application is running fine.."}

app.include_router(transaction_router)