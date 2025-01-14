from difflib import get_close_matches

def retrieve_relevant_parts(document, query, max_length=8000):
    sentences = document.split(".")
    matches = get_close_matches(query, sentences, n=10, cutoff=0.2)
    result = " ".join(matches)
    return result[:max_length]

