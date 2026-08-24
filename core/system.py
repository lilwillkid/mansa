from config import ASSISTANT_NAME, PLATFORM_NAME, VERSION


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
        "SOUL handles routing and system logic.\n"
        "Specialized agents currently include Academic, Development, and Game Development."
    )


def get_history(session):
    return session.get_history()


def get_mode(session):
    return session.get_current_mode()