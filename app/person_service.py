from typing import List 
from app.person_repository import PersonRepository
from app.person import Person

class PersonService:
    def __init__(self, person_repository: PersonRepository):
        self.person_repository = person_repository

    def register_person(self, person: Person):
        self.person_repository.insert(person)

    def register_persons(self, persons: List[Person]):
        self.person_repository.bulk_insert(persons)

    def find_person_by_image(self, image_path: str):
        image_embedding = Person.get_embedding(image_path)
        return self.person_repository.search_by_image(image_embedding)
