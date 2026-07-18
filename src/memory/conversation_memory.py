from collections import deque
import numpy as np

from src.memory.conversation import Conversation


class ConversationMemory:
    """
    Stores recent conversations between the user and the AI.
    """

    FOLLOW_UP_KEYWORDS = {
        "it",
        "that",
        "this",
        "they",
        "them",
        "those",
        "these",
        "again",
        "same",
        "then",
        "after",
        "before",
        "next",
        "previous",
        "above",
        "can i",
        "is it",
        "does it",
        "what if",
        "how about",
        "after that",
        "before that"
    }

    # --------------------------------------------------
    # Constructor
    # --------------------------------------------------

    def __init__(self, embedding_model, max_history=5):

        self.embedding_model = embedding_model

        self.max_history = max_history

        self.history = deque(maxlen=max_history)

    # --------------------------------------------------
    # Add Conversation
    # --------------------------------------------------

    def add_interaction(self, question, answer):
        """
        Store one conversation together with
        its embedding.
        """

        question_embedding = self.embedding_model.encode(question)

        conversation = Conversation(
            question=question,
            answer=answer,
            embedding=question_embedding
        )

        self.history.append(conversation)

    # --------------------------------------------------
    # Get History
    # --------------------------------------------------

    def get_history(self):

        return list(self.history)

    # --------------------------------------------------
    # Get Recent History
    # --------------------------------------------------

    def get_recent_history(self, count=3):

        return list(self.history)[-count:]

    # --------------------------------------------------
    # Get Formatted History
    # --------------------------------------------------

    def get_formatted_history(self, count=3):

        history = self.get_recent_history(count)

        if not history:
            return ""

        formatted = ""

        for conversation in history:

            formatted += f"""
User:
{conversation.question}

Assistant:
{conversation.answer}

------------------------------------------------------------

"""

        return formatted.strip()

    # --------------------------------------------------
    # Get Last Question
    # --------------------------------------------------

    def get_last_question(self):

        if self.is_empty():
            return None

        return self.history[-1].question

    # --------------------------------------------------
    # Is Empty
    # --------------------------------------------------

    def is_empty(self):

        return len(self.history) == 0

    # --------------------------------------------------
    # Temporary Keyword Detection
    # --------------------------------------------------

    def is_follow_up(self, question):
        """
        Temporary keyword-based detection.

        This will be removed in Part 3.4.6.4.
        """

        if self.is_empty():
            return False

        question = question.lower()

        for keyword in self.FOLLOW_UP_KEYWORDS:

            if keyword in question:
                return True

        return False

    # --------------------------------------------------
    # Get Embeddings
    # --------------------------------------------------

    def get_embeddings(self):

        return [
            conversation.embedding
            for conversation in self.history
        ]

    # --------------------------------------------------
    # Cosine Similarity
    # --------------------------------------------------

    def cosine_similarity(
        self,
        embedding1,
        embedding2
    ):
        """
        Compute cosine similarity
        between two embeddings.
        """

        numerator = np.dot(
            embedding1,
            embedding2
        )

        denominator = (
            np.linalg.norm(embedding1)
            *
            np.linalg.norm(embedding2)
        )

        if denominator == 0:

            return 0.0

        return float(
            numerator / denominator
        )

    # --------------------------------------------------
    # Find Similar Conversations
    # --------------------------------------------------

    def find_similar_conversations(
        self,
        question,
        top_k=3,
        threshold=0.70
    ):
        """
        Return semantically similar conversations.
        """

        if self.is_empty():
            return []

        question_embedding = self.embedding_model.encode(question)

        similarities = []

        for conversation in self.history:

            score = self.cosine_similarity(
                question_embedding,
                conversation.embedding
            )

            similarities.append(
                (
                    score,
                    conversation
                )
            )

        similarities.sort(
            key=lambda x: x[0],
            reverse=True
        )

        results = []

        for score, conversation in similarities:

            if score >= threshold:

                results.append(
                    (
                        score,
                        conversation
                    )
                )

            if len(results) >= top_k:

                break

        return results

    # --------------------------------------------------
    # Has Similar Conversation
    # --------------------------------------------------

    def has_similar_conversation(
        self,
        question,
        threshold=0.70
    ):
        """
        Returns True if a similar
        conversation exists.
        """

        results = self.find_similar_conversations(
            question,
            top_k=1,
            threshold=threshold
        )

        return len(results) > 0

    # --------------------------------------------------
    # Clear Memory
    # --------------------------------------------------

    def clear(self):

        self.history.clear()

    # --------------------------------------------------
    # Memory Size
    # --------------------------------------------------

    def size(self):

        return len(self.history)