import os

document_path = 'processed'

for root, _, files in os.walk(f"./{document_path}"):
    for file in files:
        file_path = os.path.join(root, file)
        filename = os.path.splitext(file)[0]
        
        with open(file_path, 'r') as file:
            document = file.read()
            