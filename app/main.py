from fastapi import FastAPI, UploadFile, File, Form
from app.search import search_by_image
from app.register import register_person
from app.util import Util
from app.person_service import PersonService
from app.person_repository import PersonRepository
import os
from fastapi.staticfiles import StaticFiles
import uuid
import socket
from fastapi.middleware.cors import CORSMiddleware

def get_active_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0] 
        s.close()
        return ip_address
    except Exception as e:
        raise Exception(f"Gagal mendapatkan IP aktif: {e}")
    
app = FastAPI()
server_ip = get_active_ip()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f"http://{server_ip}:8000", 
        f"http://{server_ip}:8100",   
        "http://localhost:8100"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Setup koneksi Elasticsearch dan service
es_db = Util.get_connection()
person_repo = PersonRepository(es_db, Util.get_index_name())
person_service = PersonService(person_repo)


# Folder untuk menyimpan file gambar
DATASET_FOLDER = "dataset/persons"
os.makedirs(DATASET_FOLDER, exist_ok=True)

#mounting untuk folder foto
app.mount("/images", StaticFiles(directory="dataset/persons"), name="images")



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
    image: UploadFile = Form(...)
):
    """
    Endpoint untuk mendaftarkan satu orang berdasarkan input pengguna.
    Args:
        full_name: Nama lengkap orang.
        birth_place: Tempat lahir.
        birth_date: Tanggal lahir.
        address: Alamat.
        nationality: Kewarganegaraan.
        passport_number: Nomor paspor.
        gender: Jenis kelamin.
        national_id_number: Nomor identitas nasional.
        marital_status: Status pernikahan.
        image: File gambar yang diunggah.
    """

    # Get extension
    file_extension = os.path.splitext(image.filename)[1]
    if not file_extension:
        return {"error": "Invalid file extension"}
    
    # Simpan file gambar ke folder dataset/persons
    image_filename = f"{uuid.uuid4().hex}{file_extension}"
    image_path = os.path.join(DATASET_FOLDER, image_filename)
    with open(image_path, "wb") as f:
        f.write(await image.read())
    # Siapkan data untuk disimpan
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

    # Registrasi ke Elasticsearch
    response = register_person(person_service, person_data)
    return response

@app.post("/search/")
async def search_person(image: UploadFile = File(...)):
    """
    Endpoint untuk mencari orang berdasarkan gambar.
    Args:
        file: Gambar yang diunggah.
    """
    temp_filename = f"temp_{image.filename}"
    with open(temp_filename, "wb") as temp_file:
        temp_file.write(await image.read())
    
    # Gunakan search_by_image
    result = search_by_image(person_service, temp_filename)
    
    # Hapus file sementara
    os.remove(temp_filename)
    
    if result:
        score = result["_score"]
        person_data = result["_source"]
        image_url = f"http://{server_ip}:8000/images/{os.path.basename(person_data.get('image_path', ''))}"
        value = {
            "score":score,
            "image":image_url,
            "full_name":person_data.get("full_name"),
            "birth_place":person_data.get("birth_place"),
            "birth_date":person_data.get("birth_date"),
            "address":person_data.get("address"),
            "nationality":person_data.get("nationality"),
            "passport_number":person_data.get("passport_number"),
            "gender":person_data.get("gender"),
            "national_id_number":person_data.get("national_id_number"),
            "marital_status":person_data.get("marital_status")
        }
        return value
    return {"message": "data not found"}

