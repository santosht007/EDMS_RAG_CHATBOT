class SourceManager:
    """
    Utility class for formatting source references.

    Responsibilities:
    - Group documents by manual.
    - Remove duplicate slide numbers.
    - Sort slide numbers.
    """

    @staticmethod
    def organize_sources(results):

        grouped = {}

        for doc in results:

            manual = doc.manual_name
            slide = doc.slide_number

            if manual not in grouped:
                grouped[manual] = set()

            grouped[manual].add(slide)

        return grouped