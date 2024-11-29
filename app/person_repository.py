from typing import List, Dict
from elasticsearch import Elasticsearch
from app.util import Util  # Pastikan util.py ada di direktori yang sama

class PersonRepository:
    def __init__(self, es_client: Elasticsearch, index_name: str = "people-image-deepface"):
        self.es_client = es_client
        self._index_name = index_name
        Util.create_index(es_client, index_name)

    def insert(self, person):
        person.generate_embedding()
        document = person.to_dict()
        self.es_client.index(index=self._index_name, document=document)

    def bulk_insert(self, persons: List):
        operations = []
        for person in persons:
            operations.append({"index": {"_index": self._index_name}})
            operations.append(person.to_dict())
        self.es_client.bulk(body=operations)

    def search_by_image(self, image_embedding: List[float]):
        field_key = "image_embedding"

        knn = {
            "field": field_key,
            "k": 3,
            "num_candidates": 100,
            "query_vector": image_embedding
        }

        fields = [
            "full_name", "birth_place", "birth_date",
            "address", "nationality", "passport_number",
            "gender", "national_id_number", "marital_status", "image_path"
        ]

        try:
            resp = self.es_client.search(
                index=self._index_name,
                body={
                    "knn": knn,
                    "_source": fields
                },
                size=3  
            )

            # validasi threshold
            threshold = 0.89
            results = [
                hit for hit in resp['hits']['hits']
                if hit['_score'] >= threshold
            ]

            if not results:  
                print("No relevant results found.")
                return None
            
            print(results[0]['_score'])
            return results[0]
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}

