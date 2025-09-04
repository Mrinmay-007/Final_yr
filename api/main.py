

from fastapi import FastAPI  #type: ignore
from fastapi.middleware.cors import CORSMiddleware #type: ignore
import uvicorn #type: ignore
import os

from api.routers import prediction

app = FastAPI()

# Allow CORS (if you want to call the API from a frontend React/JS app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
#  API Router
# ======================


app.include_router(prediction.router)

# ======================
# Main
# ======================

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
