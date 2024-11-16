from dotenv import load_dotenv
import os

load_dotenv()

from DataPreProcessing import DataPreProcessing
dataPreProcessor = DataPreProcessing()

from Helper import RemoveExcessiveSpacing, SplitByMarkdownHeader

document_path = 'documents'
processed_prefix = 'processed'

section_max_length = 600

file_index = 1
section_index = 1

for root, _, files in os.walk(f"./{document_path}"):
    processed_root = root.replace(document_path, f"{processed_prefix}")
    if not os.path.exists(processed_root):
        os.makedirs(processed_root)

    for file in files:
        file_path = os.path.join(root, file)
        filename = os.path.splitext(file)[0]
        
        processed_file_path = os.path.join(processed_root, f"{filename}.{processed_prefix}.md")
        formatted_chunks = []

        with open(file_path, 'r') as file:
            document = file.read()
            sections = SplitByMarkdownHeader(document)
            for section in sections:
                section = RemoveExcessiveSpacing(section)
                section_parts = [section]
                header = False
                
                if len(section) > section_max_length:
                    from Helper import ExtractMarkdownHeadersAndContent, RecursiveSplitSentences
                    header, section = ExtractMarkdownHeadersAndContent(section)[0]
                    section_parts = RecursiveSplitSentences(section, section_max_length)
                
                for section in section_parts:
                    if header:
                        section = "##  " + header + "\n\n" + section
                    section = dataPreProcessor.run(section)
                    section = RemoveExcessiveSpacing(section)
                    print(section)
                    formatted_chunks.append(section)
                    section_index += 1
                    print(f"oooooooooooooooooooo File {file_index}/{len(files)} - Section {section_index} - {file_path} oooooooooooooooooooo \n\n\n\n\n")

        with open(processed_file_path, 'w') as f:
            f.write('\n'.join(formatted_chunks))

        file_index += 1