import chromadb
from chromadb.config import Settings


class vectordb:
    def __init__(self, path, collection):
        self.client = chromadb.PersistentClient(path=path, settings=Settings(allow_reset=True))

        self.collection = self.client.get_or_create_collection(name=collection)

    def add(self, id, data, metadata):
        self.collection.upsert(documents=data, ids=str(id), metadatas=metadata) 

    def query(self, text, results):
        return self.collection.query(query_texts=text, n_results=results)

    def reset(self):
        self.client.reset()




