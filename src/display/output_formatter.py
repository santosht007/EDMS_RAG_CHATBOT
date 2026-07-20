from collections import defaultdict


class OutputFormatter:
    """
    Handles all console output formatting for the EDMS AI Chatbot.
    """

    LINE = "-" * 60

    # --------------------------------------------------
    # Startup Screen
    # --------------------------------------------------

    @staticmethod
    def display_startup(
        embedding_model="all-MiniLM-L6-v2",
        chunk_count=0,
        llm_model="llama3.2:3b"
    ):
        """
        Display chatbot startup dashboard.
        """

        print()
        print(OutputFormatter.LINE)
        print("  EDMS_AI_chatbot")
        print(OutputFormatter.LINE)
        print()

        print("Initializing AI Components...\n")

        print("[✓] Embedding Model")
        print("Engine : Sentence Transformers")
        print(f"Model  : {embedding_model}")
        print()

        print("[✓] Vector Database")
        print("Engine : FAISS")
        print(f"Indexed Chunks : {chunk_count}")
        print()

        print("[✓] Semantic Search Engine")
        print("Status : Ready")
        print()

        print("[✓] Large Language Model")
        print("Engine : Ollama")
        print(f"Model  : {llm_model}")
        print("Status : Connected")
        print()

        print("[✓] Conversation Memory")
        print("Status : Active")
        print()

        print(OutputFormatter.LINE)
        print("System Status : READY")
        print(OutputFormatter.LINE)
        print()

        print("Hello, I am EDMS_AI_chatbot.")
        print()
        print("Thank you for contacting me.")
        print()
        print("I can assist you with EDMS manuals, procedures,")
        print("workflows, and document-related questions.")
        print()
        print("How may I help you?")

    # --------------------------------------------------
    # Answer
    # --------------------------------------------------

    @staticmethod
    def display_answer(answer):
        """
        Display only the chatbot answer.
        """
        print()
        print(answer)
        print()

    # --------------------------------------------------
    # References
    # --------------------------------------------------

    @staticmethod
    def display_references(results):
        """
        Display consolidated reference documents.
        """

        manuals = defaultdict(set)

        for doc in results:
            manuals[doc.manual_name].add(doc.slide_number)

        print("Reference:\n")

        for manual, slides in manuals.items():

            slide_numbers = sorted(slides)

            slide_text = ", ".join(
                str(slide)
                for slide in slide_numbers
            )

            print(f"Manual : {manual}")
            print(f"Slides : {slide_text}")
            print()

    # --------------------------------------------------
    # Status Messages
    # --------------------------------------------------

    @staticmethod
    def info(message):
        print(f"[INFO] {message}")

    @staticmethod
    def success(message):
        print(f"[SUCCESS] {message}")

    @staticmethod
    def warning(message):
        print(f"[WARNING] {message}")

    @staticmethod
    def error(message):
        print(f"[ERROR] {message}")

    # --------------------------------------------------
    # Goodbye
    # --------------------------------------------------

    @staticmethod
    def goodbye():

        print()
        print("Thank you for using EDMS_AI_chatbot.")
        print("Goodbye!")