import truststore

# ----------------------------------------------------
# Use Windows Certificate Store
# (Useful in Corporate Windows Environments)
# ----------------------------------------------------

truststore.inject_into_ssl()

from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Loads and manages the Sentence Transformer model.
    """

    def __init__(self):
        """
        Initialize the embedding model.
        """

        self.model_name = "all-MiniLM-L6-v2"
        self.model = None

    # ----------------------------------------------------
    # Load Model
    # ----------------------------------------------------

    def load_model(self):
        """
        Load the Sentence Transformer model.
        """

        if self.model is None:

            print("=" * 60)
            print("Loading Embedding Model")
            print("=" * 60)

            print(f"Model Name : {self.model_name}")
            print("\nDownloading model (first time only)...")

            try:

                self.model = SentenceTransformer(self.model_name)

                print("\nEmbedding model loaded successfully!")

            except Exception as e:

                print("\nFailed to load embedding model.")
                print(f"Error: {e}")

                raise

        return self.model

    # ----------------------------------------------------
    # Get Model Name
    # ----------------------------------------------------

    def get_model_name(self):
        """
        Returns the model name.
        """

        return self.model_name