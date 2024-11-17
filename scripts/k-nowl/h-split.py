import os
from Helper import RemoveExcessiveSpacing, SplitByMarkdownHeader, HardSplitSentences, ExtractMarkdownHeadersAndContent, CleanText

document_path = 'documents'
processed_prefix = 'processed'

from CreateEmbedding import CreateEmbedding
# embedder = CreateEmbedding(url= 'http://localhost:11434/api/embed')
embedder = CreateEmbedding()

from SupabaseVectorStore import SupabaseVectorStore
SUPABASE_URL = "http://localhost:8000"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
TABLE_NAME = "n8n_documents_bbc_bvms"
supabase = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, TABLE_NAME)

section_max_length = 110

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
                    header, section = ExtractMarkdownHeadersAndContent(section)[0]
                    section_parts = HardSplitSentences(section, section_max_length)
                
                for section in section_parts:
                    if len(section) == 0:
                        continue
                    if header:
                        section = "##  " + header + "\n\n" + section
                    section = RemoveExcessiveSpacing(section)
                    print(section)
                    formatted_chunks.append(section)
                    print(f"oooooooooooooooooooo File {file_index}/{len(files)} - Section {section_index}/{len(sections)} - {file_path} oooooooooooooooooooo \n\n\n\n\n")
                
                section_index += 1
        
        with open(processed_file_path, 'w') as f:
            f.write('\n'.join(formatted_chunks))

        file_index += 1

document_path = 'processed'

file_index = 1
line_index = 1

for root, _, files in os.walk(f"./{document_path}"):
    for file in files:
        file_path = os.path.join(root, file)
        filename = os.path.splitext(file)[0]
        
        with open(file_path, 'r') as file:
            document = file.read()

            sections = SplitByMarkdownHeader(document)
            section_index = 1

            for section in sections:

                try:
                    header, content = ExtractMarkdownHeadersAndContent(section)[0]
                except Exception as e:
                    print(f"Error: {e}")
                    header, content = "", section

                # Use the entire chunk as one line
                lines = content
                
                for line in [line for line in lines.split("VNLPAGL\n") if len(line) > 0]:

                    filename = CleanText(filename.replace(document_path, ""))
                    metadata = f"[f]={filename}\t[t]={header}\t[k]=api,url,endpoints"

                    embedding1 = embedder.run(metadata)
                    print(f"Embedding1: {metadata}\n")

                    content = f"{header}: {line}"
                    print(f"Content: {content}\n")

                    supabase.insert_embedding(text=content, embedding=embedding1, metadata=metadata, embedding2=embedding1)
                    print(f"oooooooooooooooooooo File {file_index}/{len(files)} - Line {line_index} - Section {section_index}/{len(sections)} - {file_path} oooooooooooooooooooo \n\n\n\n\n")
                    line_index += 1
                section_index += 1
        file_index += 1

