from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import tasks  # your tasks router

app = FastAPI(title="Hackathon Task App")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for hackathon simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Hackathon Task App Running!"}
