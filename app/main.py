from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from app.search import search_by_image
from app.register import register_person, register_persons
from app.util import Util
from app.person_service import PersonService
from app.person_repository import PersonRepository
from app.config import get_settings
from app.logger import logger
import os
from fastapi.staticfiles import StaticFiles
import uuid
import socket
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import aiofiles
from datetime import datetime
import json
import asyncio

settings = get_settings()

class ImageSearchException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

def validate_image_file(file: UploadFile) -> None:
    """Validate uploaded image file."""
    if not file:
        raise ImageSearchException("No file uploaded")
    
    # Check file size
    file.file.seek(0, 2)  # Seek to end of file
    size = file.file.tell()
    file.file.seek(0)  # Reset file pointer
    
    if size > settings.MAX_FILE_SIZE:
        raise ImageSearchException(f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE/1024/1024}MB")
    
    # Check file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise ImageSearchException(f"Invalid file extension. Allowed extensions: {settings.ALLOWED_EXTENSIONS}")

async def save_upload_file(upload_file: UploadFile, folder: str) -> str:
    """Save uploaded file to disk asynchronously."""
    try:
        ext = os.path.splitext(upload_file.filename)[1]
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(folder, filename)
        
        async with aiofiles.open(filepath, 'wb') as out_file:
            content = await upload_file.read()
            await out_file.write(content)
            
        return filepath
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise ImageSearchException("Failed to save uploaded file")

def get_active_ip() -> str:
    """Get active IP address of the server."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0] 
        s.close()
        return ip_address
    except Exception as e:
        logger.error(f"Failed to get active IP: {e}")
        return "localhost"

server_ip = get_active_ip()
logger.info(f"Server running on IP: {server_ip}")

app = FastAPI(title=settings.PROJECT_NAME)

@app.exception_handler(ImageSearchException)
async def image_search_exception_handler(request: Request, exc: ImageSearchException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup database connection
try:
    es_db = Util.get_connection()
    person_repo = PersonRepository(es_db, settings.ELASTICSEARCH_INDEX)
    person_service = PersonService(person_repo)
except Exception as e:
    logger.error(f"Failed to initialize database connection: {str(e)}")
    raise

# Create dataset folder if it doesn't exist
os.makedirs(settings.DATASET_FOLDER, exist_ok=True)

# Mount static files
app.mount("/images", StaticFiles(directory=settings.DATASET_FOLDER), name="images")

@app.post("/register/")
async def register_person_api(
    full_name: str = Form(...),
    birth_place: str = Form(...),
    birth_date: str = Form(...),
    address: str = Form(...),
    nationality: str = Form(...),
    passport_number: str = Form(...),
    gender: str = Form(...),
    national_id_number: str = Form(...),
    marital_status: str = Form(...),
    image: UploadFile = File(...)
):
    """
    Register a new person with their details and image.
    
    Args:
        full_name: Full name of the person
        birth_place: Place of birth
        birth_date: Date of birth (YYYY-MM-DD)
        address: Current address
        nationality: Nationality
        passport_number: Passport number
        gender: Gender 
        national_id_number: National ID number
        marital_status: Marital status
        image: Profile image file
    
    Returns:
        dict: Registration result with person details
    """
    try:
        # Validate date format
        try:
            datetime.strptime(birth_date, '%Y-%m-%d')
        except ValueError:
            raise ImageSearchException("Invalid birth date format. Use YYYY-MM-DD")
            
        # Validate gender
        if not gender.strip():
            raise ImageSearchException("Gender cannot be empty")
            
        # Validate image
        validate_image_file(image)
        
        # Save image
        image_path = await save_upload_file(image, settings.DATASET_FOLDER)
        
        # Prepare person data
        person_data = {
            "image_path": image_path,
            "full_name": full_name,
            "birth_place": birth_place,
            "birth_date": birth_date,
            "address": address,
            "nationality": nationality,
            "passport_number": passport_number,
            "gender": gender,
            "national_id_number": national_id_number,
            "marital_status": marital_status,
        }
        
        # Register person
        result = await register_person(person_data, person_service)
        logger.info(f"Successfully registered person: {full_name}")
        return result
        
    except ImageSearchException as e:
        raise
    except Exception as e:
        logger.error(f"Error in register_person_api: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/register-bulk/")
async def register_bulk_persons(
    request: Request,
    files: List[UploadFile] = File(...),
    persons_data: str = Form(...),
    enforce_detection: bool = Form(True)
):
    """
    Register multiple persons with their details and images in bulk.
    
    Args:
        files: List of image files
        persons_data: JSON string containing list of person details
        
    Returns:
        List[dict]: List of registration results
    """
    try:
        # Parse persons data JSON
        persons = json.loads(persons_data)
        if not isinstance(persons, list):
            raise ImageSearchException("persons_data harus berupa array")
        
        if len(persons) != len(files):
            raise ImageSearchException("Jumlah data person harus sama dengan jumlah file gambar")
        
        # Process images in parallel
        async def save_images():
            tasks = []
            for idx, image_file in enumerate(files):
                # Validate image
                validate_image_file(image_file)
                # Save image
                task = save_upload_file(image_file, settings.DATASET_FOLDER)
                tasks.append(task)
            return await asyncio.gather(*tasks)
        
        # Save all images and get their paths
        image_paths = await save_images()
        
        # Add image paths to person data
        for person_data, image_path in zip(persons, image_paths):
            # Validate date format
            try:
                datetime.strptime(person_data["birth_date"], '%Y-%m-%d')
            except ValueError:
                raise ImageSearchException("Invalid birth date format. Use YYYY-MM-DD")
            
            # Validate gender
            if not person_data["gender"].strip():
                raise ImageSearchException("Gender cannot be empty")
            
            person_data["image_path"] = image_path
        
        # Bulk register all persons
        results = await register_persons(persons, person_service)
        
        return JSONResponse({
            "status": "completed",
            "total": len(results),
            "successful": len(results),
            "failed": 0,
            "results": results
        })
        
    except json.JSONDecodeError:
        raise ImageSearchException("Format JSON untuk persons_data tidak valid")
    except Exception as e:
        logger.error(f"Bulk registration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/search/")
async def search_person(image: UploadFile = File(...)):
    """
    Search for a person using facial recognition.
    
    Args:
        image: Image file to search with
        
    Returns:
        dict: Search results with matching persons
    """
    temp_path = None
    try:
        # Validate image
        validate_image_file(image)
        
        # Save temporary image for processing
        temp_path = await save_upload_file(image, settings.DATASET_LOST_FOLDER)
        try:
            # Perform search
            results = await search_by_image(temp_path, person_service)
            print("ini results",results)
            if results.get("status") == "success" and results.get("data"):
                data = results["data"]['hits']['hits'][0]
                print("ini result" , data)
                score = data['_score']
                source_data = data['_source']
                image_path = source_data.get("image_path", "")
                
                # Create response with image URL
                response = {
                    "status": "success",
                    "message": "Person found",
                    "data": {
                        "image_url": f"http://{server_ip}:8000/images/{os.path.basename(image_path)}",
                        "full_name": source_data.get("full_name"),
                        "birth_place": source_data.get("birth_place"),
                        "birth_date": source_data.get("birth_date"),
                        "address": source_data.get("address"),
                        "nationality": source_data.get("nationality"),
                        "passport_number": source_data.get("passport_number"),
                        "gender": source_data.get("gender"),
                        "national_id_number": source_data.get("national_id_number"),
                        "marital_status": source_data.get("marital_status"),
                        "score": score
                    }
                }
                
                logger.info(f"Successfully performed search with image: {image.filename}")
                return response
            else:
                return {"status": "not_found", "message": "Person not found"}
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                print (temp_path)
                # os.remove(temp_path)
                
    except ImageSearchException as e:
        raise
    except Exception as e:
        logger.error(f"Error in search_person: {str(e)}")
        raise HTTPException(status_code=500, detail=f"{str(e)}")
