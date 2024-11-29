from elasticsearch import Elasticsearch
import getpass

class Util:
    @staticmethod
    def get_index_name():
        return "people-image-deepface"

    @staticmethod
    def get_connection():

        es = Elasticsearch(hosts="http://localhost:9200",basic_auth=("admin", "4dm1nus3r"))
        es.info() 
        return es

    @staticmethod
    def create_index(es: Elasticsearch, index_name: str):
        index_config = {
            "settings": {
                "index.refresh_interval": "5s",
                "number_of_shards": 1
            },
            "mappings": {
                "properties": {
                    "image_embedding": {
                        "type": "dense_vector",
                        "dims": 128,
                        "index": True,
                        "similarity": "cosine"
                    },
                    "full_name": {
                        "type": "keyword"
                    },
                    "birth_place": {
                        "type": "keyword"
                    },
                    "birth_date": {
                        "type": "date"
                    },
                    "address": {
                        "type": "keyword"
                    },
                    "nationality": {
                        "type": "keyword"
                    },
                    "passport_number": {
                        "type": "keyword"
                    },
                    "gender": {
                        "type": "keyword"
                    },
                    "national_id_number": {
                        "type": "keyword"
                    },
                    "marital_status": {
                        "type": "keyword"
                    },
                    "exif": {
                        "properties": {
                            "location": {
                                "type": "geo_point"
                            },
                            "date": {
                                "type": "date"
                            }
                        }
                    }
                }
            }
        }

        if not es.indices.exists(index=index_name):
            index_creation = es.indices.create(index=index_name, ignore=400, body=index_config)
            print("Index created: ", index_creation)
        else:
            print("Index already exists.")

    @staticmethod
    def delete_index(es: Elasticsearch, index_name: str):
        es.indices.delete(index=index_name, ignore_unavailable=True)
