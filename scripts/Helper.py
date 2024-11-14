def word_count_less_than(chunk, count = 7):
  # Keep only alphabetic characters and spaces
  cleaned_text = ''.join(char for char in chunk if char.isalpha() or char.isspace())
  # Split by spaces to get the words and count them
  word_count = len(cleaned_text.split())
  # Check if the word count is less than 5
  return word_count < count

def remove_duplicated(chunks):
    seen = set()
    unique_chunks = []
    for chunk in chunks:
        if chunk not in seen:
            unique_chunks.append(chunk)
            seen.add(chunk)
    return unique_chunks

def clean_text(text):
  # Remove newlines, tabs, and extra spaces
  cleaned_text = text.strip().replace("\n", " ").replace("\r", " ").replace("\t", " ").replace("  ", " ")
  cleaned_text = cleaned_text.replace("|||", "").replace("| |", "")
  cleaned_text = cleaned_text.replace(" | ", "-")
  cleaned_text = cleaned_text.replace("**", "").replace("--", "")

  return cleaned_text