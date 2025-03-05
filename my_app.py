import streamlit as st
from response_utils import get_chat_response, init_model_in_memory, set_pdf_in_memory
from sessions_utils import (
    add_pdf_to_session,
    load_sessions,
    add_new_session,
    get_session_conversation,
    add_message_to_session,
)
from utils.save_files import save_uploaded_file

llm, embedding_model = init_model_in_memory()
st.title("Doc RAG Chatbot for Streamlit")

# Load existing sessions
sessions = load_sessions()

# Initialize session state
if "selected_session" not in st.session_state:
    st.session_state.selected_session = None

# Sidebar for session Management
with st.sidebar:
    st.header("sessions")
    new_session_title = st.text_input("New session Title")
    if st.button("Create New session"):
        if new_session_title:
            sessions = add_new_session(sessions, new_session_title)
            st.session_state.selected_session = new_session_title
            st.rerun()

    # Display the session buttons (menu)
    if sessions:
        for session_title in sessions:
            if st.button(session_title, key=session_title):
                st.session_state.selected_session = session_title
                st.rerun()

# Main content area for displaying conversation
if st.session_state.selected_session:
    st.header(f"session: {st.session_state.selected_session}")
    conversation = get_session_conversation(sessions, st.session_state.selected_session)
    for message in conversation:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    uploaded_files = st.file_uploader(
        "Choose a PDF file", accept_multiple_files=True, type="pdf"
    )
    for uploaded_file in uploaded_files:
        pdf_file_path = save_uploaded_file(uploaded_file)
        set_pdf_in_memory(pdf_file_path, embedding_model)

    if prompt := st.chat_input("Ask me about anything"):
        # Get last 5 conversation turns
        last_5_messages = conversation[-5:]
        message_user = {"role": "user", "content": prompt}
        sessions = add_message_to_session(
            sessions, st.session_state.selected_session, message_user
        )
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Call the get_streaming_chat_response function with user input
            response_text = get_chat_response(user_message=prompt, llm=llm)
            # Use a generator to enable streaming
            response = st.write(response_text)
        message_assistant = {"role": "assistant", "content": response_text}
        sessions = add_message_to_session(
            sessions, st.session_state.selected_session, message_assistant
        )
