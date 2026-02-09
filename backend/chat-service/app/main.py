from fastapi import FastAPI
from app.db.db import Base, engine
from app.models.models import Consultant,Conversation,Message
from app.api.routes import router as chat_router
app = FastAPI(
    title="Loan Chatting Service",
    description="Modern microservice-based banking application",
    version="1.0.0",
)
from app.api.websockets import ws_router

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:  
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def health():
    return {"status": "Chatting service of banking application is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
app.include_router(chat_router)
app.include_router(ws_router)