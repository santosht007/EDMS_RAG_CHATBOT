class PromptBuilder:
    """
    Builds professional prompts for the EDMS AI Assistant.
    """

    @staticmethod
    def build_prompt(
        question,
        documents,
        conversation_history=None,
        evidence_warning=""
    ):
        """
        Build the final prompt sent to the LLM.

        Args:
            question (str)
            documents (list)
            conversation_history (list)
            evidence_warning (str)

        Returns:
            str
        """

        # --------------------------------------------------------
        # Previous Conversation
        # --------------------------------------------------------

        history_text = ""

        if conversation_history:

            history_text += """
============================================================
PREVIOUS CONVERSATION
============================================================

"""

            for conversation in conversation_history:

                history_text += f"""
User:
{conversation.question}

Assistant:
{conversation.answer}

------------------------------------------------------------

"""

        else:

            history_text = "No previous conversation."

        # --------------------------------------------------------
        # Retrieved Documents
        # --------------------------------------------------------

        context = ""

        for rank, doc in enumerate(documents, start=1):

            if rank == 1:
                importance = "Highest Relevance"

            elif rank == 2:
                importance = "High Relevance"

            elif rank == 3:
                importance = "Medium Relevance"

            else:
                importance = "Supporting Information"

            context += f"""
============================================================
DOCUMENT {rank}
============================================================

Importance
----------
{importance}

Manual
------
{doc.manual_name}

Slide
-----
{doc.slide_number}

Title
-----
{doc.title}

Content
-------
{doc.text}

"""

        # --------------------------------------------------------
        # Build Final Prompt
        # --------------------------------------------------------

        prompt = f"""
# ROLE

You are an experienced EDMS Support Engineer.

Your job is to answer user questions ONLY using the retrieved EDMS manuals.

============================================================

# MISSION

Provide accurate, professional and evidence-based answers.

Correctness is more important than completeness.

============================================================

# STRICT EVIDENCE POLICY

Every factual statement MUST be directly supported by the retrieved manuals.

Never use:

• General knowledge

• Common software behaviour

• Personal assumptions

• Typical EDMS functionality

• Industry best practices

If the manuals do NOT explicitly mention something,
do NOT present it as fact.

============================================================

# UNKNOWN INFORMATION POLICY

If relevant manuals are retrieved but they do not answer the user's exact question, reply like this:

"The retrieved EDMS manuals describe the related procedure, but they do not specify this information."

If NO relevant manuals are available, reply exactly:

"I could not find this information in the EDMS manuals."

============================================================

# DO NOT

Never:

• invent steps

• invent buttons

• invent menu names

• invent permissions

• invent supported file formats

• invent workflows

• invent system behaviour

• invent prerequisites

If information is missing,
clearly state that it is not specified.

============================================================

# PROCEDURE RULES

When documents describe a procedure:

• Preserve the original order.

• Do not add new steps.

• Do not remove important steps.

• Merge multiple documents only if they clearly describe the same workflow.

============================================================

# IMPORTANT CONDITIONS

Mention conditions ONLY if explicitly written.

Examples:

• Draft status

• Required permissions

• Registration completed

• Access rights

• Administrator requirement

If none are mentioned, write:

None.

============================================================

# WARNINGS

Mention warnings ONLY if explicitly written.

Otherwise write:

None.

============================================================

# PREVIOUS CONVERSATION

{history_text}

============================================================

# RETRIEVED EDMS MANUALS

{context}

============================================================

# EVIDENCE VALIDATION

{evidence_warning}

============================================================

# USER QUESTION

{question}

============================================================

# RESPONSE FORMAT

Summary

Step-by-step Procedure

Important Conditions

Warnings

============================================================

# FINAL VERIFICATION

Before generating your answer, silently verify:

1. Every factual statement is supported by the manuals.

2. If the Evidence Validation section reports missing information,
do NOT infer or guess the answer.

3. Clearly state when the manuals do not specify the requested information.

4. Never use outside knowledge.

Only after these checks, generate the final answer.

============================================================

FINAL ANSWER
"""

        return prompt