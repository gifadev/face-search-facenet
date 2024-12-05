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
            "full_name": "Anies Baswedan",
            "birth_place": "New York",
            "birth_date": "1990-01-01",
            "address": "123 Main St",
            "nationality": "USA",
            "passport_number": "US123456",
            "gender": "Male",
            "national_id_number": "123-45-6789",
            "marital_status": "Single"
        },
        {
            "full_name": "Ridwan Kamil",
            "birth_place": "Los Angeles",
            "birth_date": "1992-05-15",
            "address": "456 Oak Ave",
            "nationality": "USA",
            "passport_number": "US789012",
            "gender": "Female",
            "national_id_number": "987-65-4321",
            "marital_status": "Married"
        }
    ]
    
    # Path ke file gambar (sesuaikan dengan lokasi file Anda)
    image_paths = [
        "/home/me/Downloads/anies.jpg",
        "/home/me/Downloads/rk.jpg"
    ]
    
    # Buat folder images jika belum ada
    # Path("images").mkdir(exist_ok=True)
    
    # Jalankan bulk registration
    bulk_register_persons(BASE_URL, persons_data, image_paths)
