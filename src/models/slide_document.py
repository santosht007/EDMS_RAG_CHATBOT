from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SlideDocument:
    """
    Represents a document unit from PowerPoint, Word, or PDF.
    """

    manual_name: str

    # PowerPoint slide number
    # Word/PDF can keep this as None
    slide_number: Optional[int]

    title: str
    text: str

    # Document source information
    source_type: str = "ppt"

    # Word heading / PDF section information
    section: str = ""

    heading_level: Optional[int] = None

    # Existing multimedia support
    images: List[str] = field(default_factory=list)

    tables: List[str] = field(default_factory=list)

    notes: str = ""

    language: str = "English"