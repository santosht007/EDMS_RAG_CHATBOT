import requests


class OllamaClient:
    """
    Handles communication with the local Ollama server.

    Responsibilities
    ----------------
    - Connect to Ollama
    - Send prompts
    - Receive responses from the LLM
    """

    def __init__(
        self,
        model_name="llama3.2:3b",
        base_url="http://localhost:11434"
    ):
        """
        Initialize Ollama client.

        Args:
            model_name (str): Ollama model name.
            base_url (str): Ollama server URL.
        """

        self.model_name = model_name
        self.base_url = base_url

    # --------------------------------------------------
    # Generate Response
    # --------------------------------------------------

    def generate(self, prompt):
        """
        Send prompt to Ollama and return response.

        Args:
            prompt (str): Prompt to send.

        Returns:
            str: Generated response.
        """

        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        try:

            response = requests.post(
                url,
                json=payload,
                timeout=120
            )

            response.raise_for_status()

            result = response.json()

            return result.get(
                "response",
                "No response generated."
            )

        except requests.exceptions.ConnectionError:

            raise Exception(
                "Cannot connect to Ollama.\n"
                "Make sure Ollama is running."
            )

        except requests.exceptions.Timeout:

            raise Exception(
                "Ollama request timed out."
            )

        except Exception as e:

            raise Exception(
                f"Ollama Error: {str(e)}"
            )

    # --------------------------------------------------
    # Test Connection
    # --------------------------------------------------

    def test_connection(self):
        """
        Check whether Ollama server is running.

        Returns:
            bool
        """

        try:

            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=10
            )

            return response.status_code == 200

        except Exception:

            return False