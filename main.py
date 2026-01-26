from fastapi import FastAPI
from routes import tasks, auth
from db import engine, Base

app = FastAPI(title="Evolution-of-Todo Phase II")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(tasks.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Backend is running"}
