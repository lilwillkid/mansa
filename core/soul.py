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
from core.help import get_help
from core.system import (
    get_status,
    get_version,
    get_about,
    get_history,
    get_mode
)


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
    "mode": lambda session: get_mode(session)
}


def get_current_group(session):
    if not session.current_mode:
        return None

    return COMMAND_GROUPS.get(session.current_mode)


def route_command(command, session):
    command = command.strip().lower()

    if command == "help":
        return get_help(COMMAND_GROUPS)

    system_action = SYSTEM_COMMANDS.get(command)

    if system_action:
        return system_action(session)

    current_group = get_current_group(session)

    if current_group:
        local_commands = current_group["commands"]

        if command in local_commands:
            return current_group["action"](command)

    for group_name, group in COMMAND_GROUPS.items():
        if command in group["aliases"]:
            session.set_mode(group_name)

            return group["action"]()

    if current_group:
        return current_group["action"](command)

    return "I don't recognize that command yet."