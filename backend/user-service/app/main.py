from fastapi import FastAPI

app = FastAPI(
    title="GuapFlow Banking Application",
    description="Modern microservice-based banking application",
    version="1.0.0",
)

@app.get("/")
def health():
    return {"status": "User service of banking application is running"}
