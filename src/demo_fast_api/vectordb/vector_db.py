import os
from typing import Any
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

class VectorDB:
    def __init__(self):
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX_NAME")

        if not self.api_key:
            raise ValueError("PINECONE_API_KEY IS NOT SET")

        if not self.index_name:
            raise ValueError("PINECONE_INDEX_NAME IS NOT SET")

        self.client = Pinecone(api_key=self.api_key)

        existing_indexes = (
            self.client.list_indexes().names()
        )

        if self.index_name not in existing_indexes:
            self.client.create_index(
                name = self.index_name,
                dimension=384,
                metric="cosine"
            )

        self.index = self.client.Index(self.index_name)

    def insert_vectors(self, vectors : list[dict[str, Any]], namespace: str):
        return self.index.upsert(vectors=vectors, namespace=namespace)

    def delete_namespace(self, namespace: str):
        try:
            return self.index.delete(
                        delete_all=True,
                        namespace=namespace,
                    )
        except Exception as e:
            if "namespace not found" in str(e).lower():
                return None
            raise