from config import EMBEDDING_DIMENSION

from src.embeddings.embedding_model import EmbeddingModel
from src.vectorstore.faiss_manager import FAISSManager
from src.vectorstore.search_engine import SearchEngine
from src.llm.ollama_client import OllamaClient
from src.llm.prompt_builder import PromptBuilder
from src.display.output_formatter import OutputFormatter
from src.memory.conversation_memory import ConversationMemory


# ==================================================
# Initialize Embedding Model
# ==================================================

embedding_model = EmbeddingModel()
model = embedding_model.load_model()


# ==================================================
# Load FAISS
# ==================================================

faiss_manager = FAISSManager(EMBEDDING_DIMENSION)
faiss_manager.load_index()
faiss_manager.load_metadata()


# ==================================================
# Search Engine
# ==================================================

search_engine = SearchEngine(
    embedding_model=model,
    faiss_manager=faiss_manager
)


# ==================================================
# Large Language Model
# ==================================================

llm = OllamaClient()

if not llm.test_connection():
    raise SystemExit("Unable to connect to Ollama.")


# ==================================================
# Conversation Memory
# ==================================================

memory = ConversationMemory(
    embedding_model=model,
    max_history=5
)


# ==================================================
# Startup Screen
# ==================================================

OutputFormatter.display_startup(
    embedding_model="all-MiniLM-L6-v2",
    chunk_count=len(faiss_manager.metadata),
    llm_model=llm.model_name
)


# ==================================================
# Chat Loop
# ==================================================

while True:

    question = input("\nAsk: ").strip()

    # ----------------------------------------------
    # Exit
    # ----------------------------------------------

    if question.lower() in ["exit", "quit", "bye"]:

        OutputFormatter.goodbye()
        break

    if not question:
        continue

    # ----------------------------------------------
    # Search Documents
    # ----------------------------------------------

    results = search_engine.search(
        question,
        top_k=5
    )

    if not results:

        print("\nSorry, I couldn't find any relevant information.\n")
        continue

    # ----------------------------------------------
    # Conversation History
    # ----------------------------------------------

    if memory.is_follow_up(question):
        history = memory.get_recent_history(3)
    else:
        history = []

    # ----------------------------------------------
    # Build Prompt
    # ----------------------------------------------

    prompt = PromptBuilder.build_prompt(
        question=question,
        documents=results,
        conversation_history=history
    )

    # ----------------------------------------------
    # Generate Answer
    # ----------------------------------------------

    answer = llm.generate(prompt)

    # ----------------------------------------------
    # Save Conversation
    # ----------------------------------------------

    memory.add_interaction(
        question=question,
        answer=answer
    )

    # ----------------------------------------------
    # Display Answer
    # ----------------------------------------------

    OutputFormatter.display_answer(answer)

    # ----------------------------------------------
    # Display References
    # ----------------------------------------------

    OutputFormatter.display_references(results)