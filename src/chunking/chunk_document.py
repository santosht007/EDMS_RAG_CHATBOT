from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ChunkDocument:
    """
    Represents one searchable chunk of knowledge.
    """

    # ==========================================================
    # Source Information
    # ==========================================================

    manual_name: str
    slide_number: int
    chunk_number: int

    # ==========================================================
    # Content
    # ==========================================================

    title: str
    text: str

    # ==========================================================
    # Document Information
    # ==========================================================

    source_type: str = "PowerPoint"
    language: str = "English"

    # ==========================================================
    # AI Metadata
    # ==========================================================

    keywords: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    # ==========================================================
    # Future Extensions
    # ==========================================================

    image_paths: List[str] = field(default_factory=list)

    related_documents: List[str] = field(default_factory=list)