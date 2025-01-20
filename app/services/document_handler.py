"""
Document handling utility module.

Provides a function to retrieve relevant parts of a document
based on a user query.
"""

from difflib import get_close_matches

def retrieve_relevant_parts(document: str, query: str, max_length: int = 8000) -> str:
    """
    Retrieves relevant parts of the document that match the query.

    Args:
        document (str): The content of the document to search within.
        query (str): The query string to match against the document.
        max_length (int): The maximum length of the returned result.

    Returns:
        str: Relevant parts of the document or a message if the document is missing.
    """
    if not document:  # Check if the document is empty or None
        return "Document content is missing. Please upload a document."

    sentences = document.split(".")  # Split the document into sentences
    matches = get_close_matches(query, sentences, n=10, cutoff=0.2)
    result = " ".join(matches)
    return result[:max_length]
