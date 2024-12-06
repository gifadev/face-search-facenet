import requests
import json
import os
from pathlib import Path

def bulk_register_persons(base_url: str, persons_data: list, image_paths: list):
    """
    Register multiple persons with their images.
    
    Args:
        base_url: API base URL (e.g., "http://localhost:8000")
        persons_data: List of dictionaries containing person information
        image_paths: List of paths to image files, must match order of persons_data
    """
    try:
        # Validasi jumlah data dan gambar
        if len(persons_data) != len(image_paths):
            raise ValueError("Jumlah data person harus sama dengan jumlah gambar")
            
        # Siapkan file gambar untuk upload
        files = []
        for i, image_path in enumerate(image_paths):
            # Pastikan file exists
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"File tidak ditemukan: {image_path}")
                
            # Buka file gambar dan tambahkan ke list files
            # Parameter 'files' adalah nama field yang diexpect oleh API
            files.append(
                ('files', (
                    os.path.basename(image_path),  # nama file
                    open(image_path, 'rb'),        # file object dalam mode binary
                    'image/jpeg'                   # mime type
                ))
            )
        
        # Siapkan data untuk request
        request_data = {
            'persons_data': json.dumps(persons_data),  # Convert list ke JSON string
            'enforce_detection': 'true'
        }
        
        # Kirim request ke endpoint bulk register
        print("Mengirim request bulk registration...")
        response = requests.post(
            f'{base_url}/register-bulk/',
            files=files,    # List of tuples untuk file upload
            data=request_data  # Data tambahan (persons_data dan enforce_detection)
        )
        
        # Tampilkan hasil
        if response.status_code == 200:
            result = response.json()
            print("\nHasil Registration:")
            print(f"Status: {result['status']}")
            print(f"Total: {result['total']}")
            print(f"Sukses: {result['successful']}")
            print(f"Gagal: {result['failed']}")
            print("\nDetail hasil:")
            for r in result['results']:
                print(f"- {r['data']['full_name']}: {r['status']}")
        else:
            print(f"Error: {response.status_code}")
            print(response.json())
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Tutup semua file yang dibuka
        for _, (_, f, _) in files:
            f.close()

# Contoh penggunaan
if __name__ == "__main__":
    # URL API
    BASE_URL = "http://172.15.3.237:8000"
    
    # Data person (sesuaikan dengan format yang dibutuhkan)
    persons_data = [
        {
            "full_name": "abi",
            "birth_place": "Bekasi",
            "birth_date": "1990-01-01",
            "address": "123 Main St",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "123-45-6789",
            "marital_status": "Single"
        },
        {
            "full_name": "adi",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "ali",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "arif munawar",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "arrizque",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "awan",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "azhar",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "chairul",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "chandra",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "cristoper",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "eko",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "fajri",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "fandi",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "ferdi",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "firman",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "gisna",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "hanif",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "imanuel zagoto",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "jaki",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "kharisma",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "kunto",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "leon",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "luthfi",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "moel",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "perlindungan duha",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "purwowidodo",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "radit",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "rajadi",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "reizky lesmana",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "reyhan",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "ridzki",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "rizky",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "rui costa hidayat",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "somad",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "tora",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "wahyu sanjaya",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "wildan",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "yasser arafat",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        },
        {
            "full_name": "yusuf",
            "birth_place": "Bekasi",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "Indonesia",
            "passport_number": "INA123456",
            "gender": "Male",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        }
    ]
    
    # Path ke file gambar (sesuaikan dengan lokasi file Anda)
    image_paths = [
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/abi.png",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/adi.png",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/ali.png",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/arif_munawar.jpeg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/arrizque.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/awan.png",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/azhar.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/chairul.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/chandra.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/cristoper.jpeg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/eko.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/fajri.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/fandi.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/ferdi.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/firman.png",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/gisna.jpeg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/hanif.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/imanuel_zagoto.jpeg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/jaki.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/kharisma.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/kunto.png",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/leon.png",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/luthfi.jpeg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/moel.png",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/perlindungan_duha.jpeg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/purwowidodo.jpeg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/radit.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/rajadi.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/reizky_lesmana.jpeg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/reyhan.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/ridzki.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/rizky.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/rui_costa_hidayat.jpeg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/somad.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/tora.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/wahyu_sanjaya.jpeg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/wildan.jpg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/yasser_arafat.jpeg",
        "/home/me/app/image_search/image-search-people-deepface-facenet/dataset/register/yusuf.jpg",
    ]
    
    # Buat folder images jika belum ada
    # Path("images").mkdir(exist_ok=True)
    
    # Jalankan bulk registration
    bulk_register_persons(BASE_URL, persons_data, image_paths)
