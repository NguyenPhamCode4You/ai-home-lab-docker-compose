import os
from .CodeBlockExtractor import CodeBlockExtractor
from .CodeExplainer import CodeExplainer
from .FolderStructureExplain import FolderStructureExplain
from ..knowl.CreateEmbedding import CreateEmbedding
from ..knowl.KeywordExtraction import KeywordExtraction
from ..knowl.SupabaseVectorStore import SupabaseVectorStore
from ..knowl.Helper import SplitByMarkdownHeader, ExtractMarkdownHeadersAndContent, CleanText

OLLAMA_URL = "http://10.13.13.4:11434/api/generate"
OLLAMA_MODEL = "qwen2.5-coder:14b-instruct-q6_K"

EMBEDING_URL = "http://10.13.13.4:11434/api/embed"
EMBEDING_MODEL = "nomic-embed-text:137m-v1.5-fp16"

embedder = CreateEmbedding(url=EMBEDING_URL, model=EMBEDING_MODEL)
codeExplainer = CodeExplainer(url=OLLAMA_URL, model=OLLAMA_MODEL)
codeBlockExtractor = CodeBlockExtractor(url=OLLAMA_URL, model=OLLAMA_MODEL)
folderStructureExplain = FolderStructureExplain(url=OLLAMA_URL, model=OLLAMA_MODEL)
keywordExtractor = KeywordExtraction(url=OLLAMA_URL, model=OLLAMA_MODEL).set_keywords_count(20)

SUPABASE_URL = "http://10.13.13.4:8000"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
TABLE_NAME = "n8n_documents_ebook"
supabase = SupabaseVectorStore(SUPABASE_URL, SUPABASE_TOKEN, TABLE_NAME)

allowed_file_extensions = {".cs"}
# allowed_file_extensions = {".py"}

ignored_file_pattern = {".Test", ".UnitTest", ".csproj", "Debug", "net7.0", "Migrations", "Snapshot", "bin", "obj", ".git", "log", ".vs", "SednaIntegrationService"}

def is_allowed_file(file_path):
    for extension in allowed_file_extensions:
        if not file_path.endswith(extension):
            return False
    
    if not is_allowed_path(file_path):
        return False
    
    return True

def is_allowed_path(file_path):
    for pattern in ignored_file_pattern:
        if pattern in file_path:
            return False
    
    return True

document_path = 'C:\\Users\\niche\\gitlab\\bbc-bvms-net-back-end-modular'
# document_path = 'C:\\Users\\niche\\ai-home-lab-docker-compose\\scripts\\knowl'

root_folder_name = document_path.split("\\")[-1]
output_path = f"codocu_results\\{root_folder_name}"

if not os.path.exists(output_path):
    os.makedirs(output_path)

files_list = []
dirs_list = []

project_structure_file_path = os.path.join(output_path, "folder_structure.txt")
with open(project_structure_file_path, "w", encoding="utf-8") as folder_structure:
    for root, dirs, files in os.walk(document_path):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not is_allowed_path(dir_path):
                continue
            if dir_path not in dirs_list:
                folder_structure.write(f"{dir_path}\n")
        
        for file in files:
            file_path = os.path.join(root, file)
            if not is_allowed_file(file_path):
                continue
            if file_path not in files_list:
                print(f"{file_path}")
                files_list.append(file_path)

with open(project_structure_file_path, "r", encoding="utf-8") as folder_structure:
    folder_structure_content = folder_structure.read()
    
    if folder_structure_content.strip():  # Avoid running if no content
        explanation = folderStructureExplain.run(folder_structure_content)
        keyword = keywordExtractor.run(explanation)

        folder_structure_content += f"\nExplain: {explanation}"
        folder_structure_content += f"\nKeyword: {keyword}"

        # Debug or process the content as needed
        print(f"Folder Structure Content:\n{folder_structure_content}")

        # header = f"Folder Structure"
        # metadata = {"f": header, "k": keyword}

        # content = f"{header}:\n{folder_structure_content}"
        # embedding = embedder.run(metadata)
        # embedding2 = embedder.run(explanation)
        # supabase.insert_document({"content": content, "embedding": embedding, "embedding2": embedding2, "metadata": metadata, "summarize": explanation})

        with open(os.path.join(output_path, "folder_structure.md"), 'w') as f:
            f.write(folder_structure_content)
            print(f"Folder Structure Analyzed: {folder_structure_content}")

file_index = 1
for file_path in files_list:

    print(f"oooooooooooooooooooo Processing File {file_index}/{len(files_list)} - {file_path} oooooooooooooooooooo \n\n\n\n\n")
    
    filename = os.path.basename(file_path)
    print(f"File Name: {filename}")
    folder_path = file_path.replace(document_path, "").replace(filename, "").strip("\\")
    print(f"Folder Path: {folder_path}")
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

    explanation = codeExplainer.run(file_content)
    keyword = keywordExtractor.run(file_content)

    print(f"Code Block: {file_content}")
    print(f"Explanation: {explanation}")
    print(f"Keyword: {keyword}")

    header = f"{folder_path}\{filename}"
    metadata = {"f": filename, "k": keyword}

    content = f"{file_path}"
    embedding = embedder.run(metadata)
    embedding2 = embedder.run(explanation)

    supabase.insert_document({"content": content, "embedding": embedding, "embedding2": embedding2, "metadata": metadata, "summarize": explanation})
    file_index += 1

    # processed_folder_path = os.path.join(output_path, folder_path)
    # processed_file_name = CleanText(filename.replace(document_path, ""))
    # processed_file_path = os.path.join(processed_folder_path, f"{processed_file_name}.md")
    
    # if not os.path.exists(processed_folder_path):
    #     os.makedirs(processed_folder_path)

    # code_blocks = codeBlockExtractor.run(file_content)
    # code_blocks = code_blocks.split("VNLPAGL\n")

    # document_content = f""
    # line_index = 1

    # for code_block in code_blocks:
    #     if len(code_block) == 0:
    #         continue

    #     explanation = codeExplainer.run(code_block)
    #     keyword = keywordExtractor.run(code_block)

    #     print(f"Code Block: {code_block}")
    #     print(f"Explanation: {explanation}")
    #     print(f"Keyword: {keyword}")

    #     header = f"{folder_path}\{filename}"
    #     metadata = {"f": processed_file_name, "h": header, "k": keyword}

    #     content = f"{header}: {code_block}"
    #     embedding = embedder.run(metadata)
    #     embedding2 = embedder.run(explanation)

    #     supabase.insert_document({"content": content, "embedding": embedding, "embedding2": embedding2, "metadata": metadata, "summarize": explanation})
    #     line_index += 1

    #     document_content += f"\n{code_block}"
    #     document_content += f"\nExplain: {explanation}"
    #     document_content += f"\nKeyword: {keyword}"

    #     print(f"oooooooooooooooooooo File {file_index}/{len(files_list)} - Line {line_index}/{len(code_blocks)} - {file_path} oooooooooooooooooooo \n\n\n\n\n")
        
    #     line_index += 1

    # with open(processed_file_path, 'w') as f:
    #     f.write(document_content)

    # file_index += 1