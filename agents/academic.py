ACADEMIC_COMMANDS = {
    "assignments": "Assignment tools are not available yet.",
    "courses": "Course tools are not available yet.",
    "notes": "Note tools are not available yet.",
    "study": "Study tools are not available yet."
}


def run(command=None):
    if command is None:
        available_tools = ", ".join(ACADEMIC_COMMANDS.keys())

        return (
            "Entering Academic mode.\n"
            f"Available tools: {available_tools}"
        )

    action = ACADEMIC_COMMANDS.get(command)

    if action:
        return action

    return "I don't recognize that Academic command yet."