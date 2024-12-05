import os
from app.util import Util
from app.logger import logger

async def search_by_image(image_path: str, service) -> dict:
    """
    Search for a person using facial recognition.
    Args:
        image_path: Path to the image file
        service: Instance of PersonService
    Returns:
        dict: Search results with person data if found
    """
    try:
        logger.info(f"Checking if image exists: {image_path}")
        if not os.path.exists(image_path):
            error_msg = f"File not found: {image_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        # Search for person
        logger.info("Searching for person using facial recognition")
        result = await service.find_person_by_image(image_path)
        # print("search_by_image", result)
        if result.get("status") == "not_found":
            logger.info("No matching person found")
            return result

        logger.info(f"Person found with score: {result.get('_score', 'N/A')}")
        return {
            "status": "success",
            "message": "Person found",
            "data": result
        }
    except Exception as e:
        logger.error(f"Error in search_by_image: {str(e)}", exc_info=True)
        raise
