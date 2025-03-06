import json
import os

SESSIONS_CONV_DATA = "sessions_data.json"
SESSIONS_FILE_DATA = "sessions_file_data.json"


def load_sessions():
    """Loads sessions from the JSON file."""
    if not os.path.exists(SESSIONS_CONV_DATA):
        return {}
    with open(SESSIONS_CONV_DATA, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:  # if there is an error parsing the json
            return {}


def save_sessions(sessions):
    """Saves sessions to the JSON file."""
    with open(SESSIONS_CONV_DATA, "w") as f:
        json.dump(sessions, f, indent=4)


def load_sessions_files():
    """Loads sessions file data from the JSON file."""
    if not os.path.exists(SESSIONS_FILE_DATA):
        return {}
    with open(SESSIONS_FILE_DATA, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_sessions_files(sessions_files):
    """Saves sessions file data to the JSON file."""
    with open(SESSIONS_FILE_DATA, "w") as f:
        json.dump(sessions_files, f, indent=4)


def add_new_session(sessions, session_title):
    """Adds a new session to the sessions dict"""
    if session_title and session_title not in sessions:
        sessions[session_title] = []
        save_sessions(sessions)
    return sessions


def get_session_conversation(sessions, selected_session):
    """Retrieve the conversation history from a specific session."""
    if selected_session in sessions:
        return sessions[selected_session]
    return []


def add_message_to_session(sessions, selected_session, message):
    """Adds a new message to the session"""
    if selected_session in sessions:
        sessions[selected_session].append(message)
        save_sessions(sessions)
    return sessions


def add_pdf_to_session(sessions, selected_session, pdf_file_path, pdf_file_name):
    """Adds a PDF file to the session's file data

    Args:
        sessions: The current sessions dictionary
        selected_session: The session to add the PDF to
        pdf_file_path: Path to the saved PDF file
        pdf_file_name: Original name of the PDF file

    Returns:
        The updated sessions dictionary
    """
    # Load the sessions file data
    sessions_files = load_sessions_files()

    # Initialize the session in sessions_files if it doesn't exist
    if selected_session not in sessions_files:
        sessions_files[selected_session] = []

    # Check if the PDF is already in the session to avoid duplicates
    for pdf in sessions_files[selected_session]:
        if pdf["name"] == pdf_file_name:
            return sessions  # PDF already exists

    # Add the PDF file info to the session
    pdf_info = {"name": pdf_file_name, "path": pdf_file_path}
    sessions_files[selected_session].append(pdf_info)

    # Save the updated sessions file data
    save_sessions_files(sessions_files)

    return sessions


def remove_pdf_from_session(selected_session, pdf_file_name):
    """Removes a PDF file from the session's file data

    Args:
        selected_session: The session to remove the PDF from
        pdf_file_name: Name of the PDF file to remove

    Returns:
        True if PDF was removed, False otherwise
    """
    # Load the sessions file data
    sessions_files = load_sessions_files()

    # Check if the session exists
    if selected_session not in sessions_files:
        return False

    # Find and remove the PDF
    for i, pdf in enumerate(sessions_files[selected_session]):
        if pdf["name"] == pdf_file_name:
            # Remove the PDF from the list
            sessions_files[selected_session].pop(i)

            # Save the updated sessions file data
            save_sessions_files(sessions_files)
            return True

    return False


def get_session_pdfs(selected_session):
    """Retrieves the list of PDFs for a specific session

    Args:
        selected_session: The session to get PDFs for

    Returns:
        List of PDF info dictionaries for the session
    """
    sessions_files = load_sessions_files()

    if selected_session in sessions_files:
        return sessions_files[selected_session]

    return []
