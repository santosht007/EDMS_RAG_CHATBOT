class EmbeddingDocument:
    """
    Represents a document chunk together with its embedding vector.
    """

    def __init__(
        self,
        manual_name,
        slide_number,
        chunk_number,
        title,
        text,
        embedding,
        source_type="PowerPoint",
        language="English",
        metadata=None,
        similarity_score=None
    ):
        """
        Initialize an EmbeddingDocument.

        Args:
            manual_name (str): Name of the source manual.
            slide_number (int): Slide number.
            chunk_number (int): Chunk number.
            title (str): Slide title.
            text (str): Chunk text.
            embedding (numpy.ndarray): Embedding vector.
            source_type (str): Source document type.
            language (str): Document language.
            metadata (dict): Additional metadata.
            similarity_score (float): Search similarity/distance score.
        """

        self.manual_name = manual_name
        self.slide_number = slide_number
        self.chunk_number = chunk_number
        self.title = title
        self.text = text
        self.embedding = embedding

        self.source_type = source_type
        self.language = language
        self.metadata = metadata if metadata is not None else {}

        # Added for Semantic Search
        self.similarity_score = similarity_score

    def __repr__(self):
        return (
            f"EmbeddingDocument("
            f"manual='{self.manual_name}', "
            f"slide={self.slide_number}, "
            f"chunk={self.chunk_number}, "
            f"title='{self.title}')"
        )