from dataclasses import dataclass, field


@dataclass
class ChunkDocument:
    """
    Represents one chunk generated from a document.

    This object is passed from the TextChunker to the
    EmbeddingGenerator before being converted into an
    EmbeddingDocument.
    """

    manual_name: str
    slide_number: int
    chunk_number: int

    title: str
    text: str

    source_type: str = "PowerPoint"
    language: str = "English"

    metadata: dict = field(default_factory=dict)