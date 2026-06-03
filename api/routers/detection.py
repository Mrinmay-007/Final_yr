


from fastapi import FastAPI, UploadFile, File, APIRouter
from ultralytics import YOLO
import shutil
import os
import numpy as np
import tensorflow as tf
from PIL import Image

router = APIRouter()

# Load YOLO models
model = YOLO(r"D:\USER\OneDrive\Desktop\Final_yr\models\yolo\best.pt")
model2 = YOLO(r"D:\USER\OneDrive\Desktop\Final_yr\models\yolo\best2.pt")

# Load Keras/TensorFlow model
CLASS_NAMES = ["Not Potato", "Potato"]
your_path = r"D:\USER\OneDrive\Desktop\Final_yr\models\\"
MODEL_PATH = your_path + "detect_V2.keras"

if MODEL_PATH.endswith(".keras") or MODEL_PATH.endswith(".h5"):
    MODEL = tf.keras.models.load_model(MODEL_PATH)  # type: ignore
else:
    MODEL = tf.keras.layers.TFSMLayer(MODEL_PATH, call_endpoint="serving_default")  # type: ignore


def preprocess_image(img_path, target_size=(224, 224)):
    """Load and preprocess image for Keras model"""
    img = Image.open(img_path).convert("RGB")
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0  # normalize
    img_array = np.expand_dims(img_array, axis=0)  # add batch dimension
    return img_array


@router.post("/detect")
async def detect(file: UploadFile = File(...)):
    # Save uploaded image temporarily
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run YOLO predictions
    results = model.predict(temp_file)
    results2 = model2.predict(temp_file)

    # Preprocess and run TensorFlow model prediction
    img_array = preprocess_image(temp_file, target_size=(224, 224))
    results3 = MODEL.predict(img_array)

    # Clean up temp file
    os.remove(temp_file)


# YOLOv8 Model 1
    pred_class = results[0].names[results[0].probs.top1]
    conf1 = float(results[0].probs.top1conf) 
    is_potato1 = pred_class.lower() == "potato"
    confidence1 = conf1 #if is_potato1 else 0.0

    # YOLOv8 Model 2
    pred_class2 = results2[0].names[results2[0].probs.top1]
    conf2 = float(results2[0].probs.top1conf) 
    is_potato2 = pred_class2.lower() == "potato"
    confidence2 = conf2 #if is_potato2 else 0.0

    # TensorFlow Model
    pred_class3 = CLASS_NAMES[np.argmax(results3[0])]
    conf3 = float(np.max(results3[0])) 
    is_potato3 = pred_class3.lower() == "potato"
    confidence3 = conf3 #if is_potato3 else 0.0

    # Majority Voting
    votes = [is_potato1, is_potato2, is_potato3]
    final_decision = "Potato" if votes.count(True) >= 2 else "Not Potato"

    return {
        # "YOLOv8 Model 1": {
        #     "class": pred_class,
        #     "is_potato": is_potato1,
        #     "confidence": round(confidence1, 3)
        # },
        # "YOLOv8 Model 2": {
        #     "class": pred_class2,
        #     "is_potato": is_potato2,
        #     "confidence": round(confidence2, 3)
        # },
        # "Keras Model": {
        #     "class": pred_class3,
        #     "is_potato": is_potato3,
        #     "confidence": round(confidence3, 3)
        # },
        
        "final_decision": final_decision
    }