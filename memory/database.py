import re
import sqlite3

from config import DATABASE_PATH


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "do",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "what",
    "with"
}


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS profile (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_user_name(name):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO profile (key, value)
        VALUES ('name', ?)
        ON CONFLICT(key)
        DO UPDATE SET value = excluded.value
        """,
        (name,)
    )

    connection.commit()
    connection.close()


def get_user_name():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT value
        FROM profile
        WHERE key = 'name'
        """
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return None


def save_memory(content, category):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO memories (content, category)
        VALUES (?, ?)
        """,
        (content, category)
    )

    connection.commit()
    connection.close()


def get_all_memories():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, content, category, created_at, updated_at
        FROM memories
        ORDER BY id
        """
    )

    memories = cursor.fetchall()

    connection.close()

    return memories


def extract_keywords(text):
    words = re.findall(
        r"\b[a-zA-Z0-9_]+\b",
        text.lower()
    )

    return {
        word
        for word in words
        if word not in STOP_WORDS
    }


def get_relevant_memories(query, limit=5):
    query_keywords = extract_keywords(query)

    if not query_keywords:
        return []

    memories = get_all_memories()
    scored_memories = []

    for memory in memories:
        content = memory[1]
        category = memory[2]

        memory_keywords = extract_keywords(
            f"{category} {content}"
        )

        score = len(
            query_keywords & memory_keywords
        )

        if score > 0:
            scored_memories.append(
                (score, memory)
            )

    scored_memories.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        memory
        for score, memory in scored_memories[:limit]
    ]


def get_memory_context(query=None):
    name = get_user_name()

    if query:
        memories = get_relevant_memories(query)
    else:
        memories = []

    lines = []

    if name:
        lines.append(f"User name: {name}")

    if memories:
        lines.append("Relevant persistent memories:")

        for memory in memories:
            content = memory[1]
            category = memory[2]

            lines.append(
                f"- [{category}] {content}"
            )

    return "\n".join(lines)


def update_memory(memory_id, new_content):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE memories
        SET content = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (new_content, memory_id)
    )

    changed_rows = cursor.rowcount

    connection.commit()
    connection.close()

    return changed_rows > 0


def delete_memory(memory_id):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM memories
        WHERE id = ?
        """,
        (memory_id,)
    )

    changed_rows = cursor.rowcount

    connection.commit()
    connection.close()

    return changed_rows > 0


def format_memories():
    memories = get_all_memories()

    if not memories:
        return "No persistent memories saved yet."

    lines = []

    for memory in memories:
        memory_id = memory[0]
        content = memory[1]
        category = memory[2]

        lines.append(
            f"{memory_id}. [{category}] {content}"
        )

    return "\n".join(lines)