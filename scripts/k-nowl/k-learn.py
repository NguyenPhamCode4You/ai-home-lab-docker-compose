import os

from LinesExtractor import LinesExtractor
from SentenceSummarizer import SentenceSummarizer
from Helper import SplitByMarkdownHeader, ExtractMarkdownHeadersAndContent
from CreateEmbedding import CreateEmbedding
from SupabaseVectorStore import SupabaseVectorStore

SUPABASE_URL = "http://localhost:8000"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
TABLE_NAME = "n8n_documents_ebook"
supabase = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, TABLE_NAME)

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
            for section in sections:

                header, content = ExtractMarkdownHeadersAndContent(section)[0]

                lines = LinesExtractor(content).run()
                for line in [line for line in lines.split("VNLPAGL\n") if len(line) > 10]:
                    print(f"Line: {line}\n")

                    sumarize = SentenceSummarizer(content).run()
                    metadata = f"{filename} / {header} - {sumarize}"
                    print(f">>>>>>>>>>>> {metadata}\n")

                    embedding = CreateEmbedding(content).run()
                    embedding_metadata = CreateEmbedding(metadata).run()
                    supabase.insert_embedding(text=content, embedding=embedding, metadata=metadata, embedding2=embedding_metadata)
                    print(f"File {file_index}/{len(files)} - Line {line_index}\n - [{file_path}]")
                    line_index += 1

        file_index += 1