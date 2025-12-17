from fastapi import FastAPI

app = FastAPI(
    title="GuapFlow Banking Application",
    description="This is a full-fledged banking application based on modern microservice architecture",
    version="1.0.0",
)

@app.get("/")
def health_check():
    return {"status": "User service running"}
