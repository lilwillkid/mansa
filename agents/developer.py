DEVELOPER_COMMANDS = {
    "projects": "Project tools are not available yet.",
    "code": "Coding tools are not available yet.",
    "debug": "Debugging tools are not available yet.",
    "git": "Git tools are not available yet."
}


def run(command=None, ai_provider=None):
    if command is None:
        available_tools = ", ".join(DEVELOPER_COMMANDS.keys())

        return (
            "Entering Development mode.\n"
            f"Available tools: {available_tools}"
        )

    action = DEVELOPER_COMMANDS.get(command)

    if action:
        return action

    return "I don't recognize that Development command yet."