from src.models.slide_document import SlideDocument

from src.loaders.powerpoint_loader import PowerPointLoader
from src.loaders.word_loader import WordLoader

from src.preprocessing.document_cleaner import DocumentCleaner

from config import PPT_DIR, DOCX_DIR

import re


class DocumentParser:
    """
    Parses different document types into a common format.

    Supports:
        • PowerPoint
        • Word Manuals
        • FAQ Documents (Question / Answer / Category)
    """

    def __init__(self):

        self.cleaner = DocumentCleaner()

    # ==================================================
    # Parse PowerPoint
    # ==================================================

    def parse_powerpoint(self, ppt_directory):

        loader = PowerPointLoader(
            ppt_directory
        )

        ppt_files = loader.get_ppt_files()

        documents = []

        for ppt in ppt_files:

            presentation = loader.load_presentation(
                ppt
            )

            if presentation is None:
                continue

            for slide_number, slide in enumerate(
                presentation.slides,
                start=1
            ):

                slide_text = loader.extract_slide_text(
                    slide
                )

                slide_text = self.cleaner.clean(
                    slide_text
                )

                if not slide_text.strip():
                    continue

                lines = slide_text.split("\n")

                title = (
                    lines[0].strip()
                    if lines
                    else ""
                )

                documents.append(

                    SlideDocument(

                        manual_name=ppt.name,

                        slide_number=slide_number,

                        title=title,

                        text=slide_text,

                        source_type="ppt"

                    )

                )

        return documents

    # ==================================================
    # FAQ Detection
    # ==================================================

    def is_faq_document(
        self,
        text
    ):
        """
        Detect whether this Word file
        is an FAQ document.
        """

        question_count = len(
            re.findall(
                r"Question\s*:",
                text,
                flags=re.IGNORECASE
            )
        )

        answer_count = len(
            re.findall(
                r"Answer\s*:",
                text,
                flags=re.IGNORECASE
            )
        )

        return (
            question_count >= 3
            and
            answer_count >= 3
        )

    # ==================================================
    # Parse FAQ Document
    # ==================================================

    def parse_faq_document(
        self,
        word_file,
        word_text
    ):

        """
        Creates ONE SlideDocument
        per FAQ.

        Question
        Answer
        Category
        """

        documents = []

        pattern = re.compile(

            r"""
            Question\s*:\s*
            (.*?)

            Answer\s*:\s*
            (.*?)

            Category\s*:\s*
            (.*?)

            (?=
                Question\s*:
                |
                $
            )
            """,

            re.IGNORECASE
            |
            re.DOTALL
            |
            re.VERBOSE

        )

        matches = list(
            pattern.finditer(
                word_text
            )
        )

        print(
            f"Detected {len(matches)} FAQ entries in {word_file.name}"
        )

        for index, match in enumerate(
            matches,
            start=1
        ):

            question = (
                match.group(1).strip()
            )

            answer = (
                match.group(2).strip()
            )

            category = (
                match.group(3).strip()
            )

            faq_text = (

                f"Question:\n"
                f"{question}\n\n"

                f"Answer:\n"
                f"{answer}\n\n"

                f"Category:\n"
                f"{category}"

            )

            documents.append(

                SlideDocument(

                    manual_name=word_file.name,

                    slide_number=index,

                    title=question,

                    text=faq_text,

                    source_type="docx",

                    section=category

                )

            )

        return documents

    # ==================================================
    # Parse Word
    # ==================================================

    def parse_word(self, word_directory):

        """
        Parse Word documents.

        Supports:
            • FAQ documents
            • Normal manuals
        """

        loader = WordLoader(
            word_directory
        )

        word_files = loader.get_word_files()

        documents = []

        for word_file in word_files:

            word_document = loader.load_document(
                word_file
            )

            if word_document is None:
                continue

            word_text = loader.extract_text(
                word_document
            )

            word_text = self.cleaner.clean(
                word_text
            )

            print("\n" + "=" * 80)
            print(f"FILE: {word_file.name}")
            print("=" * 80)
            print(word_text)
            print("=" * 80 + "\n")

            if not word_text.strip():
                continue

            # ------------------------------------------
            # FAQ document
            # ------------------------------------------

            if self.is_faq_document(
                word_text
            ):

                print(
                    f"FAQ detected : {word_file.name}"
                )

                faq_documents = self.parse_faq_document(
                    word_file,
                    word_text
                )

                documents.extend(
                    faq_documents
                )

            # ------------------------------------------
            # Normal Word Manual
            # ------------------------------------------

            else:

                lines = word_text.split("\n")

                title = (
                    lines[0].strip()
                    if lines
                    else ""
                )

                documents.append(

                    SlideDocument(

                        manual_name=word_file.name,

                        slide_number=1,

                        title=title,

                        text=word_text,

                        source_type="docx"

                    )

                )

        return documents

    # ==================================================
    # Parse All Documents
    # ==================================================

    def parse_all_documents(self):

        """
        Parse all supported documents.
        """

        all_documents = []

        print("\nLoading PowerPoint manuals...")

        ppt_documents = self.parse_powerpoint(
            PPT_DIR
        )

        print(
            f"PowerPoint documents loaded: {len(ppt_documents)}"
        )

        all_documents.extend(
            ppt_documents
        )

        print("\nLoading Word manuals...")

        word_documents = self.parse_word(
            DOCX_DIR
        )

        print(
            f"Word documents loaded: {len(word_documents)}"
        )

        all_documents.extend(
            word_documents
        )

        print(
            f"\nTotal documents loaded: {len(all_documents)}"
        )

        return all_documents

    # ==================================================
    # Future PDF Support
    # ==================================================

    def parse_pdf(self):

        pass