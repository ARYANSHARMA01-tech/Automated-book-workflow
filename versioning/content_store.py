import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()
collection = client.get_or_create_collection(name="books")

def save_version(title, content):
    collection.add(
        documents=[content],
        ids=[title]
    )

def retrieve_similar_version(query_text):
    return collection.query(query_texts=[query_text], n_results=1)