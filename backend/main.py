"""
AdModel Backend - Main API
AI-powered virtual model generation for advertisements
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
import os
import uuid
from datetime import datetime
import shutil

app = FastAPI(
    title="AdModel API",
    description="AI-powered virtual model webapp for advertisements",
    version="1.0.0"
)

# CORS middleware
# TODO: In production, restrict allow_origins to specific trusted domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Directories
UPLOAD_DIR = "uploads"
MODELS_DIR = "saved_models"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Configuration
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_image_file(filename: str, file_size: int = 0) -> tuple[bool, str]:
    """
    Validate uploaded image file
    Returns: (is_valid, error_message)
    """
    if not filename:
        return False, "No filename provided"
    
    # Check file extension
    file_ext = os.path.splitext(filename.lower())[1]
    if file_ext not in ALLOWED_IMAGE_EXTENSIONS:
        return False, f"Invalid file type. Allowed types: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
    
    # Check file size if provided
    if file_size > MAX_FILE_SIZE:
        return False, f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024):.0f} MB"
    
    return True, ""


class ModelConfig(BaseModel):
    """Model configuration schema"""
    id: Optional[str] = None
    name: str
    gender: str
    age: int
    ethnicity: str
    skin_color: str
    hair_color: str
    body_type: str
    height: str
    pose_description: str
    created_at: Optional[str] = None
    product_image: Optional[str] = None


class VirtualModel:
    """Virtual Model Manager"""
    
    @staticmethod
    def generate_model_id():
        """Generate unique model ID"""
        return str(uuid.uuid4())
    
    @staticmethod
    def save_model(config: dict, image_path: Optional[str] = None):
        """Save model configuration"""
        model_id = config.get("id") or VirtualModel.generate_model_id()
        config["id"] = model_id
        config["created_at"] = datetime.now().isoformat()
        
        # Save configuration
        config_path = os.path.join(MODELS_DIR, f"{model_id}.json")
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        
        # Save associated image if provided
        if image_path and os.path.exists(image_path):
            image_ext = os.path.splitext(image_path)[1]
            new_image_path = os.path.join(MODELS_DIR, f"{model_id}{image_ext}")
            shutil.copy(image_path, new_image_path)
            config["product_image"] = f"{model_id}{image_ext}"
        
        return config
    
    @staticmethod
    def load_model(model_id: str):
        """Load model configuration"""
        config_path = os.path.join(MODELS_DIR, f"{model_id}.json")
        if not os.path.exists(config_path):
            return None
        
        with open(config_path, "r") as f:
            return json.load(f)
    
    @staticmethod
    def list_models():
        """List all saved models"""
        models = []
        for filename in os.listdir(MODELS_DIR):
            if filename.endswith(".json"):
                with open(os.path.join(MODELS_DIR, filename), "r") as f:
                    models.append(json.load(f))
        return sorted(models, key=lambda x: x.get("created_at", ""), reverse=True)
    
    @staticmethod
    def delete_model(model_id: str):
        """Delete a saved model"""
        config_path = os.path.join(MODELS_DIR, f"{model_id}.json")
        if os.path.exists(config_path):
            # Load config to find associated image
            with open(config_path, "r") as f:
                config = json.load(f)
            
            # Delete config file
            os.remove(config_path)
            
            # Delete associated image if exists
            if "product_image" in config:
                image_path = os.path.join(MODELS_DIR, config["product_image"])
                if os.path.exists(image_path):
                    os.remove(image_path)
            
            return True
        return False


@app.get("/")
async def root():
    """Serve the main application page"""
    return FileResponse("static/index.html")


@app.post("/api/models/create")
async def create_model(
    name: str = Form(...),
    gender: str = Form(...),
    age: int = Form(...),
    ethnicity: str = Form(...),
    skin_color: str = Form(...),
    hair_color: str = Form(...),
    body_type: str = Form(...),
    height: str = Form(...),
    pose_description: str = Form(...),
    product_image: Optional[UploadFile] = File(None)
):
    """
    Create a new virtual model with specified characteristics
    """
    try:
        # Handle product image upload
        image_path = None
        if product_image:
            # Validate file
            is_valid, error_msg = validate_image_file(product_image.filename)
            if not is_valid:
                raise HTTPException(status_code=400, detail=error_msg)
            
            # Read file content first to check size
            content = await product_image.read()
            if len(content) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400, 
                    detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024):.0f} MB"
                )
            
            # Use secure file extension
            file_ext = os.path.splitext(product_image.filename.lower())[1]
            image_id = str(uuid.uuid4())
            image_path = os.path.join(UPLOAD_DIR, f"{image_id}{file_ext}")
            
            with open(image_path, "wb") as buffer:
                buffer.write(content)
        
        # Create model configuration
        config = {
            "name": name,
            "gender": gender,
            "age": age,
            "ethnicity": ethnicity,
            "skin_color": skin_color,
            "hair_color": hair_color,
            "body_type": body_type,
            "height": height,
            "pose_description": pose_description,
        }
        
        # Save the model
        saved_config = VirtualModel.save_model(config, image_path)
        
        return JSONResponse({
            "success": True,
            "message": "Virtual model created successfully",
            "model": saved_config
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/models")
async def list_models():
    """List all saved virtual models"""
    try:
        models = VirtualModel.list_models()
        return JSONResponse({
            "success": True,
            "models": models,
            "count": len(models)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/models/{model_id}")
async def get_model(model_id: str):
    """Get a specific model by ID"""
    try:
        model = VirtualModel.load_model(model_id)
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        
        return JSONResponse({
            "success": True,
            "model": model
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/models/{model_id}")
async def delete_model(model_id: str):
    """Delete a saved model"""
    try:
        if VirtualModel.delete_model(model_id):
            return JSONResponse({
                "success": True,
                "message": "Model deleted successfully"
            })
        else:
            raise HTTPException(status_code=404, detail="Model not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/models/{model_id}/use-with-product")
async def use_model_with_product(
    model_id: str,
    product_image: UploadFile = File(...)
):
    """
    Use a saved model with a new product image for advertisement
    """
    try:
        # Load the model
        model = VirtualModel.load_model(model_id)
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        
        # Validate file
        is_valid, error_msg = validate_image_file(product_image.filename)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Read file content first to check size
        content = await product_image.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024):.0f} MB"
            )
        
        # Save new product image with secure extension
        file_ext = os.path.splitext(product_image.filename.lower())[1]
        image_id = str(uuid.uuid4())
        image_path = os.path.join(UPLOAD_DIR, f"{image_id}{file_ext}")
        
        with open(image_path, "wb") as buffer:
            buffer.write(content)
        
        return JSONResponse({
            "success": True,
            "message": "Model applied to new product successfully",
            "model": model,
            "product_image": f"{image_id}{image_ext}",
            "ad_preview": {
                "model_characteristics": {
                    "gender": model["gender"],
                    "age": model["age"],
                    "ethnicity": model["ethnicity"],
                    "pose": model["pose_description"]
                },
                "status": "Generated - Ready for use in advertisement"
            }
        })
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AdModel API",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
