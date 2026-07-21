"""
Document Cleaner

This module cleans raw text extracted from PowerPoint slides
before it is chunked and indexed into FAISS.

Version: 3.0
"""


import re


class DocumentCleaner:
    """
    Cleans extracted document text.
    """

    @staticmethod
    def clean(text: str) -> str:
        """
        Main cleaning pipeline.
        """

        if not text:
            return ""

        text = DocumentCleaner.remove_extra_spaces(text)
        text = DocumentCleaner.remove_extra_blank_lines(text)
        text = DocumentCleaner.fix_duplicate_numbering(text)
        text = DocumentCleaner.fix_duplicate_bullets(text)
        text = DocumentCleaner.normalize_title(text)

        return text.strip()

    # --------------------------------------------------

    @staticmethod
    def remove_extra_spaces(text):

        # Replace multiple spaces/tabs with one space
        text = re.sub(r"[ \t]+", " ", text)

        return text

    # --------------------------------------------------

    @staticmethod
    def remove_extra_blank_lines(text):

        # Reduce multiple blank lines to one
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text

    # --------------------------------------------------

    @staticmethod
    def fix_duplicate_numbering(text):
        """
        Converts

        ①
        ①Click...

        into

        ① Click...
        """

        numbers = "①②③④⑤⑥⑦⑧⑨⑩"

        for n in numbers:

            pattern = rf"{n}\s*\n\s*{n}"
            replacement = f"{n} "

            text = re.sub(pattern, replacement, text)

        return text

    # --------------------------------------------------

    @staticmethod
    def fix_duplicate_bullets(text):
        """
        Converts

        •
        •Upload

        into

        • Upload
        """

        text = re.sub(
            r"•\s*\n\s*•",
            "• ",
            text
        )

        return text

    # --------------------------------------------------

    @staticmethod
    def normalize_title(text):
        """
        Removes numbering from slide titles.

        Example

        2.Edit Document attribute

        becomes

        Edit Document attribute
        """

        lines = text.splitlines()

        cleaned = []

        first_title_cleaned = False

        for line in lines:

            if not first_title_cleaned:

                line = re.sub(
                    r"^\d+[\.\-: ]+",
                    "",
                    line
                )

                first_title_cleaned = True

            cleaned.append(line)

        return "\n".join(cleaned)