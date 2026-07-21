from src.models.slide_document import SlideDocument
from src.loaders.powerpoint_loader import PowerPointLoader
from src.preprocessing.document_cleaner import DocumentCleaner


class DocumentParser:
    """
    Parses different document types into a common format.
    """

    def __init__(self):

        # Initialize the new document cleaner
        self.cleaner = DocumentCleaner()

    # ----------------------------------------
    # Parse PowerPoint
    # ----------------------------------------

    def parse_powerpoint(self, ppt_directory):
        """
        Parse all PowerPoint manuals into SlideDocument objects.
        """

        loader = PowerPointLoader(ppt_directory)

        ppt_files = loader.get_ppt_files()

        documents = []

        for ppt in ppt_files:

            presentation = loader.load_presentation(ppt)

            if presentation is None:
                continue

            # Read every slide
            for slide_number, slide in enumerate(
                presentation.slides,
                start=1
            ):

                # ----------------------------------
                # Extract raw text
                # ----------------------------------

                slide_text = loader.extract_slide_text(slide)

                # ----------------------------------
                # Clean extracted text
                # ----------------------------------

                slide_text = self.cleaner.clean(slide_text)

                # Skip empty slides
                if not slide_text.strip():
                    continue

                # ----------------------------------
                # Title
                # ----------------------------------

                lines = slide_text.split("\n")

                title = lines[0].strip() if lines else ""

                # ----------------------------------
                # Create SlideDocument
                # ----------------------------------

                document = SlideDocument(
                    manual_name=ppt.name,
                    slide_number=slide_number,
                    title=title,
                    text=slide_text
                )

                documents.append(document)

        return documents

    # ----------------------------------------
    # Future
    # ----------------------------------------

    def parse_pdf(self):
        pass

    def parse_word(self):
        pass

    def create_document(self):
        pass