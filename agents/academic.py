import re
from academic.database import (
    add_assignment,
    add_course,
    add_note,
    complete_assignment,
    get_all_assignments,
    get_all_courses,
    get_all_notes,
    get_assignment,
    get_assignments_for_course,
    get_course,
    get_course_by_code,
    get_note,
    get_notes_for_course
)


ACADEMIC_COMMANDS = {
    "assignments": "Assignment tools are available.",
    "courses": "Course tools are available.",
    "notes": "Note tools are available.",
    "study": "Study tools are not available yet."
}


def format_course(course):
    if not course:
        return "Course not found."

    course_id = course[0]
    code = course[1]
    name = course[2]
    professor = course[3]
    semester = course[4]
    status = course[5]

    professor_text = professor or "Not specified"

    return (
        f"ID: {course_id}\n"
        f"Code: {code}\n"
        f"Name: {name}\n"
        f"Professor: {professor_text}\n"
        f"Semester: {semester}\n"
        f"Status: {status}"
    )


def format_courses(courses):
    if not courses:
        return "No courses saved yet."

    lines = ["Courses:"]

    for course in courses:
        course_id = course[0]
        code = course[1]
        name = course[2]
        semester = course[4]
        status = course[5]

        lines.append(
            f"{course_id}. {code} - {name} "
            f"({semester}, {status})"
        )

    return "\n".join(lines)

def format_assignment(assignment):
    if not assignment:
        return "Assignment not found."

    assignment_id = assignment[0]
    course_code = assignment[1]
    course_name = assignment[2]
    title = assignment[3]
    due_date = assignment[4]
    status = assignment[5]

    due_date_text = due_date or "No due date"

    return (
        f"ID: {assignment_id}\n"
        f"Course: {course_code} - {course_name}\n"
        f"Title: {title}\n"
        f"Due: {due_date_text}\n"
        f"Status: {status}"
    )


def format_assignments(assignments):
    if not assignments:
        return "No assignments saved yet."

    lines = ["Assignments:"]

    for assignment in assignments:
        assignment_id = assignment[0]
        course_code = assignment[1]
        title = assignment[2]
        due_date = assignment[3]
        status = assignment[4]

        due_date_text = due_date or "No due date"

        lines.append(
            f"{assignment_id}. [{course_code}] "
            f"{title} - {due_date_text} "
            f"({status})"
        )

    return "\n".join(lines)

def format_note(note):
    if not note:
        return "Note not found."

    note_id = note[0]
    course_code = note[1]
    course_name = note[2]
    title = note[3]
    content = note[4]
    created_at = note[5]
    updated_at = note[6]

    return (
        f"ID: {note_id}\n"
        f"Course: {course_code} - {course_name}\n"
        f"Title: {title}\n"
        f"Content:\n{content}\n"
        f"Created: {created_at}\n"
        f"Updated: {updated_at}"
    )


def format_notes(notes):
    if not notes:
        return "No academic notes saved yet."

    lines = ["Notes:"]

    for note in notes:
        note_id = note[0]
        course_code = note[1]
        title = note[2]
        created_at = note[3]

        lines.append(
            f"{note_id}. [{course_code}] "
            f"{title} - {created_at}"
        )

    return "\n".join(lines)


def handle_add_course(command):
    course_data = command[
        len("add course "):
    ].strip()

    parts = [
        part.strip()
        for part in course_data.split("|")
    ]

    if len(parts) != 4:
        return (
            "Use: add course "
            "<code> | <name> | <professor> | <semester>"
        )

    code = parts[0]
    name = parts[1]
    professor = parts[2]
    semester = parts[3]

    if not professor:
        professor = None

    course_id = add_course(
        code,
        name,
        professor,
        semester
    )

    return f"Course saved with ID {course_id}."

def handle_add_assignment(command):
    assignment_data = command[
        len("add assignment "):
    ].strip()

    parts = [
        part.strip()
        for part in assignment_data.split("|")
    ]

    if len(parts) != 3:
        return (
            "Use: add assignment "
            "<course id> | <title> | <due date>"
        )

    course_id_text = parts[0]
    title = parts[1]
    due_date = parts[2]

    if not course_id_text.isdigit():
        return "Course ID must be a number."

    course_id = int(course_id_text)

    if not get_course(course_id):
        return f"Course {course_id} does not exist."

    if not title:
        return "Assignment title cannot be empty."

    if not due_date:
        due_date = None

    assignment_id = add_assignment(
        course_id,
        title,
        due_date
    )

    return (
        f"Assignment saved with ID "
        f"{assignment_id}."
    )

def handle_add_note(command):
    note_data = command[
        len("add note "):
    ].strip()

    parts = [
        part.strip()
        for part in note_data.split("|", maxsplit=2)
    ]

    if len(parts) != 3:
        return (
            "Use: add note "
            "<course id> | <title> | <content>"
        )

    course_id_text = parts[0]
    title = parts[1]
    content = parts[2]

    if not course_id_text.isdigit():
        return "Course ID must be a number."

    course_id = int(course_id_text)

    if not get_course(course_id):
        return f"Course {course_id} does not exist."

    if not title:
        return "Note title cannot be empty."

    if not content:
        return "Note content cannot be empty."

    note_id = add_note(
        course_id,
        title,
        content
    )

    return f"Note saved with ID {note_id}."

def find_course_code(text):
    match = re.search(
        r"\b[A-Za-z]{2,5}\s+\d{3}\b",
        text
    )

    if not match:
        return None

    return match.group().upper()

def build_course_context(course_code):
    course = get_course_by_code(
        course_code
    )

    if not course:
        return (
            f"Course {course_code} "
            f"was not found."
        )

    course_id = course[0]
    code = course[1]
    name = course[2]
    professor = course[3]
    semester = course[4]
    status = course[5]

    assignments = get_assignments_for_course(
        course_id
    )

    notes = get_notes_for_course(
        course_id
    )

    lines = [
        f"Course: {code} - {name}",
        f"Professor: {professor or 'Not specified'}",
        f"Semester: {semester}",
        f"Status: {status}",
        "",
        "Assignments:"
    ]

    if assignments:
        for assignment in assignments:
            assignment_id = assignment[0]
            title = assignment[1]
            due_date = assignment[2]
            assignment_status = assignment[3]

            lines.append(
                f"- {assignment_id}: {title} | "
                f"Due: {due_date or 'No due date'} | "
                f"Status: {assignment_status}"
            )
    else:
        lines.append("- None")

    lines.append("")
    lines.append("Notes:")

    if notes:
        for note in notes:
            note_id = note[0]
            title = note[1]
            content = note[2]

            lines.append(
                f"- {note_id}: {title}"
            )

            lines.append(
                f"  {content}"
            )
    else:
        lines.append("- None")

    return "\n".join(lines)

def ask_ai_with_course_context(
    question,
    course_code,
    ai_provider
):
    course_context = build_course_context(
        course_code
    )

    if course_context.endswith(
        "was not found."
    ):
        return course_context

    messages = [
        {
            "role": "system",
            "content": (
                "You are the Academic Agent for M.A.N.S.A. "
                "Use the provided course context when answering "
                "questions about the user's course records. "
                "Do not invent assignments, notes, grades, dates, "
                "or other personal academic information that is "
                "not present in the context. "
                "For general academic concepts, you may use your "
                "general knowledge. "
                "Clearly distinguish general explanations from "
                "information taken from the user's course context. "
                "Respond clearly and concisely."
            )
        },
        {
            "role": "user",
            "content": (
                f"Course context:\n"
                f"{course_context}\n\n"
                f"Question:\n"
                f"{question}"
            )
        }
    ]

    return ai_provider.generate_response(
        messages
    )

def handle_course_question(command, ai_provider):
    question_data = command[
        len("ask course "):
    ].strip()

    parts = [
        part.strip()
        for part in question_data.split("|", maxsplit=1)
    ]

    if len(parts) != 2:
        return (
            "Use: ask course "
            "<course code> | <question>"
        )

    course_code = parts[0]
    question = parts[1]

    if not question:
        return "Tell me what you want to ask."

    return ask_ai_with_course_context(
        question,
        course_code,
        ai_provider
    )

def handle_natural_course_question(
    command,
    ai_provider
):
    course_code = find_course_code(
        command
    )

    if not course_code:
        return None

    return ask_ai_with_course_context(
        command,
        course_code,
        ai_provider
    )

def run(command=None, ai_provider=None):
    if command is None:
        available_tools = ", ".join(
            ACADEMIC_COMMANDS.keys()
        )

        return (
            "Entering Academic mode.\n"
            f"Available tools: {available_tools}"
        )

    if command == "courses":
        return format_courses(
            get_all_courses()
        )

    if command == "assignments":
        return format_assignments(
            get_all_assignments()
        )

    if command == "notes":
        return format_notes(
            get_all_notes()
        )

    if command.startswith("ask course "):
        if ai_provider is None:
            return "Academic AI is not available."

        return handle_course_question(
            command,
            ai_provider
        )

    if command.startswith("context "):
        course_code = command[
            len("context "):
        ].strip()

        if not course_code:
            return "Use: context <course code>"

        return build_course_context(
            course_code
        )

    if command.startswith("course "):
        course_id_text = command[
            len("course "):
        ].strip()

        if not course_id_text.isdigit():
            return "Use: course <id>"

        return format_course(
            get_course(
                int(course_id_text)
            )
        )

    if command.startswith("assignment "):
        assignment_id_text = command[
            len("assignment "):
        ].strip()

        if not assignment_id_text.isdigit():
            return "Use: assignment <id>"

        return format_assignment(
            get_assignment(
                int(assignment_id_text)
            )
        )

    if command.startswith("note "):
        note_id_text = command[
            len("note "):
        ].strip()

        if not note_id_text.isdigit():
            return "Use: note <id>"

        return format_note(
            get_note(
                int(note_id_text)
            )
        )

    if command.startswith("add course "):
        return handle_add_course(command)

    if command.startswith("add assignment "):
        return handle_add_assignment(command)

    if command.startswith("add note "):
        return handle_add_note(command)

    if command.startswith("complete assignment "):
        assignment_id_text = command[
            len("complete assignment "):
        ].strip()

        if not assignment_id_text.isdigit():
            return (
                "Use: complete assignment "
                "<id>"
            )

        assignment_id = int(
            assignment_id_text
        )

        if complete_assignment(
            assignment_id
        ):
            return (
                f"Assignment {assignment_id} "
                f"marked complete."
            )

        return (
            f"Assignment {assignment_id} "
            f"not found."
        )

    action = ACADEMIC_COMMANDS.get(command)

    if action:
        return action

    return (
        "I don't recognize that "
        "Academic command yet."
    )