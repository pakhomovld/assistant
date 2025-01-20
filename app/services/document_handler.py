from difflib import get_close_matches

def retrieve_relevant_parts(document, query, max_length=8000):
    if not document:  # Если документ пустой или равен None
        return "Document content is missing. Please upload a document."

    sentences = document.split(".")
    matches = get_close_matches(query, sentences, n=10, cutoff=0.2)
    result = " ".join(matches)
    return result[:max_length]
