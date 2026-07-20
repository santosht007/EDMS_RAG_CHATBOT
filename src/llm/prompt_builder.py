class PromptBuilder:
    """
    Builds the final prompt for the EDMS AI Assistant.
    """

    @staticmethod
    def build_prompt(
        question,
        documents,
        conversation_history=None
    ):
        """
        Build the final prompt sent to Ollama.
        """

        # --------------------------------------------------------
        # Conversation History
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

            context += f"""
============================================================
DOCUMENT {rank}

Manual:
{doc.manual_name}

Slide:
{doc.slide_number}

Title:
{doc.title}

Content:
{doc.text}

"""

        # --------------------------------------------------------
        # Final Prompt
        # --------------------------------------------------------

        prompt = f"""
You are an experienced EDMS Support Engineer.

Your responsibility is to answer ONLY using the retrieved EDMS manuals.

============================================================

RULES

1. Use ONLY the retrieved documents.

2. Never use outside knowledge.

3. Never guess.

4. Never invent:

- buttons
- menus
- permissions
- workflows
- prerequisites
- file formats
- system behaviour

5. If the manuals do not contain the requested information,
clearly state that the manuals do not specify it.

============================================================

IMPORTANT

Do NOT include:

- References
- Citations
- Manual names
- Slide numbers
- Source documents

The application automatically displays the supporting
documents after your answer.

============================================================

PREVIOUS CONVERSATION

{history_text}

============================================================

RETRIEVED DOCUMENTS

{context}

============================================================

USER QUESTION

{question}

============================================================

RESPONSE FORMAT

Summary

Procedure
(only if applicable)

Important Conditions
(write "None" if not specified)

Warnings
(write "None" if not specified)

============================================================

Keep the answer concise.

Do not repeat information.

Only include information explicitly stated in the manuals.

FINAL ANSWER
"""

        return prompt