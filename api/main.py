

from fastapi import FastAPI  #type: ignore
from fastapi.middleware.cors import CORSMiddleware #type: ignore
import uvicorn #type: ignore
import os

# ============================
from .db import connect_to_mongo, close_mongo_connection
from api.routers import prediction,detection,logbook,weather,lang
# ============================
app = FastAPI()

# Allow CORS (if you want to call the API from a frontend React/JS app)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Change to your frontend domain in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
#  Database Connection
# ======================


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()
    
# ======================
#  API Router
# ======================
 
app.include_router(prediction.router)
app.include_router(detection.router)
# app.include_router(detect_yolo.router)
app.include_router(logbook.router)
app.include_router(weather.router)
app.include_router(lang.router)
# ======================
# Main
# ======================

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
