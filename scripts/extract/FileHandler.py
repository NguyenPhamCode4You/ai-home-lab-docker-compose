import os
from datetime import datetime
from docling.document_converter import DocumentConverter
import pandas as pd
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat

pipeline_options_PDF = PdfPipelineOptions()
pipeline_options_PDF.do_ocr = False
pipeline_options_PDF.do_table_structure = True
pipeline_options_PDF.table_structure_options.do_cell_matching = True

pipeline_options_IMAGE = PdfPipelineOptions()
pipeline_options_IMAGE.do_ocr = True
pipeline_options_IMAGE.do_table_structure = False
pipeline_options_IMAGE.table_structure_options.do_cell_matching = False

# converter = DocumentConverter(
#     format_options={
#         InputFormat.IMAGE: PdfFormatOption(pipeline_options=pipeline_options_IMAGE),
#         InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options_PDF),
#     }
# )
converter = DocumentConverter()

class FileHandler:
    def __init__(self, file_stream, filename):
        """
        Initializes the FileHandler class with a file stream and filename.
        :param file_stream: File stream object from FastAPI UploadFile
        :param filename: The original filename of the uploaded file
        """
        self.file_stream = file_stream
        self.filename = filename
        self.temp_file_path = None

    def save_temp_file(self):
        """
        Saves the uploaded file to a temporary file with a timestamped name.
        :return: The file path of the saved temporary file.
        """
        timestamp = datetime.now().strftime('%Y.%m.%d-%H.%M.%S')
        filename_with_timestamp = f"{timestamp}-{self.filename}"
        self.temp_file_path = os.path.join(os.getcwd(), 'temp', filename_with_timestamp)

        # Ensure the temp directory exists
        os.makedirs(os.path.dirname(self.temp_file_path), exist_ok=True)

        # Save the file to the temporary path
        with open(self.temp_file_path, 'wb') as f:
            f.write(self.file_stream.read())  # Read file stream and save as a byte stream
        return self
    
    def convert_file_to_text(self):
        """
        Converts the saved file to text using the docling library.
        Supported formats: PDF, Markdown, Excel, and HTML.
        :return: The extracted text content.
        """
        if not self.temp_file_path:
            raise ValueError("File must be saved before conversion.")

        file_extension = os.path.splitext(self.temp_file_path)[1].lower()
        try:
            if file_extension in ['.pdf', '.doc', '.docx', '.ppt', '.html', '.jpg', '.png', '.jpeg']:
                result = converter.convert(self.temp_file_path)
                return result.document.export_to_markdown()
            
            elif file_extension in ['.txt', '.xml', '.md']:
                with open(self.temp_file_path, 'r', encoding='utf-8') as file:
                    return file.read()
                
            else:
                raise ValueError(f"Unsupported file extension: {file_extension}")
            
        except Exception as e:
            raise ValueError(f"Error converting file: {e}")

    def cleanup(self):
        """
        Removes the temporary file after processing.
        """
        if self.temp_file_path and os.path.exists(self.temp_file_path):
            os.remove(self.temp_file_path)