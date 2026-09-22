GAME_DEV_COMMANDS = {
    "projects": "Game project tools are not available yet.",
    "unity": "Unity tools are not available yet.",
    "debug": "Game debugging tools are not available yet.",
    "design": "Game design tools are not available yet."
}


def run(command=None, ai_provider=None):
    if command is None:
        available_tools = ", ".join(GAME_DEV_COMMANDS.keys())

        return (
            "Entering Game Development mode.\n"
            f"Available tools: {available_tools}"
        )

    action = GAME_DEV_COMMANDS.get(command)

    if action:
        return action

    return "I don't recognize that Game Development command yet."