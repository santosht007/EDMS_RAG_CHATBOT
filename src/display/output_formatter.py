class OutputFormatter:
    """
    Handles all console output formatting for the EDMS AI Assistant.
    """

    LINE = "=" * 70
    SUB_LINE = "-" * 70

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    @staticmethod
    def print_header(title):

        print()
        print(OutputFormatter.LINE)
        print(title)
        print(OutputFormatter.LINE)

    # --------------------------------------------------
    # Sub Header
    # --------------------------------------------------

    @staticmethod
    def print_sub_header(title):

        print()
        print(OutputFormatter.SUB_LINE)
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
    # AI Answer
    # --------------------------------------------------

    @staticmethod
    def display_answer(answer):

        OutputFormatter.print_header("EDMS AI ANSWER")

        print(answer)

    # --------------------------------------------------
    # Reference Documents
    # --------------------------------------------------

    @staticmethod
    def display_references(documents):
        """
        Display unique reference documents.

        Duplicate definition:
            Same Manual + Same Slide
        """

        OutputFormatter.print_header("REFERENCE DOCUMENTS")

        if not documents:

            print("No reference documents found.")
            return

        # ---------------------------------------------
        # Remove duplicates
        # ---------------------------------------------

        unique_documents = {}

        for doc in documents:

            key = (
                doc.manual_name,
                doc.slide_number
            )

            if key not in unique_documents:

                unique_documents[key] = doc

        # ---------------------------------------------
        # Sort references
        # ---------------------------------------------

        sorted_documents = sorted(
            unique_documents.values(),
            key=lambda d: (
                d.manual_name.lower(),
                d.slide_number
            )
        )

        # ---------------------------------------------
        # Print references
        # ---------------------------------------------

        for index, doc in enumerate(sorted_documents, start=1):

            print(f"[{index}]")

            print(f"Manual : {doc.manual_name}")

            print(f"Slide  : {doc.slide_number}")

            print(f"Title  : {doc.title}")

            if hasattr(doc, "similarity_score"):

                print(f"Similarity Score : {doc.similarity_score:.4f}")

            print()

    # --------------------------------------------------
    # Goodbye
    # --------------------------------------------------

    @staticmethod
    def goodbye():

        print()

        print(OutputFormatter.LINE)

        print("Thank you for using EDMS AI Assistant.")

        print(OutputFormatter.LINE)