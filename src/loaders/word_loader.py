from pathlib import Path
from docx import Document

from config import SUPPORTED_WORD


class WordLoader:
    """
    Loads Microsoft Word (.docx) documents.
    """

    def __init__(self, docx_directory):

        self.docx_directory = Path(docx_directory)


    # --------------------------------------------------
    # Get Word Files
    # --------------------------------------------------

    def get_word_files(self):
        """
        Returns all supported Word documents.
        """

        word_files = []

        for extension in SUPPORTED_WORD:

            word_files.extend(
                self.docx_directory.glob(f"*{extension}")
            )

        return sorted(word_files)


    # --------------------------------------------------
    # Load Word Document
    # --------------------------------------------------

    def load_document(self, file_path):
        """
        Loads a Word document.
        """

        try:

            return Document(file_path)

        except Exception as e:

            print(f"Unable to load {file_path.name}")
            print(e)

            return None


    # --------------------------------------------------
    # Check TOC Number Pattern
    # --------------------------------------------------

    def is_toc_number_line(self, text):
        """
        Checks whether the text looks like a Table Of Contents entry.
        """

        toc_symbols = (
            "①",
            "②",
            "③",
            "④",
            "⑤",
            "⑥",
            "⑦",
            "⑧",
            "⑨",
            "⑩",
            "⑪",
            "⑫",
            "⑬",
            "⑭",
            "⑮"
        )


        if text.startswith(toc_symbols):

            return True


        if text[0].isdigit():

            return True


        return False



    # --------------------------------------------------
    # Extract Text with Smart TOC Detection
    # --------------------------------------------------

    def extract_text(self, document):
        """
        Extract text from Word document.

        Features:
        - Preserves headings
        - Removes TOC entries
        - Supports EDMS manuals
        """

        paragraphs = []

        toc_mode = False


        toc_keywords = [

            "pre-requisites",
            "prerequisites",
            "functions on home page",
            "history",
            "favorites",
            "tasks",
            "reports",
            "clipboard",
            "trash",
            "bizadmin",
            "administration",
            "profile",
            "faq"

        ]


        for paragraph in document.paragraphs:


            text = paragraph.text.strip()


            if not text:

                continue


            lower_text = text.lower()



            # ----------------------------------
            # Detect explicit TOC
            # ----------------------------------

            if "table of contents" in lower_text:

                toc_mode = True

                continue



            # ----------------------------------
            # Detect TOC numbered items
            # ----------------------------------

            if self.is_toc_number_line(text):

                toc_mode = True

                continue



            # ----------------------------------
            # Detect TOC keyword items
            # ----------------------------------

            if lower_text in toc_keywords:

                toc_mode = True

                continue



            # ----------------------------------
            # Skip TOC area
            # ----------------------------------

            if toc_mode:


                # Actual content indicators

                if (

                    len(text) > 50
                    or
                    "important" in lower_text
                    or
                    "click" in lower_text
                    or
                    "select" in lower_text
                    or
                    "screen" in lower_text

                ):

                    toc_mode = False


                else:

                    continue



            # ----------------------------------
            # Preserve Heading Information
            # ----------------------------------

            style_name = paragraph.style.name


            if style_name.startswith("Heading"):


                paragraphs.append(
                    f"\nSECTION: {text}\n"
                )


            else:

                paragraphs.append(text)



        return "\n".join(paragraphs)