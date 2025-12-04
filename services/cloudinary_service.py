import cloudinary.uploader
from fastapi import UploadFile, HTTPException
import cloudinary_config # Ensure config is loaded

def upload_image(file: UploadFile) -> str:
    """
    Uploads an image to Cloudinary and returns the secure URL.
    """
    try:
        # Upload the file to Cloudinary
        result = cloudinary.uploader.upload(file.file)
        return result.get("secure_url")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")
