"""
Text Chunker

Converts SlideDocument objects into ChunkDocument objects
for embedding and FAISS indexing.

Version: 1.2
"""


from config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    MIN_CHUNK_SIZE
)

from src.chunking.chunk_document import ChunkDocument



class TextChunker:
    """
    Converts documents into searchable chunks.
    """



    def __init__(self):

        self.chunk_size = CHUNK_SIZE

        self.chunk_overlap = CHUNK_OVERLAP

        self.min_chunk_size = MIN_CHUNK_SIZE



    # ==================================================
    # Chunk All Documents
    # ==================================================

    def chunk_documents(self, slide_documents):
        """
        Convert SlideDocument list into ChunkDocument list.
        """

        chunks = []


        skipped_chunks = 0


        for slide in slide_documents:


            document_chunks = self.chunk_single_document(
                slide
            )


            print(
                f"{slide.manual_name}: "
                f"{len(document_chunks)} chunks"
            )


            chunks.extend(
                document_chunks
            )


        print("\nChunking completed")

        print(
            "Total chunks:",
            len(chunks)
        )


        return chunks



    # ==================================================
    # Chunk Single Document
    # ==================================================

    def chunk_single_document(self, slide):
        """
        Split one document into smaller chunks.
        """

        text = slide.text.strip()


        if not text:

            return []



        chunks = []


        start = 0

        chunk_number = 1


        text_length = len(text)



        while start < text_length:


            end = start + self.chunk_size


            chunk_text = text[start:end]



            # ------------------------------------------
            # Sentence boundary handling
            # ------------------------------------------

            if end < text_length:

                last_period = chunk_text.rfind(".")


                if last_period > 100:

                    chunk_text = (
                        chunk_text[:last_period + 1]
                    )



            chunk_text = chunk_text.strip()



            if not chunk_text:

                break



            # ------------------------------------------
            # Quality Filter
            # ------------------------------------------

            if len(chunk_text) >= self.min_chunk_size:


                chunk = ChunkDocument(

                    manual_name=slide.manual_name,

                    slide_number=slide.slide_number,

                    chunk_number=chunk_number,

                    title=slide.title,

                    text=chunk_text,

                    source_type=slide.source_type,

                    language=slide.language,


                    metadata={

                        "word_count":
                            len(chunk_text.split()),


                        "character_count":
                            len(chunk_text),


                        "original_title":
                            slide.title

                    }

                )


                chunks.append(chunk)


                chunk_number += 1



            # ------------------------------------------
            # Safe movement with overlap
            # ------------------------------------------

            previous_start = start


            start = (
                start
                +
                len(chunk_text)
                -
                self.chunk_overlap
            )



            # Prevent infinite loop

            if start <= previous_start:

                start = previous_start + len(chunk_text)



        return chunks