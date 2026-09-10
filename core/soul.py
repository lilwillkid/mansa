from agents.academic import (
    run as run_academic,
    ACADEMIC_COMMANDS
)
from agents.developer import (
    run as run_developer,
    DEVELOPER_COMMANDS
)
from agents.game_dev import (
    run as run_game_dev,
    GAME_DEV_COMMANDS
)
from ai.local_provider import LocalProvider
from config import AI_SYSTEM_PROMPT
from core.help import get_help
from core.system import (
    VALID_MEMORY_CATEGORIES,
    get_status,
    get_version,
    get_about,
    get_history,
    get_mode,
    get_memories,
    search_memories,
    remember,
    forget,
    update_saved_memory,
    update_user_name
)
from memory.database import get_memory_context


AI_PROVIDER = LocalProvider()


COMMAND_GROUPS = {
    "Academic": {
        "aliases": [
            "study",
            "school",
            "academic",
            "homework"
        ],
        "action": run_academic,
        "commands": ACADEMIC_COMMANDS
    },

    "Development": {
        "aliases": [
            "code",
            "coding",
            "developer",
            "develop",
            "development",
            "programming"
        ],
        "action": run_developer,
        "commands": DEVELOPER_COMMANDS
    },

    "Game Development": {
        "aliases": [
            "game",
            "gaming",
            "game dev",
            "gamedev",
            "unity"
        ],
        "action": run_game_dev,
        "commands": GAME_DEV_COMMANDS
    }
}


SYSTEM_COMMANDS = {
    "status": lambda session: get_status(),
    "version": lambda session: get_version(),
    "about": lambda session: get_about(),
    "history": lambda session: get_history(session),
    "mode": lambda session: get_mode(session),
    "memories": lambda session: get_memories()
}


def get_current_group(session):
    if not session.current_mode:
        return None

    return COMMAND_GROUPS.get(session.current_mode)


def build_system_context(query=None):
    memory_context = get_memory_context(query)

    if memory_context:
        return (
            f"{AI_SYSTEM_PROMPT}\n\n"
            f"{memory_context}"
        )

    return AI_SYSTEM_PROMPT


def refresh_ai_context(session, query=None):
    messages = session.get_ai_messages()

    if not messages:
        return

    if messages[0]["role"] == "system":
        messages[0]["content"] = build_system_context(
            query
        )


def ask_ai(command, session):
    if not session.get_ai_messages():
        session.add_ai_message(
            "system",
            build_system_context(command)
        )
    else:
        refresh_ai_context(
            session,
            command
        )

    session.add_ai_message(
        "user",
        command
    )

    response = AI_PROVIDER.generate_response(
        session.get_ai_messages()
    )

    session.add_ai_message(
        "assistant",
        response
    )

    return response


def parse_memory_command(raw_command):
    memory_text = raw_command[
        len("remember "):
    ].strip()

    parts = memory_text.split(
        maxsplit=1
    )

    if len(parts) == 2:
        possible_category = parts[0].lower()
        content = parts[1]

        if possible_category in VALID_MEMORY_CATEGORIES:
            return content, possible_category

    return memory_text, "general"


def route_command(command, session):
    raw_command = command.strip()
    normalized_command = raw_command.lower()

    if normalized_command == "help":
        return get_help(COMMAND_GROUPS)

    if normalized_command.startswith("call me "):
        name = raw_command[
            len("call me "):
        ].strip()

        response = update_user_name(name)
        refresh_ai_context(session)

        return response

    if normalized_command.startswith("search memories "):
        query = raw_command[
            len("search memories "):
        ].strip()

        if not query:
            return "Use: search memories <text>"

        return search_memories(query)

    if normalized_command.startswith("remember "):
        memory_content, category = parse_memory_command(
            raw_command
        )

        response = remember(
            memory_content,
            category
        )

        refresh_ai_context(session)

        return response

    if normalized_command.startswith("forget "):
        memory_id_text = raw_command[
            len("forget "):
        ].strip()

        if not memory_id_text.isdigit():
            return "Use: forget <memory id>"

        response = forget(
            int(memory_id_text)
        )

        refresh_ai_context(session)

        return response

    if normalized_command.startswith("update "):
        update_content = raw_command[
            len("update "):
        ].strip()

        parts = update_content.split(
            maxsplit=1
        )

        if len(parts) != 2:
            return "Use: update <memory id> <new text>"

        memory_id_text = parts[0]
        new_content = parts[1]

        if not memory_id_text.isdigit():
            return "Use: update <memory id> <new text>"

        response = update_saved_memory(
            int(memory_id_text),
            new_content
        )

        refresh_ai_context(session)

        return response

    system_action = SYSTEM_COMMANDS.get(
        normalized_command
    )

    if system_action:
        return system_action(session)

    current_group = get_current_group(session)

    if current_group:
        local_commands = current_group["commands"]

        if normalized_command in local_commands:
            return current_group["action"](
                normalized_command
            )

    for group_name, group in COMMAND_GROUPS.items():
        if normalized_command in group["aliases"]:
            session.set_mode(group_name)

            return group["action"]()

    return ask_ai(raw_command, session)