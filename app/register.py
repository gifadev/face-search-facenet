from app.person import Person
from app.logger import logger

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
