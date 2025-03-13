import os
import requests


def download_pdf_for_chat(paper):
    """Downloads the PDF locally and returns the file path."""
    if not paper["pdf_url"]:
        return None

    response = requests.get(paper["pdf_url"])
    if response.status_code == 200:
        file_path = os.path.join(f"uploads/{paper['title']}.pdf")
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path
    return None


def download_pdf_for_user(paper):
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
