import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv

load_dotenv()

cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
api_key = os.getenv("CLOUDINARY_API_KEY")
api_secret = os.getenv("CLOUDINARY_API_SECRET")

if not all([cloud_name, api_key, api_secret]):
    print("⚠️ WARNING: Cloudinary credentials missing in .env")

# Configuración de Cloudinary
cloudinary.config( 
  cloud_name = cloud_name, 
  api_key = api_key, 
  api_secret = api_secret,
  secure = True
)
