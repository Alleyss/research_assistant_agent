import os
import requests
import arxiv
import shutil
from semanticscholar import SemanticScholar

# Ensure a directory exists for PDFs
PDF_DIR = "uploads"
os.makedirs(PDF_DIR, exist_ok=True)


# arXiv Search (Returns List of Dicts)
def search_arxiv(query, max_results=5):
    """
    Searches for academic papers on arXiv based on the given query.

    This function uses the arXiv API to retrieve a list of research papers that match the specified query.
    It fetches details such as the paper's title, publication year, abstract, authors, and URLs for access.

    Parameters:
    -----------
    query : str
        The search query string used to find relevant papers on arXiv.
    max_results : int, optional
        The maximum number of papers to retrieve (default is 5).

    Returns:
    --------
    list of dict
        A list of dictionaries where each dictionary contains:
        - "title" (str): The title of the paper.
        - "year" (int): The year the paper was published.
        - "abstract" (str): A summary of the paper.
        - "authors" (str): A comma-separated string of author names.
        - "url" (str): The arXiv page URL for the paper.
        - "pdf_url" (str): The direct link to the paper's PDF.
        - "source" (str): A constant value "arxiv" to indicate the data source.

    Example:
    --------
    >>> search_arxiv("deep learning", max_results=3)
    [
        {
            "title": "Deep Learning for AI",
            "year": 2023,
            "abstract": "This paper explores...",
            "authors": "John Doe, Jane Smith",
            "url": "https://arxiv.org/abs/1234.56789",
            "pdf_url": "https://arxiv.org/pdf/1234.56789.pdf",
            "source": "arxiv"
        },
        ...
    ]
    """
    client = arxiv.Client()
    search = arxiv.Search(
        query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance
    )

    papers = []
    for result in client.results(search):
        papers.append(
            {
                "title": result.title,
                "year": result.published.year,
                "abstract": result.summary,
                "authors": ", ".join([a.name for a in result.authors]),
                "url": result.entry_id,
                "pdf_url": result.pdf_url,
                "source": "arxiv",  # Adding source field for consistency
            }
        )
    return papers


# Semantic Scholar Search (Returns List of Dicts)
import requests


def search_semantic_scholar(query, max_results=5):
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": max_results,
        "fields": "title,authors,year,abstract,url,openAccessPdf",
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return []

    data = response.json()
    papers = []

    for paper in data.get("data", []):  # Ensure it doesn't break if no data
        pdf_info = paper.get("openAccessPdf")  # This could be None

        papers.append(
            {
                "title": paper.get("title", "No Title"),
                "year": paper.get("year", "Unknown"),
                "abstract": paper.get("abstract", "No Abstract"),
                "authors": (
                    ", ".join([author["name"] for author in paper.get("authors", [])])
                    if paper.get("authors")
                    else "Unknown"
                ),
                "url": paper.get("url", "#"),
                "pdf_url": (
                    pdf_info["url"]
                    if isinstance(pdf_info, dict) and "url" in pdf_info
                    else None
                ),  # Safe handling
                "source": "semantic_scholar",
            }
        )

    return papers


# Function to download PDFs
def download_pdf(paper):
    pdf_url = paper.get("pdf_url")
    if not pdf_url:
        print(f"No PDF available for {paper['title']}")
        return None

    filename = f"{PDF_DIR}/{paper['title'].replace(' ', '_')}.pdf"

    try:
        response = requests.get(pdf_url, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                shutil.copyfileobj(response.raw, f)
            print(f"Downloaded: {filename}")
            return filename
    except Exception as e:
        print(f"Failed to download {pdf_url}: {e}")

    return None


# Unified Search Function (Ensures Consistent Output Format)
def search_papers(keywords, sources=["arxiv", "semantic_scholar"], max_results=2):
    papers = []
    query = " AND ".join([f'"{k.strip()}"' for k in keywords.split(",")])  # Trim spaces

    if "arxiv" in sources:
        papers.extend(search_arxiv(query, max_results))

    if "semantic_scholar" in sources:
        papers.extend(search_semantic_scholar(query, max_results))

    return papers  # Returns a list of dictionaries with consistent keys


# Example Usage:
# results = search_papers("machine learning, transformers", sources=['semantic_scholar'],max_results=3)
# print(results)
