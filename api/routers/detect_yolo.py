from fastapi import FastAPI, UploadFile, File,APIRouter
from ultralytics import YOLO
import shutil
import os

router = APIRouter()

# Load your trained YOLO classification model
# your_path = "D:\\USER\\OneDrive\\Desktop\\Final_yr\\models\\"


model = YOLO(r"D:\USER\OneDrive\Desktop\Final_yr\models\yolo\best.pt")

@router.post("/detect_yolo/")
async def predict(file: UploadFile = File(...)):
    # Save uploaded image temporarily
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run prediction
    results = model.predict(temp_file)

    # Clean up temp file
    os.remove(temp_file)

    # Parse result
    pred_class = results[0].names[results[0].probs.top1]   # best class name
    confidence = float(results[0].probs.top1conf)          # confidence

    # Decide Potato / Not Potato
    is_potato = (pred_class.lower() == "potato")

    return {
        "class": pred_class,
        "confidence": round(confidence, 3),
        "is_potato": is_potato
    }

