from dataclasses import dataclass, field
from typing import List


@dataclass
class SlideDocument:
    """
    Represents one PowerPoint slide.
    """

    manual_name: str
    slide_number: int

    title: str
    text: str

    images: List[str] = field(default_factory=list)
    tables: List[str] = field(default_factory=list)

    notes: str = ""

    language: str = "English"