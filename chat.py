from config import ASSISTANT_NAME, SHUTDOWN_COMMANDS
from core.soul import route_command
from core.session import Session
from logger import log_event


def run_chat():
    session = Session()

    print(f"{ASSISTANT_NAME} online.")
    log_event(f"{ASSISTANT_NAME} started.")

    name = input("What is your name? ")
    print(f"Welcome, {name}.")
    log_event(f"User identified as {name}.")

    while True:
        if session.current_mode:
            prompt = f"{session.current_mode} > "
        else:
            prompt = "What would you like to do? "

        command = input(f"\n{prompt}").strip().lower()

        if command in SHUTDOWN_COMMANDS:
            print(f"{ASSISTANT_NAME} offline.")
            log_event(f"{ASSISTANT_NAME} shut down.")
            break

        if command == "back":
            if session.current_mode:
                previous_mode = session.current_mode
                session.set_mode(None)

                print(f"Leaving {previous_mode} mode.")
            else:
                print("No active mode.")

            continue

        session.add_command(command)
        log_event(f"Command received: {command}")

        response = route_command(command, session)

        print(response)