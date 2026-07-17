from src.models.embedding_document import EmbeddingDocument


class EmbeddingGenerator:
    """
    Generates embeddings for ChunkDocument objects.
    """

    def __init__(self, model):
        """
        Args:
            model: SentenceTransformer model
        """
        self.model = model

    # ----------------------------------------------------
    # Generate embedding for one chunk
    # ----------------------------------------------------

    def generate_embedding(self, chunk):

        embedding = self.model.encode(
            chunk.text,
            convert_to_numpy=True
        )

        document = EmbeddingDocument(

            manual_name=chunk.manual_name,

            slide_number=chunk.slide_number,

            chunk_number=chunk.chunk_number,

            title=chunk.title,

            text=chunk.text,

            embedding=embedding.tolist(),

            source_type=chunk.source_type,

            language=chunk.language,

            metadata=chunk.metadata

        )

        return document

    # ----------------------------------------------------
    # Generate embeddings for all chunks
    # ----------------------------------------------------

    def generate_embeddings(self, chunks):

        embedding_documents = []

        total = len(chunks)

        print("\nGenerating Embeddings...\n")

        for index, chunk in enumerate(chunks, start=1):

            document = self.generate_embedding(chunk)

            embedding_documents.append(document)

            print(f"[{index}/{total}] Embedded")

        return embedding_documents