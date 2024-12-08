from dotenv import load_dotenv
import os

load_dotenv()

from LinesExtractor import LinesExtractor
from SentenceSummarizer import SentenceSummarizer
from CreateEmbedding import CreateEmbedding
from KeywordExtraction import KeywordExtraction

linesExtractor = LinesExtractor()
sentenceSummarizer = SentenceSummarizer()
embedder = CreateEmbedding()
keywordExtractor = KeywordExtraction().set_keywords_count(10)

from Helper import SplitByMarkdownHeader, ExtractMarkdownHeadersAndContent, CleanText

from SupabaseVectorStore import SupabaseVectorStore
SUPABASE_URL = "http://localhost:8000"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
TABLE_NAME = "n8n_documents_bbc_bvms"
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
            section_index = 1

            for section in sections:

                try:
                    header, content = ExtractMarkdownHeadersAndContent(section)[0]
                except Exception as e:
                    print(f"Error: {e}")
                    header, content = "", section

                ## Use the entire chunk as one line
                lines = content

                ## Use lines by lines using the extractor
                lines = linesExtractor.run(content)
                
                for line in [line for line in lines.split("VNLPAGL\n") if len(line) > 0]:

                    summarize = sentenceSummarizer.run(line)
                    keyword = keywordExtractor.run(line)
                    filename = CleanText(filename.replace(document_path, ""))
                    metadata = {"f": filename, "k": keyword, "h": header}

                    embedding = embedder.run(metadata)
                    print(f"\nEmbedding1: {metadata}")

                    embedding2 = embedder.run(summarize)
                    print(f"\nEmbedding2: {summarize}")

                    content = f"{header}: {line}"
                    print(f"\nContent: {content}")

                    supabase.insert_document({"content": content, "embedding": embedding, "embedding2": embedding2, "metadata": metadata, "summarize": summarize})
                    print(f"\noooooooooooooooooooo File {file_index}/{len(files)} - Line {line_index} - Section {section_index}/{len(sections)} - {file_path} oooooooooooooooooooo")
                    line_index += 1
                section_index += 1
        file_index += 1