from pathlib import Path

# ==========================================================
# Project Root Directory
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

# ==========================================================
# Data Directories
# ==========================================================

DATA_DIR = BASE_DIR / "data"

MANUAL_DIR = DATA_DIR / "manuals"

PPT_DIR = MANUAL_DIR / "ppt"
PDF_DIR = MANUAL_DIR / "pdf"
DOCX_DIR = MANUAL_DIR / "docx"

FAQ_DIR = DATA_DIR / "faq"

FAQ_EXCEL_DIR = FAQ_DIR / "excel"
FAQ_WORD_DIR = FAQ_DIR / "word"

IMAGE_DIR = DATA_DIR / "images"

# ==========================================================
# Project Directories
# ==========================================================

VECTORSTORE_DIR = BASE_DIR / "vectorstore"

LOG_DIR = BASE_DIR / "logs"

DOCS_DIR = BASE_DIR / "docs"

TEST_DIR = BASE_DIR / "tests"

# ==========================================================
# Embedding Configuration
# ==========================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

EMBEDDING_DIMENSION = 384

# ==========================================================
# Text Chunking Configuration
# ==========================================================

CHUNK_SIZE = 500

CHUNK_OVERLAP = 50

# ==========================================================
# FAISS Configuration
# ==========================================================

FAISS_INDEX_FILE = VECTORSTORE_DIR / "edms_faiss.index"

EMBEDDING_METADATA_FILE = VECTORSTORE_DIR / "embedding_metadata.pkl"

# ==========================================================
# Supported File Types
# ==========================================================

SUPPORTED_POWERPOINT = [".pptx"]

SUPPORTED_PDF = [".pdf"]

SUPPORTED_WORD = [".docx"]

SUPPORTED_IMAGE = [
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tiff"
]

# ==========================================================
# Application Information
# ==========================================================

APP_NAME = "EDMS AI Assistant"

APP_VERSION = "1.0"

AUTHOR = "Santosh Thoppe"

# ==========================================================
# Future Configuration (Version 1.1+)
# ==========================================================

TOP_K_RESULTS = 5

DEFAULT_LANGUAGE = "English"

ENABLE_OCR = False

ENABLE_IMAGE_ANALYSIS = False

ENABLE_HYBRID_SEARCH = False

# ---------------------------------------------
# Vector Store
# ---------------------------------------------

VECTORSTORE_DIR = BASE_DIR / "vectorstore"

FAISS_INDEX_FILE = VECTORSTORE_DIR / "edms_faiss.index"

METADATA_FILE = VECTORSTORE_DIR / "embedding_metadata.pkl"