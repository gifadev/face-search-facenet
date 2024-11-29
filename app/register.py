from app.person import Person

def register_person(person_service, person_data):
    """
    Fungsi untuk mendaftarkan satu orang berdasarkan input pengguna.
    Args:
        person_service: Instance dari PersonService.
        person_data: Data orang dalam bentuk dictionary.
    """
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
    person_service.register_person(person)
    return {"message": "Person registered successfully"}
