import os
import requests
import streamlit as st
from modules.process_controller import (
    get_chat_response,
    init_model_in_memory,
    set_pdf_in_memory,
    rebuild_session_vector_store,
)
from modules.rag.vector_store import clear_vector_store, retrieve_pdfdocument_from_vector
from modules.chat_db.chat_session_utils import (
    add_pdf_to_session,
    load_sessions,
    add_new_session,
    get_session_conversation,
    add_message_to_session,
    get_session_pdfs,
    remove_pdf_from_session,
)
from utils.save_files import save_uploaded_file
from modules.fetch_papers.search_paper import search_papers

# Initialize LLM and Embedding Model
llm, embedding_model = init_model_in_memory()
st.title("PaperPal")

# Load existing sessions
sessions = load_sessions()

# Initialize session state
if "selected_session" not in st.session_state:
    st.session_state.selected_session = None
if "initialized_vectors" not in st.session_state:
    st.session_state.initialized_vectors = set()

# Sidebar for session management
with st.sidebar:
    st.header("Chat Sessions")
    new_session_title = st.text_input("New session Title")
    if st.button("Create New session"):
        if new_session_title:
            sessions = add_new_session(sessions, new_session_title)
            st.session_state.selected_session = new_session_title
            st.rerun()

    # Display available sessions
    if sessions:
        for session_title in sessions:
            if st.button(session_title, key=session_title):
                # Clear previous vector store if switching sessions
                if (
                    st.session_state.selected_session is not None
                    and st.session_state.selected_session != session_title
                ):
                    clear_vector_store(st.session_state.selected_session)

                st.session_state.selected_session = session_title
                st.rerun()

# Main content area for conversation
if st.session_state.selected_session:
    session_id = st.session_state.selected_session
    st.header(f"Session: {session_id}")

    # Load session PDFs into vector store if not already done
    if session_id not in st.session_state.initialized_vectors:
        session_pdfs = get_session_pdfs(session_id)
        pdf_paths = [pdf["path"] for pdf in session_pdfs]

        with st.spinner("Loading documents..."):
            rebuild_session_vector_store(session_id, pdf_paths, embedding_model)

        st.session_state.initialized_vectors.add(session_id)

    # Display attached PDFs with removal option
    session_pdfs = get_session_pdfs(session_id)
    if session_pdfs:
        st.subheader("Attached Documents")
        for i, pdf in enumerate(session_pdfs):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(f"{i+1}. {pdf['name']}")
            with col2:
                if st.button("Remove", key=f"remove_{i}"):
                    if remove_pdf_from_session(session_id, pdf["name"]):
                        updated_pdfs = get_session_pdfs(session_id)
                        pdf_paths = [p["path"] for p in updated_pdfs]

                        with st.spinner("Updating documents..."):
                            rebuild_session_vector_store(
                                session_id, pdf_paths, embedding_model
                            )

                        st.success(f"Removed {pdf['name']}")
                        st.rerun()

    # PDF Uploader Section
    with st.expander("Add Document", expanded=False):
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

                    # Add PDF to session
                    sessions = add_pdf_to_session(
                        sessions,
                        session_id,
                        pdf_file_path,
                        pdf_file_name,
                    )

                    # Process the PDF for embedding
                    set_pdf_in_memory(session_id, pdf_file_path, embedding_model)

            st.success(f"Added {len(uploaded_files)} document(s)")
            st.rerun()

    # Search Papers Section
    with st.expander("Search Papers", expanded=False):
        search_keywords = st.text_input("Enter keywords (comma-separated)")
        col1, col2 = st.columns([1, 1])
        with col1:
            arxiv_check = st.checkbox("arXiv", value=True)
        with col2:
            semantic_scholar_check = st.checkbox("Semantic Scholar", value=True)

        if st.button("Search"):
            selected_sources = []
            if arxiv_check:
                selected_sources.append("arxiv")
            if semantic_scholar_check:
                selected_sources.append("semantic_scholar")

            with st.spinner("Searching..."):
                search_results = search_papers(search_keywords, selected_sources, max_results=2)

            if search_results:
                st.subheader("Search Results")
                for paper in search_results:
                    with st.container():
                        st.write(f"**{paper['title']}** ({paper['year']})")
                        st.write(f"**Authors:** {paper.get('authors', 'Unknown')}")
                        st.write(f"**Abstract:** {paper['abstract']}")

                        col1, col2 = st.columns([1, 1])

                        # Download PDF Button
                        if paper["pdf_url"]:  
                            with col1:
                                st.download_button(
                                    label="Download PDF",
                                    data=requests.get(paper["pdf_url"]).content,
                                    file_name=f"{paper['title']}.pdf",
                                    mime="application/pdf",
                                    key=f"download_{paper['title']}"
                                )
                        else:
                            with col1:
                                st.warning("No PDF available.")

                        # Use This to Chat Button
                        def download_pdf_locally(paper):
                            """Downloads the PDF locally and returns the file path."""
                            if not paper["pdf_url"]:
                                return None

                            response = requests.get(paper["pdf_url"])
                            if response.status_code == 200:
                                file_path = os.path.join("uploaded_papers", f"{paper['title']}.pdf")
                                with open(file_path, "wb") as f:
                                    f.write(response.content)
                                return file_path
                            return None

                        with col2:
                            if st.button("Use This to Chat", key=f"chat_{paper['title']}"):
                                file_path = download_pdf_locally(paper)

                                if file_path:
                                    # Add to session like an uploaded PDF
                                    sessions = add_pdf_to_session(
                                        sessions,
                                        session_id,
                                        file_path,
                                        paper["title"]
                                    )

                                    # Process with embeddings
                                    set_pdf_in_memory(session_id, file_path, embedding_model)

                                    st.success("Added to session. Now you can chat with this paper!")
                                    st.rerun()
                                else:
                                    st.error("Failed to download PDF.")
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