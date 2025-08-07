import inflect
import re

# Initialize inflect engine
p = inflect.engine()

def singularize_prompt(prompt: str) -> str:
    """
    Converts plural nouns in the prompt to singular to reduce confusion.
    Handles basic subject-level pluralization (e.g., 'libraries' -> 'library').
    """
    words = prompt.split()
    updated_words = []

    for word in words:
        # Extract the pure word (remove surrounding punctuation)
        word_clean = re.sub(r'[^\w]', '', word)

        if word_clean.isalpha():  # Ensure it's a valid word
            singular = p.singular_noun(word_clean)
            if singular:
                # Replace only the clean part, keep punctuation intact
                word = word.replace(word_clean, singular)

        updated_words.append(word)

    return ' '.join(updated_words)
