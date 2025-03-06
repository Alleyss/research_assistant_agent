import streamlit as st
from response_utils import (
    get_chat_response,
    init_model_in_memory,
    set_pdf_in_memory,
    rebuild_session_vector_store,
)
from modules.vector_store import clear_vector_store, retrieve_pdfdocument_from_vector
from sessions_utils import (
    add_pdf_to_session,
    load_sessions,
    add_new_session,
    get_session_conversation,
    add_message_to_session,
    get_session_pdfs,
    remove_pdf_from_session,
)
from utils.save_files import save_uploaded_file

llm, embedding_model = init_model_in_memory()
st.title("Doc RAG Chatbot for Streamlit")

# Load existing sessions
sessions = load_sessions()

# Initialize session state
if "selected_session" not in st.session_state:
    st.session_state.selected_session = None
if "initialized_vectors" not in st.session_state:
    st.session_state.initialized_vectors = set()

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
                # If changing sessions, clear the previous vector store from memory
                if (
                    st.session_state.selected_session is not None
                    and st.session_state.selected_session != session_title
                ):
                    clear_vector_store(st.session_state.selected_session)

                st.session_state.selected_session = session_title
                st.rerun()

# Main content area for displaying conversation
if st.session_state.selected_session:
    session_id = st.session_state.selected_session
    st.header(f"Session: {st.session_state.selected_session}")

    # Load session PDFs into vector store if not already done
    if session_id not in st.session_state.initialized_vectors:
        session_pdfs = get_session_pdfs(session_id)
        pdf_paths = [pdf["path"] for pdf in session_pdfs]

        with st.spinner("Loading documents..."):
            rebuild_session_vector_store(session_id, pdf_paths, embedding_model)

        # Mark this session as initialized
        st.session_state.initialized_vectors.add(session_id)

    # Display current PDFs attached to this session with remove buttons
    session_pdfs = get_session_pdfs(session_id)
    if session_pdfs:
        st.subheader("Attached Documents")
        for i, pdf in enumerate(session_pdfs):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(f"{i+1}. {pdf['name']}")
            with col2:
                if st.button("Remove", key=f"remove_{i}"):
                    # Remove PDF from session data
                    if remove_pdf_from_session(session_id, pdf["name"]):
                        # Re-initialize vector store without this PDF
                        updated_pdfs = get_session_pdfs(session_id)
                        pdf_paths = [p["path"] for p in updated_pdfs]

                        with st.spinner("Updating documents..."):
                            rebuild_session_vector_store(
                                session_id, pdf_paths, embedding_model
                            )

                        st.success(f"Removed {pdf['name']}")
                        st.rerun()

    # Compact PDF uploader with expander
    with st.expander("Add Document", expanded=False):
        # Make the uploader more compact
        col1, col2 = st.columns([3, 1])
        with col1:
            uploaded_files = st.file_uploader(
                "PDF files",
                accept_multiple_files=True,
                type="pdf",
                label_visibility="collapsed",
            )
        with col2:
            upload_button = st.button("Upload", use_container_width=True)

        if uploaded_files and upload_button:
            with st.spinner("Processing documents..."):
                for uploaded_file in uploaded_files:
                    pdf_file_path = save_uploaded_file(uploaded_file)
                    pdf_file_name = uploaded_file.name

                    # Add PDF to session data
                    sessions = add_pdf_to_session(
                        sessions,
                        session_id,
                        pdf_file_path,
                        pdf_file_name,
                    )

                    # Process the PDF for embedding in this session's vector store
                    set_pdf_in_memory(session_id, pdf_file_path, embedding_model)

            st.success(f"Added {len(uploaded_files)} document(s)")
            st.rerun()

    # Display conversation
    st.subheader("Conversation")
    conversation = get_session_conversation(sessions, session_id)
    for message in conversation:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me about anything"):
        # Get last 5 conversation turns
        last_5_messages = conversation[-5:]
        message_user = {"role": "user", "content": prompt}
        sessions = add_message_to_session(sessions, session_id, message_user)
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Retrieve relevant documents from vector store
            context = retrieve_pdfdocument_from_vector(session_id, prompt)

            # Get chat response with context from relevant documents
            response_text = get_chat_response(
                user_message=prompt, llm=llm, context=context["context"]
            )

            # Display response
            response = st.write(response_text)

        message_assistant = {"role": "assistant", "content": response_text}
        sessions = add_message_to_session(sessions, session_id, message_assistant)
else:
    st.info("Please select or create a session to start chatting")
