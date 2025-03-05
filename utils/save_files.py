import os


def save_uploaded_file(uploaded_file):
    folder = "uploads"
    os.makedirs(folder, exist_ok=True)  # Ensure the directory exists
    file_path = os.path.join(folder, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())  # Save file to disk

    return file_path
