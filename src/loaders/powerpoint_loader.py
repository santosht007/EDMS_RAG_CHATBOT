from pathlib import Path
from pptx import Presentation


class PowerPointLoader:
    """
    PowerPoint Loader

    Responsible for:
    - Finding PowerPoint files
    - Opening presentations
    - Extracting text
    - Extracting tables
    - Extracting images
    - Extracting metadata
    """

    def __init__(self, ppt_directory):
        """
        Initialize the loader.

        Args:
            ppt_directory (Path): Folder containing PowerPoint manuals.
        """
        self.ppt_directory = Path(ppt_directory)

    # --------------------------------------------------
    # Step 1 : Find all PowerPoint files
    # --------------------------------------------------
    def get_ppt_files(self):
        """
        Returns a list of PowerPoint files.
        """
        return list(self.ppt_directory.glob("*.pptx"))

    # --------------------------------------------------
    # Step 2 : Open a PowerPoint presentation
    # --------------------------------------------------
    def load_presentation(self, ppt_file):
        """
        Opens a PowerPoint presentation.

        Args:
            ppt_file (Path): PowerPoint file

        Returns:
            Presentation object
        """

        try:
            presentation = Presentation(ppt_file)
            return presentation

        except Exception as e:
            print(f"Error opening {ppt_file.name}: {e}")
            return None

    # --------------------------------------------------
    # Step 3 : Extract text from one slide
    # --------------------------------------------------
    def extract_slide_text(self, slide):
        """
        Extract all text from one PowerPoint slide.

        Args:
            slide : PowerPoint Slide

        Returns:
            str : Combined slide text
        """

        text = []

        for shape in slide.shapes:

            if hasattr(shape, "text"):

                if shape.text.strip():

                    text.append(shape.text.strip())

        return "\n".join(text)

    # --------------------------------------------------
    # Step 4 : Extract images from one slide
    # --------------------------------------------------
    def extract_slide_images(self, slide):
        """
        Extract images from a slide.
        """
        pass

    # --------------------------------------------------
    # Step 5 : Extract tables from one slide
    # --------------------------------------------------
    def extract_slide_tables(self, slide):
        """
        Extract tables from a slide.
        """
        pass

    # --------------------------------------------------
    # Step 6 : Extract metadata
    # --------------------------------------------------
    def extract_metadata(self, presentation):
        """
        Extract PowerPoint metadata.
        """
        pass