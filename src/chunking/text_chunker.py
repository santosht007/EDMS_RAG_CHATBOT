from config import CHUNK_SIZE

from src.chunking.chunk_document import ChunkDocument


class TextChunker:
    """
    Converts SlideDocument objects into ChunkDocument objects.
    """

    def __init__(self):
        self.chunk_size = CHUNK_SIZE

    def chunk_documents(self, slide_documents):
        """
        Convert SlideDocuments into ChunkDocuments.
        """

        chunks = []

        for slide in slide_documents:

            chunk = ChunkDocument(

                manual_name=slide.manual_name,

                slide_number=slide.slide_number,

                chunk_number=1,

                title=slide.title,

                text=slide.text,

                source_type="PowerPoint",

                language=slide.language,

                metadata={
                    "word_count": len(slide.text.split())
                }

            )

            chunks.append(chunk)

        return chunks