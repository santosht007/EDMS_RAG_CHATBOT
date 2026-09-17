from src.preprocessing.document_parser import DocumentParser
from config import DOCX_DIR


parser = DocumentParser()

documents = parser.parse_word(DOCX_DIR)

print("Documents loaded:", len(documents))


for doc in documents:
    print("----------------------")
    print(doc.manual_name)
    print(doc.title)
    print(doc.text[:300])