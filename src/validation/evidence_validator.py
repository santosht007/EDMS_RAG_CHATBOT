class EvidenceValidator:
    """
    Validates whether the LLM actually found
    an answer inside the EDMS manuals.
    """

    def __init__(self):
        """
        Initialize validator.
        """

        self.not_found_phrases = [

            "manuals do not specify",

            "not specified",

            "not mentioned",

            "not available",

            "no information",

            "cannot be found",

            "could not find",

            "not covered",

            "i don't know",

            "unable to answer",

            "does not contain"

        ]

    # --------------------------------------------------
    # Validate Answer
    # --------------------------------------------------

    def validate(self, answer):
        """
        Returns
        -------
        True  -> Valid answer found

        False -> Manual does not contain answer
        """

        answer = answer.lower()

        for phrase in self.not_found_phrases:

            if phrase in answer:

                return False

        return True