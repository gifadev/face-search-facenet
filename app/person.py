from deepface import DeepFace
from PIL import Image
import numpy as np

class Person:
    def __init__(self, image_path=None, full_name=None, birth_place=None, birth_date=None, address=None, nationality=None, passport_number=None, gender=None, national_id_number=None, marital_status=None):
        self.image_path = image_path
        self.full_name = full_name
        self.birth_place = birth_place
        self.birth_date = birth_date
        self.address = address
        self.nationality = nationality
        self.passport_number = passport_number
        self.gender = gender
        self.national_id_number = national_id_number
        self.marital_status = marital_status
        self.image_embedding = None

    @staticmethod
    def get_embedding(image_path: str, model_name="Facenet"):
        """
        Generate an embedding vector for the face in the given image.
        """
        try:
            embedding_result = DeepFace.represent(img_path=image_path, model_name=model_name)
            if embedding_result:
                # Ambil embedding dari hasil pertama
                embedding = embedding_result[0]["embedding"]
                return np.array(embedding)
            else:
                raise ValueError("No embedding found for the given image.")
        except Exception as e:
            print(f"Error generating embedding for {image_path}: {e}")
            return None

    def generate_embedding(self, model_name="Facenet"):
        """
        Generate and store the embedding for the current instance.
        """
        self.image_embedding = Person.get_embedding(self.image_path, model_name)

    def __repr__(self):
        return (f"image_path={self.image_path}, "
                f"full_name={self.full_name}, image_embedding={self.image_embedding})")

    def to_dict(self):
        return {
            "image_path": self.image_path,
            "full_name": self.full_name,
            "birth_place": self.birth_place,
            "birth_date": self.birth_date,
            "address": self.address,
            "nationality": self.nationality,
            "passport_number": self.passport_number,
            "gender": self.gender,
            "national_id_number": self.national_id_number,
            "marital_status": self.marital_status,
            "image_embedding": self.image_embedding.tolist() if self.image_embedding is not None else None
        }
