from agents.academic import run as run_academic
from agents.developer import run as run_developer
from agents.game_dev import run as run_game_dev


COMMANDS = {
    "study": run_academic,
    "code": run_developer,
    "game": run_game_dev
}


def route_command(command):
    command = command.strip().lower()

    action = COMMANDS.get(command)

    if action:
        return action()

    return "I don't recognize that command yet."