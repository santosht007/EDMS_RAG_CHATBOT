"""
Document Cleaner

Cleans raw text extracted from PowerPoint and Word documents
before chunking and FAISS indexing.

Version: 4.0
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

        text = DocumentCleaner.remove_toc_sections(text)

        text = DocumentCleaner.normalize_title(text)


        return text.strip()



    # ==================================================
    # Remove Extra Spaces
    # ==================================================

    @staticmethod
    def remove_extra_spaces(text):

        """
        Replace multiple spaces/tabs with one space.
        """

        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        return text



    # ==================================================
    # Remove Blank Lines
    # ==================================================

    @staticmethod
    def remove_extra_blank_lines(text):

        """
        Reduce multiple blank lines.
        """

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )

        return text



    # ==================================================
    # Fix Duplicate Numbering
    # ==================================================

    @staticmethod
    def fix_duplicate_numbering(text):

        """
        Converts:

        ①
        ① Click

        into:

        ① Click
        """

        numbers = (
            "①②③④⑤⑥⑦⑧⑨⑩"
        )


        for number in numbers:

            pattern = rf"{number}\s*\n\s*{number}"

            replacement = f"{number} "


            text = re.sub(
                pattern,
                replacement,
                text
            )


        return text



    # ==================================================
    # Fix Duplicate Bullets
    # ==================================================

    @staticmethod
    def fix_duplicate_bullets(text):

        """
        Converts:

        •
        • Upload

        into:

        • Upload
        """

        text = re.sub(
            r"•\s*\n\s*•",
            "• ",
            text
        )


        return text



    # ==================================================
    # Remove Table Of Contents
    # ==================================================

    @staticmethod
    def remove_toc_sections(text):

        """
        Removes Table Of Contents noise.

        Example removed:

        Table Of Contents

        1.ED Introduction
        2.Pre-requisites
        3.Registration


        Keeps:

        Actual procedure descriptions.
        """


        lines = text.splitlines()


        cleaned = []


        skip_mode = False



        for line in lines:


            clean_line = line.strip()



            if not clean_line:

                continue



            lower = clean_line.lower()



            # ------------------------------------------
            # Detect TOC header
            # ------------------------------------------

            if (
                "table of contents" in lower
                or
                lower == "contents"
            ):

                skip_mode = True

                continue



            # ------------------------------------------
            # Remove TOC numbered entries
            # ------------------------------------------

            if skip_mode:


                # Examples:
                # 1. ED Introduction
                # 2-1 URL and Signing In
                # 3. Registration


                if re.match(
                    r"^\d+([.-]\d+)?[\s\.\-]",
                    clean_line
                ):

                    continue



                # Stop skipping when real text starts

                if (
                    len(clean_line) > 80
                    or
                    clean_line.endswith(".")
                ):

                    skip_mode = False



            cleaned.append(
                clean_line
            )


        return "\n".join(cleaned)



    # ==================================================
    # Normalize Title
    # ==================================================

    @staticmethod
    def normalize_title(text):

        """
        Removes numbering from first title.

        Example:

        2.Edit Document Attribute

        becomes:

        Edit Document Attribute
        """


        lines = text.splitlines()


        cleaned = []


        first_line = True



        for line in lines:


            if first_line:


                line = re.sub(
                    r"^\d+[\.\-:\s]+",
                    "",
                    line
                )


                first_line = False



            cleaned.append(
                line
            )


        return "\n".join(cleaned)