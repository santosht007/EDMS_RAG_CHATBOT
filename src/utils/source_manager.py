class SourceManager:
    """
    Utility class for formatting source references.

    Responsibilities
    ----------------
    - Group documents by manual.
    - Remove duplicate slide numbers.
    - Sort slide numbers.
    - Compress consecutive slides into ranges.
    """

    @staticmethod
    def organize_sources(results):
        """
        Returns:
            dict

            Example:

            {
                "01_ED_Other Functions.pptx": "5–9",
                "01.ED Registration.pptx": "17, 21–24"
            }
        """

        grouped = {}

        # Preserve manual order while removing duplicates
        for doc in results:

            manual = doc.manual_name
            slide = int(doc.slide_number)

            if manual not in grouped:
                grouped[manual] = set()

            grouped[manual].add(slide)

        formatted = {}

        for manual, slides in grouped.items():

            slides = sorted(slides)

            formatted[manual] = SourceManager._compress_ranges(slides)

        return formatted

    # ---------------------------------------------------------

    @staticmethod
    def _compress_ranges(slides):
        """
        Convert

        [5,6,7,8,9]

        into

        5–9

        and

        [17,21,22,23,24]

        into

        17, 21–24
        """

        if not slides:
            return ""

        ranges = []

        start = slides[0]
        end = slides[0]

        for slide in slides[1:]:

            if slide == end + 1:

                end = slide

            else:

                if start == end:
                    ranges.append(str(start))
                else:
                    ranges.append(f"{start}–{end}")

                start = slide
                end = slide

        # Final range

        if start == end:
            ranges.append(str(start))
        else:
            ranges.append(f"{start}–{end}")

        return ", ".join(ranges)