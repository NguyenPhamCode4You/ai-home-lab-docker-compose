import datetime
import os

class Job:
    def __init__(self, name: str, instruction: str, model, document_chunk_size: int = 8000):
        self.model = model
        self.name = name or "GenericJob"
        self.instruction = instruction
        self.document_chunk_size = document_chunk_size

    async def stream(self, context: str):
        chunks = HardSplitChar(context, self.document_chunk_size)
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        folder_path = os.path.join(os.getcwd(), "logs", self.model.name, self.name, date_str)
        os.makedirs(folder_path, exist_ok=True)
        time_str = datetime.datetime.now().strftime("%H-%M-%S")
        
        with open(os.path.join(folder_path, f"{time_str}.md"), "w", encoding="utf-8") as file:
            for chunk in chunks:
                final_prompt = self.instruction.format(context=chunk)
                async for response_chunk in self.model.stream(final_prompt):
                    yield response_chunk
                    file.write(response_chunk)
                    file.flush()

def HardSplitChar(text: str, max_length: int = 8000):
    chunks = []
    while len(text) > max_length:
        chunks.append(text[:max_length])
        text = text[max_length:]
    chunks.append(text)
    return chunks