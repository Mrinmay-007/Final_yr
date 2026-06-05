# #Final_yr/api/auth/a.py
# # Final_yr/ .env

# import os
# from dotenv import load_dotenv
# # Load API Key from .env
# load_dotenv()
# API_KEY = os.getenv("WEATHER_API_KEY")
# KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv(
#     "ACCESS_TOKEN_EXPIRE_MINUTES")) #type: ignore

# print(API_KEY)
# print(KEY)
# print(ALGORITHM)
# print(ACCESS_TOKEN_EXPIRE_MINUTES)

# Final_yr/api/auth/a.py

import os
from dotenv import load_dotenv
load_dotenv()

# Read variables
API_KEY = os.getenv("WEATHER_API_KEY")
KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

expire = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# Safe conversion
ACCESS_TOKEN_EXPIRE_MINUTES = int(expire) if expire else 30

print("API_KEY:", API_KEY)
print("SECRET_KEY:", KEY)
print("ALGORITHM:", ALGORITHM)
print("TOKEN_EXPIRE:", ACCESS_TOKEN_EXPIRE_MINUTES)