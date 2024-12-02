from deepface import DeepFace
from PIL import Image
import numpy as np
from app.logger import logger
import asyncio
from concurrent.futures import ThreadPoolExecutor

class Person:
    # Thread pool for CPU-intensive tasks
    _executor = ThreadPoolExecutor(max_workers=3)
    
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
    async def get_embedding(image_path: str, model_name="Facenet") -> np.ndarray:
        """
        Generate an embedding vector for the face in the given image.
        Args:
            image_path: Path to the image file
            model_name: Name of the model to use for embedding
        Returns:
            numpy.ndarray: Embedding vector
        """
        try:
            logger.info(f"Generating embedding for image: {image_path}")
            
            # Run CPU-intensive task in thread pool
            loop = asyncio.get_event_loop()
            embedding_result = await loop.run_in_executor(
                Person._executor,
                lambda: DeepFace.represent(img_path=image_path, model_name=model_name)
            )
            
            if embedding_result:
                embedding = embedding_result[0]["embedding"]
                embedding_array = np.array(embedding)
                logger.info(f"Successfully generated embedding with shape: {embedding_array.shape}")
                return embedding_array
            else:
                raise ValueError("No embedding found for the given image.")
        except Exception as e:
            logger.error(f"Error generating embedding for {image_path}: {str(e)}", exc_info=True)
            raise

    async def generate_embedding(self, model_name="Facenet") -> None:
        """
        Generate and store the embedding for the current instance.
        Args:
            model_name: Name of the model to use for embedding
        """
        try:
            self.image_embedding = await self.get_embedding(self.image_path, model_name)
        except Exception as e:
            logger.error(f"Error generating embedding for person {self.full_name}: {str(e)}", exc_info=True)
            raise

    def __repr__(self):
        return (f"Person(image_path={self.image_path}, "
                f"full_name={self.full_name})")

    def to_dict(self):
        """Convert person object to dictionary for storage"""
        try:
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
        except Exception as e:
            logger.error(f"Error converting person to dict: {str(e)}", exc_info=True)
            raise
