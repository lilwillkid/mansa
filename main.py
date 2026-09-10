from config import PLATFORM_NAME, VERSION

from chat import run_chat
from memory.database import initialize_database


initialize_database()

print(f"{PLATFORM_NAME} v{VERSION}")

run_chat()