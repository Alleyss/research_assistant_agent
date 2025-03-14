from google import genai
from google.genai import types
import os


def init_decision_agent():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    sys_instruct = get_agent_use_decision()
    response = client.models.generate_content(
        model="models/gemini-2.0-flash",
        config=types.GenerateContentConfig(system_instruction=sys_instruct),
        contents=["search for paper related to graphRAG"],
    )

    print(response.text)


def get_agent_use_decision():
    prompt = [
        "You are a agent which decides which tools will be used to process user question/quey",
        "Tools:",
        """
        name: search_arxiv
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
        """,
        """
        name: normal_query
        Processes a normal query from the user.
        """,
        "Now you have to process it and return weather to use search_arxiv or normal_query",
        """
        Follow this output structure strictly:
        Thought: what tasks to perform
        Action: which tool to use e.g. search_arxiv or normal_query
        Action input: query to be processed which has to be passed to tool
        output: output of the tool
        """,
    ]

    return prompt


if __name__ == "__main__":
    init_decision_agent()
