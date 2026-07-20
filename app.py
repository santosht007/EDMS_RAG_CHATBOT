"""
============================================================
EDMS AI Assistant
Version : 2.3
============================================================
"""

from config import EMBEDDING_DIMENSION

from src.embeddings.embedding_model import EmbeddingModel
from src.vectorstore.faiss_manager import FAISSManager
from src.vectorstore.search_engine import SearchEngine

from src.llm.ollama_client import OllamaClient
from src.llm.prompt_builder import PromptBuilder

from src.display.output_formatter import OutputFormatter
from src.memory.conversation_memory import ConversationMemory


# ==========================================================
# Application Header
# ==========================================================

OutputFormatter.print_header("EDMS AI Assistant")
print("Version 2.3")


# ==========================================================
# Load Embedding Model
# ==========================================================

embedding_model = EmbeddingModel()
model = embedding_model.load_model()

print("✓ Embedding Model Ready.")


# ==========================================================
# Load FAISS Index
# ==========================================================

print("\nLoading FAISS Index...")

faiss_manager = FAISSManager(
    EMBEDDING_DIMENSION
)

faiss_manager.load_index()
faiss_manager.load_metadata()

print(f"✓ Loaded {faiss_manager.total_vectors()} document chunks.")


# ==========================================================
# Initialize Search Engine
# ==========================================================

print("\nInitializing Search Engine...")

search_engine = SearchEngine(
    embedding_model=model,
    faiss_manager=faiss_manager
)

print("✓ Search Engine Ready.")


# ==========================================================
# Connect to Ollama
# ==========================================================

print("\nConnecting to Ollama...")

llm = OllamaClient()

if llm.test_connection():

    print("✓ Connected Successfully.")

else:

    raise SystemExit(
        "\n❌ Cannot connect to Ollama.\n"
        "Please make sure Ollama is running."
    )


# ==========================================================
# Initialize Conversation Memory
# ==========================================================

print("\nInitializing Conversation Memory...")

memory = ConversationMemory(
    embedding_model=model,
    max_history=5
)

print("✓ Conversation Memory Ready.")


# ==========================================================
# Chat Loop
# ==========================================================

OutputFormatter.print_header("EDMS AI Chat")

while True:

    question = input(
        "\nAsk EDMS (type 'exit' to quit): "
    ).strip()

    # ------------------------------------------------------

    if question.lower() in [
        "exit",
        "quit",
        "bye"
    ]:

        OutputFormatter.goodbye()
        break

    # ------------------------------------------------------

    if not question:

        continue

    # ------------------------------------------------------
    # Display Question
    # ------------------------------------------------------

    OutputFormatter.display_question(question)

    # ------------------------------------------------------
    # Search Documents
    # ------------------------------------------------------

    results = search_engine.search(
        query=question,
        top_k=5
    )

    if not results:

        print("\nNo relevant documents found.")
        continue

    # ------------------------------------------------------
    # Conversation Memory
    # ------------------------------------------------------

    if memory.is_follow_up(question):

        print("\nUsing previous conversation...")

        conversation_history = memory.get_recent_history(3)

    else:

        print("\nStarting a new conversation...")

        conversation_history = []

    # ------------------------------------------------------
    # Build Prompt
    # ------------------------------------------------------

    prompt = PromptBuilder.build_prompt(
        question=question,
        documents=results,
        conversation_history=conversation_history
    )

    # ------------------------------------------------------
    # Generate Answer
    # ------------------------------------------------------

    OutputFormatter.print_sub_header(
        "Generating Answer..."
    )

    answer = llm.generate(prompt)

    # ------------------------------------------------------
    # Save Conversation
    # ------------------------------------------------------

    memory.add_interaction(
        question=question,
        answer=answer
    )

    # ------------------------------------------------------
    # Display Answer
    # ------------------------------------------------------

    OutputFormatter.display_answer(answer)

    # ------------------------------------------------------
    # Display References
    # ------------------------------------------------------

    OutputFormatter.display_references(results)