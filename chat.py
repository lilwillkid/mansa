from config import ASSISTANT_NAME, SHUTDOWN_COMMANDS
from core.soul import route_command
from logger import log_event


def run_chat():
    print(f"{ASSISTANT_NAME} online.")
    log_event(f"{ASSISTANT_NAME} started.")

    name = input("What is your name? ")
    print(f"Welcome, {name}.")
    log_event(f"User identified as {name}.")

    while True:
        command = input("\nWhat would you like to do? ").strip().lower()

        if command in SHUTDOWN_COMMANDS:
            print(f"{ASSISTANT_NAME} offline.")
            log_event(f"{ASSISTANT_NAME} shut down.")
            break

        log_event(f"Command received: {command}")

        response = route_command(command)

        print(response)