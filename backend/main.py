from fastapi import FastAPI
from routes import tasks

app = FastAPI(title="Evolution-of-Todo Phase II")

app.include_router(tasks.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Backend is running"}
