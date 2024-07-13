import ollama
import chromadb


class SemanticSearch:
    def __init__(self):
        client = chromadb.PersistentClient()
        self.chroma_collection = client.create_collection(name="book-highlights", get_or_create=True)

    def index(self, dataframe, metadata={}):
        print(f"Indexing df of size={len(dataframe)}")
        start_index = self.chroma_collection.count()
        for index, row in dataframe.iterrows():
            start_index += 1
            self.chroma_collection.add(
                ids=[str(start_index)],
                embeddings=[row['embedding']],
                documents=[row['highlight']],
                metadatas=metadata
            )

    def generate_embedding(self, sentence):
        response = ollama.embeddings(model="nomic-embed-text", prompt=sentence)
        embedding = response['embedding']
        return embedding

    def query(self, query):
        query_embedding = self.generate_embedding(query)
        results = self.chroma_collection.query(
            query_embeddings=query_embedding,
            n_results=5
        )
        return results
