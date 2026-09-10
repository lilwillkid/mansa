from config import ASSISTANT_NAME, PLATFORM_NAME, VERSION
from memory.database import (
    delete_memory,
    format_memories,
    get_relevant_memories,
    save_memory,
    save_user_name,
    update_memory
)


VALID_MEMORY_CATEGORIES = {
    "general",
    "academic",
    "project",
    "preference",
    "development",
    "game_dev"
}


def get_status():
    return (
        f"{PLATFORM_NAME} is online.\n"
        f"Assistant: {ASSISTANT_NAME}\n"
        f"Version: {VERSION}\n"
        f"Status: Operational"
    )


def get_version():
    return f"{PLATFORM_NAME} version {VERSION}"


def get_about():
    return (
        f"{PLATFORM_NAME} is a modular personal AI assistant platform.\n"
        f"{ASSISTANT_NAME} is the conversational interface.\n"
        "S.O.U.L. handles routing and system logic.\n"
        "Specialized agents currently include Academic, Development, and Game Development."
    )


def get_history(session):
    return session.get_history()


def get_mode(session):
    return session.get_current_mode()


def get_memories():
    return format_memories()


def search_memories(query):
    memories = get_relevant_memories(query)

    if not memories:
        return "No relevant memories found."

    lines = ["Relevant memories:"]

    for memory in memories:
        memory_id = memory[0]
        content = memory[1]
        category = memory[2]

        lines.append(
            f"{memory_id}. [{category}] {content}"
        )

    return "\n".join(lines)


def remember(content, category="general"):
    if not content:
        return "Tell me what you want me to remember."

    if category not in VALID_MEMORY_CATEGORIES:
        return (
            f"Unknown memory category: {category}\n"
            f"Valid categories: {', '.join(sorted(VALID_MEMORY_CATEGORIES))}"
        )

    save_memory(
        content,
        category
    )

    return f"Memory saved under [{category}]."


def forget(memory_id):
    if delete_memory(memory_id):
        return f"Memory {memory_id} deleted."

    return f"I couldn't find memory {memory_id}."


def update_saved_memory(memory_id, new_content):
    if not new_content:
        return "Tell me what the updated memory should say."

    if update_memory(memory_id, new_content):
        return f"Memory {memory_id} updated."

    return f"I couldn't find memory {memory_id}."


def update_user_name(name):
    if not name:
        return "Tell me what you want me to call you."

    save_user_name(name)

    return f"I'll call you {name}."