
from fastapi import APIRouter, File, UploadFile #type: ignore

import numpy as np
from io import BytesIO
from PIL import Image  #type: ignore
import tensorflow as tf  #type: ignore
import os
import cv2

router = APIRouter()


# Path to your model (use .keras or .h5 format)
your_path = "D:\\USER\\OneDrive\\Desktop\\Final_yr\\models\\"
MODEL_PATH= your_path + "V1.keras" # Update this path

# Load the model depending on extension
if MODEL_PATH.endswith(".keras") or MODEL_PATH.endswith(".h5"):
    MODEL = tf.keras.models.load_model(MODEL_PATH) #type:ignore
else:
    # Fallback for TensorFlow SavedModel directory
    MODEL = tf.keras.layers.TFSMLayer(MODEL_PATH, call_endpoint="serving_default") #type:ignore

# Class names
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]





@router.get("/ping")
async def ping():
    return {"message": "Hello, World!"}


def read_file_as_image(data) -> np.ndarray:
    """Convert uploaded image bytes into a numpy array"""
    image = Image.open(BytesIO(data)).convert("RGB")
    image = image.resize((256, 256))  # resize if your model expects fixed size
    return np.array(image)




def get_severity_from_bytes(image_bytes: bytes) -> tuple[str, float]:
    """
    Rule-based severity detection (in-memory, background removed).
    Returns severity category and infected ratio.
    """
    # Decode image
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #type:ignore

    # ✅ Leaf segmentation (green range to remove background/shadows)
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([85, 255, 255])
    leaf_mask = cv2.inRange(hsv, lower_green, upper_green)

    # ✅ Disease segmentation (dark/brown/black)
    lower_disease = np.array([0, 0, 0])
    upper_disease = np.array([180, 255, 80])
    disease_mask = cv2.inRange(hsv, lower_disease, upper_disease)

    # ✅ Infected area = disease ∩ leaf
    infected_mask = cv2.bitwise_and(disease_mask, leaf_mask)

    infected_area = np.count_nonzero(infected_mask)
    total_leaf_area = np.count_nonzero(leaf_mask)

    ratio = (infected_area / total_leaf_area * 100) if total_leaf_area > 0 else 0

    # ✅ Categorize severity
    if ratio < 10:
        severity = "Mild"
    elif ratio < 30:
        severity = "Moderate"
    else:
        severity = "Severe"

    return severity, ratio


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read file bytes once (efficient)
    file_bytes = await file.read()

    # Convert for model input
    image = read_file_as_image(file_bytes)  # assumes you already have this function
    img_batch = np.expand_dims(image, 0)

    # Run classification
    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = float(np.max(predictions[0]))

    # Severity check (only if diseased)
    severity, ratio = ("N/A", 0.0)
    if predicted_class != "Healthy":
        severity, ratio = get_severity_from_bytes(file_bytes)

    return {
        "class": predicted_class,
        "confidence": confidence,
        "severity": severity,
        "infected_ratio": round(ratio, 2)  # return % infected
    }
