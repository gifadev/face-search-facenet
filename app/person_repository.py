from typing import List, Dict
from elasticsearch import AsyncElasticsearch
from app.util import Util
from app.logger import logger

class PersonRepository:
    def __init__(self, es_client: AsyncElasticsearch, index_name: str = "people-image-deepface"):
        self.es_client = es_client
        self._index_name = index_name

    async def _setup_index(self):
        """Setup Elasticsearch index with proper mappings."""
        try:
            await Util.create_index(self.es_client, self._index_name)
        except Exception as e:
            logger.error(f"Error setting up index: {str(e)}", exc_info=True)
            raise

    async def insert(self, person) -> None:
        """
        Insert a single person document into Elasticsearch.
        Args:
            person: Person object to insert.
        """
        try:
            await person.generate_embedding()
            document = person.to_dict()
            
            # Gunakan metode asinkron dengan benar
            response = self.es_client.index(index=self._index_name, document=document)
            logger.info(f"Successfully inserted person: {person.full_name} with response: {response}")
        except Exception as e:
            logger.error(f"Error inserting person: {str(e)}", exc_info=True)
            raise

    async def bulk_insert(self, persons: List) -> None:
        """
        Insert multiple person documents in bulk.
        Args:
            persons: List of Person objects to insert.
        """
        try:
            operations = []
            for person in persons:
                await person.generate_embedding()
                operations.append({"index": {"_index": self._index_name}})
                operations.append(person.to_dict())

            # Gunakan bulk asinkron
            response = await self.es_client.bulk(body=operations)
            if response['errors']:
                logger.error("Bulk insert encountered errors.")
                raise Exception("Some documents failed during bulk insert.")
            
            logger.info(f"Successfully bulk inserted {len(persons)} persons")
        except Exception as e:
            logger.error(f"Error in bulk insert: {str(e)}", exc_info=True)
            raise

    async def search_by_image(self, image_embedding: List[float]) -> Dict:
        """
        Search for persons using image embedding vector.
        Args:
            image_embedding: Vector embedding of the query image.
        Returns:
            dict: Search results with matching persons.
        """
        try:
            search_body = {
                "knn": {
                    "field": "image_embedding",
                    "k": 3,
                    "num_candidates": 100,
                    "query_vector": image_embedding
                },
                "_source": [
                    "full_name", "birth_place", "birth_date",
                    "address", "nationality", "passport_number",
                    "gender", "national_id_number", "marital_status", "image_path"
                ]
            }

            # Gunakan pencarian asinkron
            search_result = self.es_client.search(
                index=self._index_name,
                body=search_body,
                size=3
            )

            # Validasi threshold
            threshold = 0.89
            results = [
                hit['_source'] for hit in search_result['hits']['hits']
                if hit['_score'] >= threshold
            ]

            if results:
                logger.info(f"Found {len(results)} matching results") 
                # return results[0]  # Return the best match
                return search_result
            
            logger.info("No matches found above threshold")
            return None
        except Exception as e:
            logger.error(f"Error in search_by_image: {str(e)}", exc_info=True)
            raise
