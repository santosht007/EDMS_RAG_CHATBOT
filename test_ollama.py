from src.llm.ollama_client import OllamaClient

llm = OllamaClient()

print("Testing Ollama...")

if llm.test_connection():

    print("Connected Successfully!")

    response = llm.generate(
        "Introduce yourself in one sentence."
    )

    print("\nLLM Response:\n")

    print(response)

else:

    print("Connection Failed!")