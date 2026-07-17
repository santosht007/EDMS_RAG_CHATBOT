import numpy as np


class SearchEngine:
    """
    Performs semantic search using FAISS.
    """

    def __init__(self, embedding_model, faiss_manager):
        """
        Initialize Search Engine.
        """

        self.embedding_model = embedding_model
        self.faiss_manager = faiss_manager

    # --------------------------------------------------
    # Convert Question to Embedding
    # --------------------------------------------------

    def embed_query(self, query):
        """
        Convert user query into embedding.
        """

        embedding = self.embedding_model.encode(
            query,
            convert_to_numpy=True
        )

        return embedding.astype(np.float32).reshape(1, -1)

    # --------------------------------------------------
    # Search FAISS
    # --------------------------------------------------

    def search(self, query, top_k=5):
        """
        Search the FAISS index.
        """

        query_vector = self.embed_query(query)

        distances, indices = self.faiss_manager.index.search(
            query_vector,
            top_k
        )

        metadata = self.faiss_manager.get_metadata()

        results = []

        for distance, index in zip(distances[0], indices[0]):

            if index == -1:
                continue

            document = metadata[index]

            document.similarity_score = float(distance)

            results.append(document)

        return results

    # --------------------------------------------------
    # Display Results
    # --------------------------------------------------

    def display_results(self, results):
        """
        Display search results.
        """

        print("\n")
        print("=" * 60)
        print("Search Results")
        print("=" * 60)

        if not results:
            print("No results found.")
            return

        for i, doc in enumerate(results, start=1):

            print(f"\nResult {i}")
            print("-" * 60)

            print(f"Manual    : {doc.manual_name}")
            print(f"Slide     : {doc.slide_number}")
            print(f"Chunk     : {doc.chunk_number}")
            print(f"Title     : {doc.title}")
            print(f"Distance  : {doc.similarity_score:.4f}")

            print("\nText:")
            print(doc.text)