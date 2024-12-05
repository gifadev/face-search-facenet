from app.person import Person
from app.logger import logger
from typing import List, Dict

async def register_person(person_data: dict, person_service) -> dict:
    """
    Register a person based on user input.
    Args:
        person_data: Dictionary containing person data
        person_service: Instance of PersonService
    Returns:
        dict: Registration result
    """
    try:
        logger.info(f"Creating Person object for {person_data['full_name']}")
        person = Person(
            person_data["image_path"],
            person_data["full_name"],
            person_data["birth_place"],
            person_data["birth_date"],
            person_data["address"],
            person_data["nationality"],
            person_data["passport_number"],
            person_data["gender"],
            person_data["national_id_number"],
            person_data["marital_status"]
        )
        
        logger.info("Registering person in database")
        await person_service.register_person(person)
        logger.info(f"Successfully registered {person_data['full_name']}")
        
        return {
            "status": "success",
            "message": "Person registered successfully",
            "data": {
                "full_name": person_data["full_name"],
                "national_id_number": person_data["national_id_number"]
            }
        }
    except Exception as e:
        logger.error(f"Error in register_person: {str(e)}", exc_info=True)
        raise

async def register_persons(persons_data: List[dict], person_service) -> List[Dict]:
    """
    Register multiple persons in bulk.
    Args:
        persons_data: List of dictionaries containing person data
        person_service: Instance of PersonService
    Returns:
        List[dict]: List of registration results
    """
    try:
        logger.info(f"Creating Person objects for {len(persons_data)} persons")
        persons = []
        for data in persons_data:
            person = Person(
                data["image_path"],
                data["full_name"],
                data["birth_place"],
                data["birth_date"],
                data["address"],
                data["nationality"],
                data["passport_number"],
                data["gender"],
                data["national_id_number"],
                data["marital_status"]
            )
            persons.append(person)
        
        logger.info("Bulk registering persons in database")
        await person_service.register_persons(persons)
        logger.info(f"Successfully bulk registered {len(persons)} persons")
        
        return [{
            "status": "success",
            "message": "Person registered successfully",
            "data": {
                "full_name": data["full_name"],
                "national_id_number": data["national_id_number"]
            }
        } for data in persons_data]
        
    except Exception as e:
        logger.error(f"Error in register_persons: {str(e)}", exc_info=True)
        raise
