from config import EMBEDDING_DIMENSION

from src.embeddings.embedding_model import EmbeddingModel
from src.vectorstore.faiss_manager import FAISSManager
from src.vectorstore.search_engine import SearchEngine

from src.llm.ollama_client import OllamaClient
from src.llm.prompt_builder import PromptBuilder

from src.display.output_formatter import OutputFormatter


# --------------------------------------------------
# Application Header
# --------------------------------------------------

OutputFormatter.print_header("EDMS AI Assistant")
print("Version 2.0")


# --------------------------------------------------
# Load Embedding Model
# --------------------------------------------------

print("\nLoading embedding model...")

embedding_model = EmbeddingModel()
model = embedding_model.load_model()

print("Embedding model loaded.")


# --------------------------------------------------
# Load FAISS Database
# --------------------------------------------------

print("\nLoading FAISS index...")

faiss_manager = FAISSManager(EMBEDDING_DIMENSION)

faiss_manager.load_index()
faiss_manager.load_metadata()

print(f"Loaded {faiss_manager.total_vectors()} vectors.")


# --------------------------------------------------
# Create Search Engine
# --------------------------------------------------

search_engine = SearchEngine(
    embedding_model=model,
    faiss_manager=faiss_manager
)

print("Search Engine Ready.")


# --------------------------------------------------
# Initialize Ollama
# --------------------------------------------------

print("\nConnecting to Ollama...")

llm = OllamaClient()

if llm.test_connection():

    print("Connected Successfully.")

else:

    print("Cannot connect to Ollama.")
    exit()


# --------------------------------------------------
# Interactive Chat
# --------------------------------------------------

OutputFormatter.print_header("EDMS AI Chat")

while True:

    question = input("\nAsk EDMS (type 'exit' to quit): ")

    if question.lower() == "exit":

        OutputFormatter.goodbye()
        break

    if not question.strip():

        continue

    # -----------------------------------------
    # Display Question
    # -----------------------------------------

    OutputFormatter.display_question(question)

    # -----------------------------------------
    # Search
    # -----------------------------------------

    results = search_engine.search(
        question,
        top_k=5
    )

    if not results:

        print("\nNo relevant documents found.")
        continue

    # -----------------------------------------
    # Build Prompt
    # -----------------------------------------

    prompt = PromptBuilder.build_prompt(
        question,
        results
    )

    # -----------------------------------------
    # Generate Answer
    # -----------------------------------------

    OutputFormatter.print_sub_header("Thinking...")

    answer = llm.generate(prompt)

    # -----------------------------------------
    # Display Answer
    # -----------------------------------------

    OutputFormatter.display_answer(answer)

    # -----------------------------------------
    # Display References
    # -----------------------------------------

    OutputFormatter.display_references(results)