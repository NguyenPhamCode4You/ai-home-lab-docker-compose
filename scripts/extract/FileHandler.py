import os
from datetime import datetime
from docling.document_converter import DocumentConverter
import pandas as pd

converter = DocumentConverter()

class FileHandler:

    def __init__(self, file_stream):
        """
        Initializes the FileHandler class with a file stream.
        :param file_stream: File stream object from a Flask request
        """
        self.file_stream = file_stream
        self.temp_file_path = None

    def save_temp_file(self):
        """
        Saves the uploaded file to a temporary file with a timestamped name.
        :return: The file path of the saved temporary file.
        """
        timestamp = datetime.now().strftime('%Y.%m.%d-%H.%M.%S')
        filename = f"{timestamp}-{self.file_stream.filename}"
        self.temp_file_path = os.path.join(os.getcwd(), 'temp', filename)

        # Ensure the temp directory exists
        os.makedirs(os.path.dirname(self.temp_file_path), exist_ok=True)

        # Save the file
        self.file_stream.save(self.temp_file_path)
        return self
    
    def convert_file_to_table(self):
        """
        Converts the saved file to a table using the docling library.
        Supported formats: CSV, Excel, and HTML.
        :return: The extracted table content.
        """
        if not self.temp_file_path:
            raise ValueError("File must be saved before conversion.")

        file_extension = os.path.splitext(self.temp_file_path)[1].lower()
        try:
            if file_extension in ['.pdf', '.md', '.doc', '.docx', '.ppt', '.html']:
                # Use docling to extract content
                conv_res = converter.convert(self.temp_file_path)
                # Export tables
                tables_text = ""
                for table_ix, table in enumerate(conv_res.document.tables):
                    table_df: pd.DataFrame = table.export_to_dataframe()
                    formatted_rows = table_df.apply(lambda row: ', '.join([f"{col}: {row[col]}" for col in table_df.columns]), axis=1)
                    tables_text += '\n'.join(formatted_rows)

                    # tables_text += table.export_to_html()
                return tables_text

            elif file_extension in ['.csv', '.xls', '.xlsx']:
                # Read the table from the file
                if file_extension == '.csv':
                    table_df = pd.read_csv(self.temp_file_path)
                else:
                    table_df = pd.read_excel(self.temp_file_path)
                return table_df.to_markdown()
            
            else:
                raise ValueError(f"Unsupported file extension: {file_extension}")
            
        except Exception as e:
            raise ValueError(f"Error converting file: {e}")

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
            if file_extension in ['.pdf', '.md', '.doc', '.docx', '.ppt', '.html']:
                # Use docling to extract content
                result = converter.convert(self.temp_file_path)
                return result.document.export_to_markdown()
            
            elif file_extension in ['.txt', '.xml']:
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