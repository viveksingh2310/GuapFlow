from fastapi import FastAPI
from app.db.db import Base, engine
from app.api.routes import router as user_router
from app.models.models import User

app = FastAPI(
    title="User Server",
    description="Modern microservice-based banking application",
    version="1.0.0",
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:  
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def health():
    return {"status": "User service of banking application is running"}

app.include_router(user_router)