from pathlib import Path


# ==========================================================
# Project Root Directory
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent



# ==========================================================
# Data Directories
# ==========================================================

DATA_DIR = BASE_DIR / "data"


# Manuals

MANUAL_DIR = DATA_DIR / "manuals"

PPT_DIR = MANUAL_DIR / "ppt"

DOCX_DIR = MANUAL_DIR / "docx"

PDF_DIR = MANUAL_DIR / "pdf"



# FAQ

FAQ_DIR = DATA_DIR / "faq"

FAQ_EXCEL_DIR = FAQ_DIR / "excel"

FAQ_WORD_DIR = FAQ_DIR / "word"



# Images

IMAGE_DIR = DATA_DIR / "images"



# ==========================================================
# Project Directories
# ==========================================================

VECTORSTORE_DIR = BASE_DIR / "vectorstore"

LOG_DIR = BASE_DIR / "logs"

DOCS_DIR = BASE_DIR / "docs"

TEST_DIR = BASE_DIR / "tests"



# ==========================================================
# Supported File Types
# ==========================================================

SUPPORTED_POWERPOINT = [
    ".pptx"
]


SUPPORTED_WORD = [
    ".docx"
]


SUPPORTED_PDF = [
    ".pdf"
]


SUPPORTED_IMAGE = [
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tiff"
]



# ==========================================================
# Embedding Configuration
# ==========================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

EMBEDDING_DIMENSION = 384


# Number of chunks processed together
EMBEDDING_BATCH_SIZE = 32



# ==========================================================
# Text Chunking Configuration
# ==========================================================

# Maximum characters per chunk
CHUNK_SIZE = 500


# Overlap between chunks
CHUNK_OVERLAP = 50


# Ignore very small chunks
# Removes titles-only slides
MIN_CHUNK_SIZE = 100



# ==========================================================
# FAISS Vector Store Configuration
# ==========================================================

FAISS_INDEX_FILE = (
    VECTORSTORE_DIR / "edms_faiss.index"
)


EMBEDDING_METADATA_FILE = (
    VECTORSTORE_DIR / "embedding_metadata.pkl"
)


# Alias for future compatibility
METADATA_FILE = EMBEDDING_METADATA_FILE



# ==========================================================
# Application Information
# ==========================================================

APP_NAME = "EDMS AI Assistant"

APP_VERSION = "1.0"

AUTHOR = "Santosh Thoppe"



# ==========================================================
# Chatbot Configuration
# ==========================================================

TOP_K_RESULTS = 5

DEFAULT_LANGUAGE = "English"



# ==========================================================
# Future Features
# ==========================================================

ENABLE_OCR = False

ENABLE_IMAGE_ANALYSIS = False

ENABLE_HYBRID_SEARCH = False