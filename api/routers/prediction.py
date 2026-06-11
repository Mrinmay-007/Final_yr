
# # from fastapi import APIRouter, File, UploadFile #type: ignore

# # import numpy as np
# # from io import BytesIO
# # from PIL import Image  #type: ignore
# # import tensorflow as tf  #type: ignore
# # import os
# # import cv2

# # router = APIRouter(
# #     prefix="/predict",
# #     tags=["Disease Prediction"]
# # )


# # # Path to your model (use .keras or .h5 format)
# # your_path = "D:\\USER\\OneDrive\\Desktop\\Final_yr\\api\\ml_models\\"
# # MODEL_PATH= your_path + "V1.keras" # Update this path

# # # Load the model depending on extension
# # if MODEL_PATH.endswith(".keras") or MODEL_PATH.endswith(".h5"):
# #     MODEL = tf.keras.models.load_model(MODEL_PATH) #type:ignore
# # else:
# #     # Fallback for TensorFlow SavedModel directory
# #     MODEL = tf.keras.layers.TFSMLayer(MODEL_PATH, call_endpoint="serving_default") #type:ignore



# from fastapi import APIRouter, File, UploadFile
# import numpy as np
# from io import BytesIO
# from PIL import Image
# import tensorflow as tf
# import os
# import cv2

# router = APIRouter(
#     prefix="/predict",
#     tags=["Disease Prediction"]
# )

# # --------------------------------------------------
# # Model Path
# # --------------------------------------------------

# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# # routers -> api
# API_DIR = os.path.dirname(CURRENT_DIR)

# # api -> project root
# PROJECT_ROOT = os.path.dirname(API_DIR)

# MODEL_PATH = os.path.join(PROJECT_ROOT, "ml_models", "V1.keras")

# print("MODEL_PATH =", MODEL_PATH)

# if not os.path.isfile(MODEL_PATH):
#     raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

# # --------------------------------------------------
# # Load Model
# # --------------------------------------------------

# MODEL = tf.keras.models.load_model(MODEL_PATH)

# CLASS_NAMES = [
#     "Early Blight",
#     "Late Blight",
#     "Healthy"
# ]

# # --------------------------------------------------
# # Health Check
# # --------------------------------------------------
# @router.get("/ping")
# async def ping():
#     return {"message": "Hello World"}

# # --------------------------------------------------
# # Image Processing
# # --------------------------------------------------
# def read_file_as_image(data: bytes) -> np.ndarray:
#     """Convert uploaded image bytes into a numpy array"""
#     image = Image.open(BytesIO(data)).convert("RGB")
#     image = image.resize((256, 256))
#     return np.array(image)

# # --------------------------------------------------
# # Severity Detection
# # --------------------------------------------------
# def get_severity_from_bytes(image_bytes: bytes):
#     """
#      Rule-based severity detection (in-memory, background removed).
#      Returns severity category and infected ratio.
#     """
#     # Decode image
#     np_arr = np.frombuffer(image_bytes, np.uint8)
#     img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
#     if img is None:
#         return "Unknown", 0.0
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
#     # ✅ Leaf segmentation (green range to remove background/shadows)
#     lower_green = np.array([25, 40, 40])
#     upper_green = np.array([85, 255, 255])

#     leaf_mask = cv2.inRange(
#         hsv,
#         lower_green,
#         upper_green
#     )
    
#     # ✅ Disease segmentation (dark/brown/black)
#     lower_disease = np.array([0, 0, 0])
#     upper_disease = np.array([180, 255, 80])

#     disease_mask = cv2.inRange(
#         hsv,
#         lower_disease,
#         upper_disease
#     )
    
#     # ✅ Infected area calculation Infected area = disease ∩ leaf
#     infected_mask = cv2.bitwise_and(
#         disease_mask,
#         leaf_mask
#     )

#     infected_area = np.count_nonzero(infected_mask)
#     total_leaf_area = np.count_nonzero(leaf_mask)

#     ratio = (
#         infected_area / total_leaf_area * 100
#         if total_leaf_area > 0
#         else 0
#     )
    
#     # ✅ Categorize severity
#     if ratio < 10:
#         severity = "Mild"
#     elif ratio < 30:
#         severity = "Moderate"
#     else:
#         severity = "Severe"

#     return severity, ratio

# # --------------------------------------------------
# # Prediction Endpoint
# # --------------------------------------------------
# @router.post("/")
# async def predict(file: UploadFile = File(...)):

#     file_bytes = await file.read()
#     # Convert for model input
#     image = read_file_as_image(file_bytes)
#     img_batch = np.expand_dims(image, axis=0)
    
#     # Run classification
#     predictions = MODEL.predict(img_batch)
#     predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
#     confidence = float(np.max(predictions[0]))
    
#     # Severity check (only if diseased)
#     severity = "N/A"
#     ratio = 0.0

#     if predicted_class != "Healthy":
#         severity, ratio = get_severity_from_bytes(file_bytes)

#     return {
#         "class": predicted_class,
#         "confidence": round(confidence * 100, 2),
#         "severity": severity,
#         "infected_ratio": round(ratio, 2)
#     }

# # # --------------------------------------------------

# from fastapi import APIRouter, File, UploadFile
# import numpy as np
# from io import BytesIO
# from PIL import Image
# import tensorflow as tf
# import os
# import cv2
# import time

# router = APIRouter(
#     prefix="/predict",
#     tags=["Disease Prediction"]
# )

# # --------------------------------------------------
# # Model Path
# # --------------------------------------------------

# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# API_DIR = os.path.dirname(CURRENT_DIR)
# PROJECT_ROOT = os.path.dirname(API_DIR)

# MODEL_PATH = os.path.join(PROJECT_ROOT, "ml_models", "V1.keras")

# print("MODEL_PATH =", MODEL_PATH)

# if not os.path.isfile(MODEL_PATH):
#     raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

# # --------------------------------------------------
# # Load Model
# # --------------------------------------------------

# # ✅ FIX 1: Added compile=False to skip optimizer state loading (fixes crash-loop warning)
# print("Starting model load...")
# start = time.time()
# MODEL = tf.keras.models.load_model(MODEL_PATH, compile=False)
# print(f"Model loaded successfully in {time.time() - start:.2f}s")


# import psutil
# print(f"Available RAM: {psutil.virtual_memory().available / 1e9:.2f} GB")

# CLASS_NAMES = [
#     "Early Blight",
#     "Late Blight",
#     "Healthy"
# ]

# # --------------------------------------------------
# # Health Check
# # --------------------------------------------------
# @router.get("/ping")
# async def ping():
#     return {"message":f"Model loaded successfully in {time.time() - start:.2f}s"}



# # --------------------------------------------------
# # Image Processing
# # --------------------------------------------------
# def read_file_as_image(data: bytes) -> np.ndarray:
#     """Convert uploaded image bytes into a numpy array"""
#     image = Image.open(BytesIO(data)).convert("RGB")
#     image = image.resize((256, 256))
#     return np.array(image)

# # --------------------------------------------------
# # Severity Detection
# # --------------------------------------------------
# def get_severity_from_bytes(image_bytes: bytes):
#     """
#     Rule-based severity detection (in-memory, background removed).
#     Returns severity category and infected ratio.
#     """
#     np_arr = np.frombuffer(image_bytes, np.uint8)
#     img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
#     if img is None:
#         return "Unknown", 0.0
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#     lower_green = np.array([25, 40, 40])
#     upper_green = np.array([85, 255, 255])
#     leaf_mask = cv2.inRange(hsv, lower_green, upper_green)

#     lower_disease = np.array([0, 0, 0])
#     upper_disease = np.array([180, 255, 80])
#     disease_mask = cv2.inRange(hsv, lower_disease, upper_disease)

#     infected_mask = cv2.bitwise_and(disease_mask, leaf_mask)

#     infected_area = np.count_nonzero(infected_mask)
#     total_leaf_area = np.count_nonzero(leaf_mask)

#     ratio = (
#         infected_area / total_leaf_area * 100
#         if total_leaf_area > 0
#         else 0
#     )

#     if ratio < 10:
#         severity = "Mild"
#     elif ratio < 30:
#         severity = "Moderate"
#     else:
#         severity = "Severe"

#     return severity, ratio

# # --------------------------------------------------
# # Prediction Endpoint
# # --------------------------------------------------
# @router.post("/")
# async def predict(file: UploadFile = File(...)):

#     file_bytes = await file.read()
#     image = read_file_as_image(file_bytes)
#     img_batch = np.expand_dims(image, axis=0)

#     predictions = MODEL.predict(img_batch)
#     predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
#     confidence = float(np.max(predictions[0]))

#     severity = "N/A"
#     ratio = 0.0

#     if predicted_class != "Healthy":
#         severity, ratio = get_severity_from_bytes(file_bytes)

#     return {
#         "class": predicted_class,
#         "confidence": round(confidence * 100, 2),
#         "severity": severity,
#         "infected_ratio": round(ratio, 2)
#     }
    
# --------------------------------------------------
from fastapi import APIRouter, File, UploadFile
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import os
import cv2

router = APIRouter(
    prefix="/predict",
    tags=["Disease Prediction"]
)

# --------------------------------------------------
# Model Path
# --------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
API_DIR = os.path.dirname(CURRENT_DIR)
PROJECT_ROOT = os.path.dirname(API_DIR)

MODEL_PATH = os.path.join(PROJECT_ROOT, "ml_models", "V1.keras")

print("MODEL_PATH =", MODEL_PATH)

if not os.path.isfile(MODEL_PATH):
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

# --------------------------------------------------
# ✅ FIX 2: Lazy model loading — model loads on first request, not at startup.
#    This prevents OOM crash on FastAPI Cloud's CPU-only containers which
#    have limited RAM and kill the process if startup uses too much memory.
# --------------------------------------------------
_MODEL = None

def get_model():
    global _MODEL
    if _MODEL is None:
        print("Loading model...")
        _MODEL = tf.keras.models.load_model(MODEL_PATH, compile=False)  # ✅ FIX 1: compile=False
        print("Model loaded.")
    return _MODEL

CLASS_NAMES = [
    "Early Blight",
    "Late Blight",
    "Healthy"
]

# --------------------------------------------------
# Health Check
# --------------------------------------------------
@router.get("/ping")
async def ping():
    return {"message": "Hello World"}

# --------------------------------------------------
# Image Processing
# --------------------------------------------------
def read_file_as_image(data: bytes) -> np.ndarray:
    """Convert uploaded image bytes into a numpy array"""
    image = Image.open(BytesIO(data)).convert("RGB")
    image = image.resize((256, 256))
    return np.array(image)

# --------------------------------------------------
# Severity Detection
# --------------------------------------------------
def get_severity_from_bytes(image_bytes: bytes):
    """
    Rule-based severity detection (in-memory, background removed).
    Returns severity category and infected ratio.
    """
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if img is None:
        return "Unknown", 0.0
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([25, 40, 40])
    upper_green = np.array([85, 255, 255])
    leaf_mask = cv2.inRange(hsv, lower_green, upper_green)

    lower_disease = np.array([0, 0, 0])
    upper_disease = np.array([180, 255, 80])
    disease_mask = cv2.inRange(hsv, lower_disease, upper_disease)

    infected_mask = cv2.bitwise_and(disease_mask, leaf_mask)

    infected_area = np.count_nonzero(infected_mask)
    total_leaf_area = np.count_nonzero(leaf_mask)

    ratio = (
        infected_area / total_leaf_area * 100
        if total_leaf_area > 0
        else 0
    )

    if ratio < 10:
        severity = "Mild"
    elif ratio < 30:
        severity = "Moderate"
    else:
        severity = "Severe"

    return severity, ratio

# --------------------------------------------------
# Prediction Endpoint
# --------------------------------------------------
@router.post("/")
async def predict(file: UploadFile = File(...)):

    file_bytes = await file.read()
    image = read_file_as_image(file_bytes)
    img_batch = np.expand_dims(image, axis=0)

    MODEL = get_model()  # ✅ FIX 2: Load model lazily here
    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = float(np.max(predictions[0]))

    severity = "N/A"
    ratio = 0.0

    if predicted_class != "Healthy":
        severity, ratio = get_severity_from_bytes(file_bytes)

    return {
        "class": predicted_class,
        "confidence": round(confidence * 100, 2),
        "severity": severity,
        "infected_ratio": round(ratio, 2)
    }