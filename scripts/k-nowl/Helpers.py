def MarkdownHeaderMarker(document: str, marker_char: str = '§') -> str:
    for curr in range(6, 0, -1):
        document = document.replace(f'{"#"*curr} ', f'{marker_char}{"#"*curr} ')
    return document
