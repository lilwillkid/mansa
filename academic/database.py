from memory.database import get_connection


def initialize_academic_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            professor TEXT,
            semester TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            due_date TEXT,
            status TEXT NOT NULL DEFAULT 'incomplete',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (course_id)
                REFERENCES courses(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (course_id)
                REFERENCES courses(id)
        )
        """
    )

    connection.commit()
    connection.close()


def add_course(code, name, professor, semester):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO courses (
            code,
            name,
            professor,
            semester
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            code,
            name,
            professor,
            semester
        )
    )

    connection.commit()

    course_id = cursor.lastrowid

    connection.close()

    return course_id


def get_all_courses():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            code,
            name,
            professor,
            semester,
            status
        FROM courses
        ORDER BY code
        """
    )

    courses = cursor.fetchall()

    connection.close()

    return courses


def get_course(course_id):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            code,
            name,
            professor,
            semester,
            status
        FROM courses
        WHERE id = ?
        """,
        (course_id,)
    )

    course = cursor.fetchone()

    connection.close()

    return course

def get_course_by_code(code):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            code,
            name,
            professor,
            semester,
            status
        FROM courses
        WHERE LOWER(code) = LOWER(?)
        """,
        (code,)
    )

    course = cursor.fetchone()

    connection.close()

    return course

def add_assignment(course_id, title, due_date):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO assignments (
            course_id,
            title,
            due_date
        )
        VALUES (?, ?, ?)
        """,
        (
            course_id,
            title,
            due_date
        )
    )

    connection.commit()

    assignment_id = cursor.lastrowid

    connection.close()

    return assignment_id


def get_all_assignments():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            assignments.id,
            courses.code,
            assignments.title,
            assignments.due_date,
            assignments.status
        FROM assignments
        JOIN courses
            ON assignments.course_id = courses.id
        ORDER BY assignments.due_date
        """
    )

    assignments = cursor.fetchall()

    connection.close()

    return assignments


def get_assignment(assignment_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            assignments.id,
            courses.code,
            courses.name,
            assignments.title,
            assignments.due_date,
            assignments.status
        FROM assignments
        JOIN courses
            ON assignments.course_id = courses.id
        WHERE assignments.id = ?
        """,
        (assignment_id,)
    )

    assignment = cursor.fetchone()

    connection.close()

    return assignment

def get_assignments_for_course(course_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            due_date,
            status
        FROM assignments
        WHERE course_id = ?
        ORDER BY due_date
        """,
        (course_id,)
    )

    assignments = cursor.fetchall()

    connection.close()

    return assignments

def complete_assignment(assignment_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE assignments
        SET
            status = 'complete',
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (assignment_id,)
    )

    changed_rows = cursor.rowcount

    connection.commit()
    connection.close()

    return changed_rows > 0

def add_note(course_id, title, content):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO notes (
            course_id,
            title,
            content
        )
        VALUES (?, ?, ?)
        """,
        (
            course_id,
            title,
            content
        )
    )

    connection.commit()

    note_id = cursor.lastrowid

    connection.close()

    return note_id


def get_all_notes():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            notes.id,
            courses.code,
            notes.title,
            notes.created_at
        FROM notes
        JOIN courses
            ON notes.course_id = courses.id
        ORDER BY notes.id DESC
        """
    )

    notes = cursor.fetchall()

    connection.close()

    return notes


def get_note(note_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            notes.id,
            courses.code,
            courses.name,
            notes.title,
            notes.content,
            notes.created_at,
            notes.updated_at
        FROM notes
        JOIN courses
            ON notes.course_id = courses.id
        WHERE notes.id = ?
        """,
        (note_id,)
    )

    note = cursor.fetchone()

    connection.close()

    return note

def get_notes_for_course(course_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            content,
            created_at
        FROM notes
        WHERE course_id = ?
        ORDER BY id DESC
        """,
        (course_id,)
    )

    notes = cursor.fetchall()

    connection.close()

    return notes