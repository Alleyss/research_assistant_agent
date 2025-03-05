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


def add_pdf_to_session(sessions, pdf_file_path, pdf_file_name):
    """Adds a PDF file to the session"""
    pass
