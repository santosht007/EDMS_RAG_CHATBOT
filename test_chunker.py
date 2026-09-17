from src.preprocessing.document_parser import DocumentParser
from src.chunking.text_chunker import TextChunker


parser = DocumentParser()

documents = parser.parse_all_documents()


print("\n========== DOCUMENT SUMMARY ==========")

print("Documents loaded:", len(documents))


chunker = TextChunker()

chunks = chunker.chunk_documents(documents)


print("Chunks generated:", len(chunks))


print("\n========== SAMPLE CHUNK ==========")


chunk = chunks[0]


print("File:", chunk.manual_name)

print("Source:", chunk.source_type)

print("Title:", chunk.title)

print("Chunk Number:", chunk.chunk_number)

print("Metadata:", chunk.metadata)


print("\nText:")
print(chunk.text[:500])