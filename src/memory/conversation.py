from dataclasses import dataclass, field
from datetime import datetime
import numpy as np


@dataclass
class Conversation:
    """
    Represents one conversation between the user and the AI.
    """

    question: str
    answer: str
    embedding: np.ndarray | None = None
    timestamp: datetime = field(default_factory=datetime.now)