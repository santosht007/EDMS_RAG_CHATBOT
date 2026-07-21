"""
============================================================
EDMS AI Chatbot
Knowledge Base Builder
Version 1.0
============================================================

Builds the FAISS knowledge base from EDMS manuals.

Pipeline

PowerPoint
    ↓
DocumentParser
    ↓
DocumentCleaner
    ↓
TextChunker
    ↓
EmbeddingGenerator
    ↓
FAISS
"""

import time
import traceback

from config import PPT_DIR

from src.preprocessing.document_parser import DocumentParser
from src.chunking.text_chunker import TextChunker
from src.embeddings.embedding_model import EmbeddingModel
from src.embeddings.embedding_generator import EmbeddingGenerator
from src.vectorstore.faiss_manager import FAISSManager


class KnowledgeBaseBuilder:
    """
    Builds the EDMS knowledge base.
    """

    def __init__(self):

        self.parser = DocumentParser()

        self.chunker = TextChunker()

        # Initialize embedding model
        self.embedding_model = EmbeddingModel()

        # Load the model
        self.embedding_model.load_model()

        # Initialize embedding generator
        self.embedding_generator = EmbeddingGenerator(
            self.embedding_model.model
        )

        # Get embedding dimension automatically
        embedding_dimension = (
            self.embedding_model.model.get_sentence_embedding_dimension()
        )

        # Initialize FAISS
        self.faiss = FAISSManager(
            embedding_dimension=embedding_dimension
        )

        self.documents = []
        self.chunks = []
        self.embeddings = []

        self.start_time = None
    # --------------------------------------------------
    # Build Pipeline
    # --------------------------------------------------

    def build(self):

        self.start_time = time.time()

        try:

            self.display_header()

            self.load_documents()

            self.create_chunks()

            self.generate_embeddings()

            self.build_faiss()

            self.save_index()

            self.display_summary()

        except Exception:

            print("\nERROR while building knowledge base.\n")

            traceback.print_exc()

    # --------------------------------------------------
    # Display Header
    # --------------------------------------------------

    def display_header(self):

        print()
        print("=" * 60)
        print("EDMS Knowledge Base Builder")
        print("=" * 60)
        print()

    # --------------------------------------------------
    # Load Documents
    # --------------------------------------------------

    def load_documents(self):

        print("Loading PowerPoint manuals...")

        self.documents = self.parser.parse_powerpoint(PPT_DIR)

        print(f"✓ Loaded {len(self.documents)} slides.\n")

    # --------------------------------------------------
    # Create Chunks
    # --------------------------------------------------

    def create_chunks(self):

        print("Creating document chunks...")

        self.chunks = self.chunker.chunk_documents(
            self.documents
        )

        print(f"✓ Created {len(self.chunks)} chunks.\n")

    # --------------------------------------------------
    # Generate Embeddings
    # --------------------------------------------------

    def generate_embeddings(self):

        print("Generating embeddings...")

        self.embeddings = self.embedding_generator.generate_embeddings(
            self.chunks
        )

        print(f"\n✓ Generated {len(self.embeddings)} embeddings.\n")

      
    # --------------------------------------------------
    # Build FAISS
    # --------------------------------------------------

    def build_faiss(self):

        print("Building FAISS index...")

        self.faiss.add_embeddings(
            self.embeddings
        )

        print(
            f"✓ Total vectors : {self.faiss.total_vectors()}"
        )

        print()


    # --------------------------------------------------
    # Save Index
    # --------------------------------------------------

    def save_index(self):

        print("Saving knowledge base...")

        self.faiss.save_index()

        self.faiss.save_metadata()

        print("✓ Knowledge base saved successfully.\n")


    
    
    # --------------------------------------------------
    # Build Summary
    # --------------------------------------------------

    def display_summary(self):

        elapsed = time.time() - self.start_time

        print("=" * 60)
        print("Knowledge Base Build Completed")
        print("=" * 60)
        print()

        print(f"Slides Processed : {len(self.documents)}")
        print(f"Chunks Created   : {len(self.chunks)}")
        print(f"Embeddings       : {len(self.embeddings)}")
        print()

        print(f"Build Time       : {elapsed:.2f} seconds")
        print()

        print("Output Files")
        print("----------------------------------------")
        print("vectorstore/edms_faiss.index")
        print("vectorstore/edms_metadata.pkl")
        print()

        print("Knowledge base is ready.")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    builder = KnowledgeBaseBuilder()

    builder.build()


if __name__ == "__main__":

    main()
