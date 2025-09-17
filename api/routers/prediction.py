
from fastapi import APIRouter, File, UploadFile #type: ignore

import numpy as np
from io import BytesIO
from PIL import Image  #type: ignore
import tensorflow as tf  #type: ignore


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


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read the uploaded image
    image = read_file_as_image(await file.read())

    # Expand dimensions to create batch of size 1
    img_batch = np.expand_dims(image, 0)

    # Run prediction
    predictions = MODEL.predict(img_batch)

    # Get class & confidence
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = float(np.max(predictions[0]))

    return {
        "class": predicted_class,
        "confidence": confidence
    }

