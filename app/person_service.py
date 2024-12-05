from typing import List 
from app.person_repository import PersonRepository
from app.person import Person
from app.logger import logger

class PersonService:
    def __init__(self, person_repository: PersonRepository):
        self.person_repository = person_repository

    async def register_person(self, person: Person) -> None:
        """
        Register a single person in the database.
        Args:
            person: Person object to register
        """
        try:
            logger.info(f"Registering person: {person.full_name}")
            await self.person_repository.insert(person)
        except Exception as e:
            logger.error(f"Error registering person: {str(e)}", exc_info=True)
            raise

    async def register_persons(self, persons: List[Person]) -> None:
        """
        Register multiple persons in bulk.
        Args:
            persons: List of Person objects to register
        """
        try:
            logger.info(f"Bulk registering {len(persons)} persons")
            await self.person_repository.bulk_insert(persons)
        except Exception as e:
            logger.error(f"Error in bulk registration: {str(e)}", exc_info=True)
            raise

    async def find_person_by_image(self, image_path: str) -> dict:
        """
        Find a person using facial recognition from an image.
        Args:
            image_path: Path to the image file
        Returns:
            dict: Search results with person data if found
        """
        try:
            logger.info(f"Getting embedding for image: {image_path}")
            image_embedding = await Person.get_embedding(image_path)
            
            logger.info("Searching database with image embedding")
            result = await self.person_repository.search_by_image(image_embedding)
            # print("find_person_by_image", result)
            return result
        except Exception as e:
            logger.error(f"Error in find_person_by_image: {str(e)}", exc_info=True)
            raise
