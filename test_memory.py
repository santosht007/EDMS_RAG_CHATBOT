from src.memory.conversation_memory import ConversationMemory

memory = ConversationMemory(max_history=3)

memory.add_interaction(
    "How do I upload a file?",
    "Click the + button."
)

memory.add_interaction(
    "Can I edit it?",
    "Yes."
)

memory.add_interaction(
    "How do I delete it?",
    "Use the Delete option."
)

print("Current Memory:")
print(memory.get_history())

print()

print("Memory Size:")
print(memory.size())