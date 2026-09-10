from config import ASSISTANT_NAME, SHUTDOWN_COMMANDS
from core.soul import route_command
from core.session import Session
from logger import log_event
from memory.database import get_user_name, save_user_name


def run_chat():
    session = Session()

    print(f"{ASSISTANT_NAME} online.")
    log_event(f"{ASSISTANT_NAME} started.")

    name = get_user_name()

    if name:
        print(f"Welcome back, {name}.")
    else:
        name = input("What is your name? ").strip()

        if name:
            save_user_name(name)
            print(f"Welcome, {name}.")
            log_event("User name saved.")

    while True:
        if session.current_mode:
            prompt = f"{session.current_mode} > "
        else:
            prompt = "What would you like to do? "

        raw_command = input(f"\n{prompt}").strip()
        normalized_command = raw_command.lower()

        if normalized_command in SHUTDOWN_COMMANDS:
            print(f"{ASSISTANT_NAME} offline.")
            log_event(f"{ASSISTANT_NAME} shut down.")
            break

        if normalized_command == "back":
            if session.current_mode:
                previous_mode = session.current_mode
                session.set_mode(None)

                print(f"Leaving {previous_mode} mode.")
            else:
                print("No active mode.")

            continue

        session.add_command(raw_command)
        log_event(f"Command received: {raw_command}")

        response = route_command(
            raw_command,
            session
        )

        print(response)