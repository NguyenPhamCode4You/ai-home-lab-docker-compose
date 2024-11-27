def RecursiveSplitSentences(document: str, limit: int = 1000, overlap: int = 0):
    """
    Splits the document into paragraphs with a specified length limit.
    Optionally allows for overlapping sentences between paragraphs.
    
    Args:
        document (str): The input document to split.
        limit (int): Maximum character limit for each paragraph. Default is 1000.
        overlap (int): Number of overlapping sentences between consecutive paragraphs. Default is 0.
    
    Returns:
        list: A list of paragraphs.
    """
    # Split the document into sentences
    sentences = document.split(".")
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]  # Remove empty sentences
    
    paragraphs = []
    paragraph = []
    
    while sentences:
        # Add sentences to the paragraph until the limit is reached
        while sentences and len(" ".join(paragraph + [sentences[0]])) + 1 < limit:  # Account for added ". "
            paragraph.append(sentences.pop(0))
        
        # Add the paragraph to the result
        paragraphs.append(". ".join(paragraph) + ".")
        
        # Handle overlap
        if overlap > 0 and sentences:
            paragraph = paragraph[-overlap:]  # Retain last 'overlap' sentences
        else:
            paragraph = []
    
    return paragraphs

def RemoveExcessiveSpacing(text):
    while "  " in text:
        text = text.replace("  ", " ")
    while "\n\n" in text:
        text = text.replace("\n\n", "\n")
    while "...." in text:
        text = text.replace("....", "")
    while "----" in text:
        text = text.replace("----", "")
    while "|||" in text:
        text = text.replace("|||", "")
    return text
