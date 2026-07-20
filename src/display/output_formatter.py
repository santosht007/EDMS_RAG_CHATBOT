from src.utils.source_manager import SourceManager


class OutputFormatter:
    """
    Handles all console output formatting for the EDMS AI Assistant.
    """

    LINE = "=" * 70
    SUB_LINE = "-" * 70

    # --------------------------------------------------
    # Headers
    # --------------------------------------------------

    @staticmethod
    def print_header(title):

        print("\n" + OutputFormatter.LINE)
        print(title)
        print(OutputFormatter.LINE)

    @staticmethod
    def print_sub_header(title):

        print("\n" + OutputFormatter.SUB_LINE)
        print(title)
        print(OutputFormatter.SUB_LINE)

    # --------------------------------------------------
    # Question
    # --------------------------------------------------

    @staticmethod
    def display_question(question):

        OutputFormatter.print_header("QUESTION")
        print(question)

    # --------------------------------------------------
    # Answer
    # --------------------------------------------------

    @staticmethod
    def display_answer(answer):

        OutputFormatter.print_header("EDMS AI ANSWER")
        print(answer)

    # --------------------------------------------------
    # Intelligent Source Display
    # --------------------------------------------------

    @staticmethod
    def display_references(results):

        OutputFormatter.print_header("SOURCE DOCUMENTS")

        grouped_sources = SourceManager.organize_sources(results)

        for manual, slides in grouped_sources.items():

            print(f"Manual : {manual}")

            ordered_slides = sorted(slides)

            slide_text = ", ".join(
                str(slide)
                for slide in ordered_slides
            )

            print(f"Slides : {slide_text}")
            print()

    # --------------------------------------------------
    # Status Messages
    # --------------------------------------------------

    @staticmethod
    def info(message):

        print(f"\n[INFO] {message}")

    @staticmethod
    def success(message):

        print(f"\n[SUCCESS] {message}")

    @staticmethod
    def warning(message):

        print(f"\n[WARNING] {message}")

    @staticmethod
    def error(message):

        print(f"\n[ERROR] {message}")

    # --------------------------------------------------
    # Goodbye
    # --------------------------------------------------

    @staticmethod
    def goodbye():

        print("\nThank you for using EDMS AI Assistant.")
        print("Goodbye!")