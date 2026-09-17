from collections import defaultdict


class ContextBuilder:
    """
    Builds a clean context for the LLM.

    Responsibilities
    ----------------
    - Merge chunks from the same manual
    - Sort by slide number
    - Remove duplicate chunks
    - Produce one clean context
    """

    @staticmethod
    def build(results):
        """
        Build merged context.

        Args:
            results (list)

        Returns:
            str
        """

        grouped = defaultdict(list)

        # --------------------------------------------------
        # Group documents by manual
        # --------------------------------------------------

        for doc in results:
            grouped[doc.manual_name].append(doc)

        context = ""

        # --------------------------------------------------
        # Build context for each manual
        # --------------------------------------------------

        for manual_name, docs in grouped.items():

            # Safe sort for PPT, DOCX and future PDFs
            docs.sort(
                key=lambda x: (
                    x.slide_number
                    if x.slide_number is not None
                    else 0
                )
            )

            context += "\n"
            context += "=" * 70
            context += "\n"
            context += f"MANUAL : {manual_name}\n\n"

            added = set()

            for doc in docs:

                text = doc.text.strip()

                if not text:
                    continue

                if text in added:
                    continue

                added.add(text)

                # Show slide only when available
                if doc.slide_number is not None:
                    context += f"Slide : {doc.slide_number}\n"

                if doc.title:
                    context += f"Title : {doc.title}\n"

                if doc.source_type:
                    context += f"Source : {doc.source_type.upper()}\n"

                context += "\n"
                context += text
                context += "\n\n"

        return context