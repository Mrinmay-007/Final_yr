# # treatment.py

# from fastapi import APIRouter, HTTPException
# from pathlib import Path
# import json

# router = APIRouter(
#     prefix="/treatment",
#     tags=["Treatment"]
# )

# # Load treatment data once when the server starts
# BASE_DIR = Path(__file__).resolve().parent.parent
# JSON_PATH = BASE_DIR / "data" / "treatment.json"

# try:
#     with open(JSON_PATH, "r", encoding="utf-8") as f:
#         treatment_data = json.load(f)
# except Exception as e:
#     treatment_data = {}
#     print(f"Error loading treatment.json: {e}")


# @router.get("/")
# async def get_all_treatments():
#     """
#     Get all disease treatments
#     """
#     return {
#         "success": True,
#         "count": len(treatment_data),
#         "data": treatment_data
#     }


# @router.get("/{disease_name}")
# async def get_treatment(disease_name: str):
#     """
#     Get treatment details for a specific disease
#     """

#     disease_name = disease_name.strip().title()

#     disease = treatment_data.get(disease_name)

#     if not disease:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Treatment data not found for '{disease_name}'"
#         )

#     return {
#         "success": True,
#         "disease": disease_name,
#         "data": disease
#     }


# @router.get("/summary/{disease_name}")
# async def get_treatment_summary(disease_name: str):
#     """
#     Lightweight response for frontend cards
#     """
#     disease_name = disease_name.strip().title()
#     disease = treatment_data.get(disease_name)

#     if not disease:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Treatment data not found for '{disease_name}'"
#         )

#     return {
#         "disease_name": disease.get("disease_name"),
#         "severity": disease.get("severity"),
#         "description": disease.get("description")
#     }