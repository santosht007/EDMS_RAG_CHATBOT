import pickle
import faiss
import numpy as np

from config import FAISS_INDEX_FILE
from config import METADATA_FILE


class FAISSManager:
    """
    Manages the FAISS vector database.

    Responsibilities
    ----------------
    - Create FAISS index
    - Add embedding vectors
    - Save FAISS index
    - Load FAISS index
    - Save metadata
    - Load metadata
    """

    def __init__(self, embedding_dimension):
        """
        Initialize FAISS Index.

        Args:
            embedding_dimension (int): Size of embedding vector.
        """

        self.embedding_dimension = embedding_dimension
        self.index = faiss.IndexFlatL2(embedding_dimension)
        self.metadata = []

    # --------------------------------------------------
    # Add Embeddings
    # --------------------------------------------------

    def add_embeddings(self, embedding_documents):
        """
        Add embeddings to FAISS index.

        Args:
            embedding_documents (list)
        """

        if not embedding_documents:
            print("No embeddings found.")
            return

        vectors = np.array(
            [doc.embedding for doc in embedding_documents],
            dtype=np.float32
        )

        self.index.add(vectors)
        self.metadata.extend(embedding_documents)

        print(f"\nAdded {len(vectors)} vectors to FAISS.")

    # --------------------------------------------------
    # Total Vectors
    # --------------------------------------------------

    def total_vectors(self):
        """
        Returns total vectors in FAISS.
        """

        return self.index.ntotal

    # --------------------------------------------------
    # Save FAISS Index
    # --------------------------------------------------

    def save_index(self):
        """
        Save FAISS index to disk.
        """

        faiss.write_index(
            self.index,
            str(FAISS_INDEX_FILE)
        )

        print("\nFAISS index saved successfully.")

    # --------------------------------------------------
    # Load FAISS Index
    # --------------------------------------------------

    def load_index(self):
        """
        Load FAISS index from disk.
        """

        self.index = faiss.read_index(
            str(FAISS_INDEX_FILE)
        )

    # --------------------------------------------------
    # Save Metadata
    # --------------------------------------------------

    def save_metadata(self):
        """
        Save metadata to disk.
        """

        with open(METADATA_FILE, "wb") as file:
            pickle.dump(self.metadata, file)

        print("Metadata saved successfully.")

    # --------------------------------------------------
    # Load Metadata
    # --------------------------------------------------

    def load_metadata(self):
        """
        Load metadata from disk.
        """

        with open(METADATA_FILE, "rb") as file:
            self.metadata = pickle.load(file)

    # --------------------------------------------------
    # Get Metadata
    # --------------------------------------------------

    def get_metadata(self):
        """
        Returns metadata list.
        """

        return self.metadata