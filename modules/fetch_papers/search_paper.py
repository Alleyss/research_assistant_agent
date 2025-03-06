import os
import requests
import arxiv
import shutil
from semanticscholar import SemanticScholar

# Ensure a directory exists for PDFs
PDF_DIR = "downloads"
os.makedirs(PDF_DIR, exist_ok=True)

# arXiv Search
def search_arxiv(query, max_results=10):
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    return [result for result in client.results(search)]

# Semantic Scholar Search
def search_semantic_scholar(query):
    sch = SemanticScholar()
    results = sch.search_paper(query)
    return [{
        'title': paper.title,
        'abstract': paper.abstract,
        'url': paper.url,
        'pdf_url': paper.openAccessPdf['url'] if paper.openAccessPdf else None,
        'year': paper.year
    } for paper in results]

# Function to download PDFs
# def download_pdf(paper, source):
#     if source == "arxiv":
#         pdf_url = paper.pdf_url
#         filename = f"{PDF_DIR}/{paper.entry_id.split('/')[-1]}.pdf"
#     elif source == "semantic_scholar" and paper.get('pdf_url'):
#         pdf_url = paper['pdf_url']
#         filename = f"{PDF_DIR}/{paper['title'].replace(' ', '_')}.pdf"
#     else:
#         return None  # No PDF available

#     try:
#         response = requests.get(pdf_url, stream=True)
#         if response.status_code == 200:
#             with open(filename, "wb") as f:
#                 for chunk in response.iter_content(1024):
#                     f.write(chunk)
#             print(f"Downloaded: {filename}")
#             return filename
#     except Exception as e:
#         print(f"Failed to download {pdf_url}: {e}")

#     return None


def download_pdf(paper, source):
    if source == "arxiv":
        pdf_url = paper.pdf_url
        filename = f"{PDF_DIR}/{paper.entry_id.split('/')[-1]}.pdf"
    elif source == "semantic_scholar" and paper.get('pdf_url'):
        pdf_url = paper['pdf_url']
        filename = f"{PDF_DIR}/{paper['title'].replace(' ', '_')}.pdf"
    else:
        return None  # No PDF available

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
# Unified Search Interface
def search_papers(keywords, sources=['arxiv', 'semantic_scholar'], download=False,max_results=2):
    papers = []
    query = " AND ".join([f'"{k}"' for k in keywords.split(',')])

    if 'arxiv' in sources:
        arxiv_papers = search_arxiv(query,max_results)
        papers.extend(arxiv_papers)
        if download:
            for paper in arxiv_papers:
                download_pdf(paper, "arxiv")

    if 'semantic_scholar' in sources:
        semantic_papers = search_semantic_scholar(query)
        papers.extend(semantic_papers)
        if download:
            for paper in semantic_papers:
                download_pdf(paper, "semantic_scholar")

    return papers

# # Example Usage
results = search_papers("protein folding neural networks", sources=['arxiv'], download=True)
