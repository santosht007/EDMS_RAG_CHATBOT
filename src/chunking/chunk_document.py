"""
Chunk Document Model

Represents one searchable text chunk generated
from PowerPoint, Word, or PDF documents.

Used by:
    TextChunker
        |
        ↓
    EmbeddingGenerator
        |
        ↓
    FAISS Index

Version: 1.1
"""


from dataclasses import dataclass, field
from typing import Optional



@dataclass
class ChunkDocument:
    """
    Represents one chunk generated from a document.
    """


    # ------------------------------------------
    # Source Information
    # ------------------------------------------

    manual_name: str

    # PPT uses slide number
    # DOCX/PDF can be None
    slide_number: Optional[int]


    chunk_number: int



    # ------------------------------------------
    # Content Information
    # ------------------------------------------

    title: str

    text: str



    # ------------------------------------------
    # Document Metadata
    # ------------------------------------------

    source_type: str = "PowerPoint"

    language: str = "English"



    metadata: dict = field(
        default_factory=dict
    )