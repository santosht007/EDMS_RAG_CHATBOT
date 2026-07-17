import re


class TextCleaner:
    """
    Cleans text extracted from manuals.
    """

    def clean(self, text: str) -> str:
        """
        Clean extracted text.

        Args:
            text (str)

        Returns:
            Cleaned text
        """

        if not text:
            return ""

        # Convert tabs to spaces
        text = text.replace("\t", " ")

        # Remove extra spaces
        text = re.sub(r"[ ]+", " ", text)

        # Remove multiple blank lines
        text = re.sub(r"\n{2,}", "\n\n", text)

        # Remove leading/trailing spaces
        text = text.strip()

        return text