import os
from app.util import Util

def search_by_image(service, filename):
    """
    Cari orang berdasarkan gambar.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    # Cari orang
    result = service.find_person_by_image(filename)

    if not result:
        print("Image not recognized or not registered.")
        return None

    print("Person data found:", result)
    return result
