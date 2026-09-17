import streamlit as st

from config import EMBEDDING_DIMENSION

from src.embeddings.embedding_model import EmbeddingModel
from src.vectorstore.faiss_manager import FAISSManager
from src.vectorstore.search_engine import SearchEngine
from src.llm.ollama_client import OllamaClient
from src.llm.prompt_builder import PromptBuilder
from src.memory.conversation_memory import ConversationMemory
from src.validation.evidence_validator import EvidenceValidator
from src.utils.source_manager import SourceManager


# ==================================================
# Page Configuration
# ==================================================

st.set_page_config(
    page_title="EDMS AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# ==================================================
# Application Initialization
# ==================================================

@st.cache_resource
def initialize_application():

    # ----------------------------------------------
    # Embedding Model
    # ----------------------------------------------

    embedding_model = EmbeddingModel()
    model = embedding_model.load_model()

    # ----------------------------------------------
    # FAISS
    # ----------------------------------------------

    faiss_manager = FAISSManager(
        EMBEDDING_DIMENSION
    )

    faiss_manager.load_index()
    faiss_manager.load_metadata()

    # ----------------------------------------------
    # Search Engine
    # ----------------------------------------------

    search_engine = SearchEngine(
        embedding_model=model,
        faiss_manager=faiss_manager
    )

    # ----------------------------------------------
    # LLM
    # ----------------------------------------------

    llm = OllamaClient()

    if not llm.test_connection():
        raise RuntimeError(
            "Unable to connect to Ollama."
        )

    # ----------------------------------------------
    # Evidence Validator
    # ----------------------------------------------

    validator = EvidenceValidator()

    return (
        model,
        faiss_manager,
        search_engine,
        llm,
        validator
    )


# ==================================================
# Load Application
# ==================================================

try:

    (
        model,
        faiss_manager,
        search_engine,
        llm,
        validator
    ) = initialize_application()

except Exception as e:

    st.error(
        "Unable to initialize EDMS AI Assistant."
    )

    st.exception(e)

    st.stop()


# ==================================================
# Conversation Memory
# ==================================================

if "memory" not in st.session_state:

    st.session_state.memory = ConversationMemory(
        embedding_model=model,
        max_history=5
    )


memory = st.session_state.memory


# ==================================================
# Chat History
# ==================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ==================================================
# Header
# ==================================================

st.title("🤖 EDMS AI Assistant")

st.caption(
    "AI assistant for EDMS manuals, procedures, "
    "workflows, and document-related questions."
)


# ==================================================
# Sidebar
# ==================================================

with st.sidebar:

    st.header("System Status")

    st.success("System Ready")

    st.divider()

    st.subheader("AI Components")

    st.write(
        "✅ Embedding Model"
    )

    st.caption(
        "all-MiniLM-L6-v2"
    )

    st.write(
        "✅ Vector Database"
    )

    st.caption(
        "FAISS"
    )

    st.write(
        "✅ Semantic Search"
    )

    st.write(
        "✅ Ollama"
    )

    st.caption(
        llm.model_name
    )

    st.write(
        "✅ Conversation Memory"
    )

    st.divider()

    st.subheader("Knowledge Base")

    st.metric(
        "Indexed Chunks",
        len(faiss_manager.metadata)
    )

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        memory.clear()

        st.session_state.messages = []

        st.rerun()


# ==================================================
# Welcome Message
# ==================================================

if not st.session_state.messages:

    st.info(
        "Hello! I am EDMS AI Assistant. "
        "How may I help you?"
    )


# ==================================================
# Display Previous Messages
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        # ------------------------------------------
        # Display References
        # ------------------------------------------

        if (
            message["role"] == "assistant"
            and "references" in message
            and message["references"]
        ):

            with st.expander(
                "📚 References"
            ):

                for reference in message["references"]:

                    st.markdown(
                        reference
                    )


# ==================================================
# Chat Input
# ==================================================

question = st.chat_input(
    "Ask a question about EDMS..."
)


# ==================================================
# Process Question
# ==================================================

if question:

    question = question.strip()

    if not question:

        st.warning(
            "Please enter a question."
        )

        st.stop()

    # ----------------------------------------------
    # Display User Question
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # ----------------------------------------------
    # Search Documents
    # ----------------------------------------------

    with st.spinner(
        "Searching EDMS knowledge base..."
    ):

        results = search_engine.search(
            question,
            top_k=5
        )

    # ----------------------------------------------
    # No Search Results
    # ----------------------------------------------

    if not results:

        answer = (
            "Sorry, I couldn't find any relevant "
            "information in the EDMS manuals."
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "references": []
            }
        )

        with st.chat_message("assistant"):

            st.warning(answer)

        st.stop()

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

    with st.spinner(
        "Generating answer..."
    ):

        try:

            answer = llm.generate(
                prompt
            )

        except Exception as e:

            st.error(
                "Unable to generate an answer "
                "from Ollama."
            )

            st.exception(e)

            st.stop()

    # ----------------------------------------------
    # Save Conversation
    # ----------------------------------------------

    memory.add_interaction(
        question=question,
        answer=answer
    )

    # ----------------------------------------------
    # Validate Answer
    # ----------------------------------------------

    is_valid = validator.validate(
        answer
    )

    # ----------------------------------------------
    # Organize References
    # ----------------------------------------------

    references = []

    if is_valid:

        organized_sources = (
            SourceManager.organize_sources(
                results
            )
        )

        for manual, slides in organized_sources.items():

            references.append(
                f"**{manual}**  \n"
                f"Slides: {slides}"
            )

    # ----------------------------------------------
    # Save Assistant Message
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": (
                answer
                if is_valid
                else
                "Sorry, the answer could not be "
                "validated against the EDMS manuals."
            ),
            "references": references
        }
    )

    # ----------------------------------------------
    # Display Answer
    # ----------------------------------------------

    with st.chat_message("assistant"):

        if is_valid:

            st.markdown(answer)

            if references:

                with st.expander(
                    "📚 References"
                ):

                    for reference in references:

                        st.markdown(
                            reference
                        )

        else:

            st.warning(
                "Sorry, the answer could not be "
                "validated against the EDMS manuals."
            )