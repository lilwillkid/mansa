from academic.database import initialize_academic_database
from config import PLATFORM_NAME, VERSION

from chat import run_chat
from memory.database import initialize_database


initialize_database()
initialize_academic_database()

print(f"{PLATFORM_NAME} v{VERSION}")

run_chat()