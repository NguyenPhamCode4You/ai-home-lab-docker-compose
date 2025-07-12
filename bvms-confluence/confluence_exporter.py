#!/usr/bin/env python3
"""
READ-ONLY Confluence to Markdown Exporter

⚠️  SAFETY NOTICE: This script is READ-ONLY ⚠️
- This script ONLY reads data from Confluence
- It does NOT write, modify, or delete any content in Confluence
- It only creates local Markdown files on your computer
- Your Confluence space remains completely unchanged

This script connects to a Confluence workspace and exports all pages
from a specified space, converting them to Markdown format locally.
"""

import os
import re
import json
import requests
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from datetime import datetime

from dotenv import load_dotenv
from atlassian import Confluence
from markdownify import markdownify as md
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()


class ConfluenceExporter:
    """READ-ONLY Confluence exporter - only reads data, never writes to Confluence."""
    
    def __init__(self):
        """Initialize the READ-ONLY exporter with configuration from environment variables."""
        print("⚠️  READ-ONLY MODE: This script will NOT modify your Confluence space ⚠️")
        print("   - Only reads pages from Confluence")
        print("   - Creates local Markdown files only")
        print("   - Your Confluence data remains unchanged")
        print()
        
        self.confluence_url = os.getenv('CONFLUENCE_URL')
        self.token = os.getenv('CONFLUENCE_TOKEN')
        self.username = os.getenv('CONFLUENCE_USERNAME')
        self.space_key = os.getenv('CONFLUENCE_SPACE_KEY')
        self.output_dir = Path(os.getenv('OUTPUT_DIR', 'output'))
        self.max_pages = int(os.getenv('MAX_PAGES', 1000))
        
        # Validate required configuration
        if not all([self.confluence_url, self.token, self.username, self.space_key]):
            raise ValueError("Missing required configuration. Please check your .env file.")
        
        # Initialize Confluence client in READ-ONLY mode
        self.confluence = Confluence(
            url=self.confluence_url,
            username=self.username,
            password=self.token,
            cloud=True
        )
        
        # Create output directories
        self.output_dir.mkdir(exist_ok=True)
        self.attachments_dir = self.output_dir / 'attachments'
        self.attachments_dir.mkdir(exist_ok=True)
        
        print(f"Initialized Confluence exporter for space: {self.space_key}")
        print(f"Output directory: {self.output_dir.absolute()}")
    
    def get_all_pages(self) -> List[Dict]:
        """Retrieve all pages from the specified Confluence space."""
        print("Fetching all pages from Confluence...")
        
        try:
            pages = self.confluence.get_all_pages_from_space(
                space=self.space_key,
                start=0,
                limit=self.max_pages,
                expand='body.storage,version,ancestors'
            )
            
            print(f"Found {len(pages)} pages in space '{self.space_key}'")
            return pages
            
        except Exception as e:
            print(f"Error fetching pages: {str(e)}")
            raise
    
    def clean_filename(self, title: str) -> str:
        """Clean page title to create a valid filename."""
        # Remove or replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '-', title)
        filename = re.sub(r'\s+', '-', filename)  # Replace spaces with hyphens
        filename = re.sub(r'-+', '-', filename)   # Replace multiple hyphens with single
        filename = filename.strip('-')            # Remove leading/trailing hyphens
        
        # Limit length and add .md extension
        if len(filename) > 100:
            filename = filename[:100]
        
        return f"{filename}.md"
    
    def download_attachment(self, attachment_url: str, filename: str) -> Optional[str]:
        """Download an attachment and return the local path."""
        try:
            response = requests.get(
                attachment_url,
                auth=(self.username, self.token),
                timeout=30
            )
            response.raise_for_status()
            
            # Save to attachments directory
            local_path = self.attachments_dir / filename
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Downloaded attachment: {filename}")
            return f"attachments/{filename}"
            
        except Exception as e:
            print(f"Error downloading attachment {filename}: {str(e)}")
            return None
    
    def process_html_content(self, html_content: str, page_id: str) -> str:
        """Process HTML content before converting to Markdown."""
        if not html_content:
            return ""
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Handle attachments and images
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                # Handle relative URLs
                if src.startswith('/'):
                    src = urljoin(self.confluence_url, src)
                
                # Download and replace with local path
                if 'download/attachments' in src:
                    filename = src.split('/')[-1].split('?')[0]
                    local_path = self.download_attachment(src, filename)
                    if local_path:
                        img['src'] = local_path
        
        # Handle links to other Confluence pages
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and 'pages/viewpage.action' in href:
                # Convert to relative reference if possible
                link['href'] = href
        
        return str(soup)
    
    def convert_to_markdown(self, html_content: str) -> str:
        """Convert HTML content to Markdown."""
        if not html_content:
            return ""
        
        # Configure markdownify options
        markdown_content = md(
            html_content,
            heading_style="ATX",  # Use # style headings
            bullets="-",          # Use - for bullet points
            strip=['script', 'style'],  # Remove script and style tags
            convert=['b', 'strong', 'i', 'em', 'u', 'strike', 'code', 'pre', 'p', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'a', 'img', 'table', 'tr', 'td', 'th', 'blockquote']
        )
        
        # Clean up excessive whitespace
        markdown_content = re.sub(r'\n\s*\n\s*\n', '\n\n', markdown_content)
        markdown_content = markdown_content.strip()
        
        return markdown_content
    
    def create_page_metadata(self, page: Dict) -> str:
        """Create YAML front matter for the page."""
        metadata = {
            'title': page['title'],
            'id': page['id'],
            'version': page['version']['number'],
            'created': page['version']['when'],
            'space': self.space_key,
            'url': f"{self.confluence_url}/pages/viewpage.action?pageId={page['id']}"
        }
        
        # Add ancestor information if available
        if 'ancestors' in page and page['ancestors']:
            metadata['parent'] = page['ancestors'][-1]['title']
        
        yaml_header = "---\n"
        for key, value in metadata.items():
            yaml_header += f"{key}: {json.dumps(value) if isinstance(value, str) else value}\n"
        yaml_header += "---\n\n"
        
        return yaml_header
    
    def export_page(self, page: Dict) -> bool:
        """Export a single page to Markdown."""
        try:
            page_title = page['title']
            page_id = page['id']
            
            print(f"Processing page: {page_title} (ID: {page_id})")
            
            # Get page content
            html_content = page.get('body', {}).get('storage', {}).get('value', '')
            
            if not html_content:
                print(f"  Warning: No content found for page '{page_title}'")
                html_content = ""
            
            # Process HTML content (handle attachments, etc.)
            processed_html = self.process_html_content(html_content, page_id)
            
            # Convert to Markdown
            markdown_content = self.convert_to_markdown(processed_html)
            
            # Create metadata header
            metadata = self.create_page_metadata(page)
            
            # Combine metadata and content
            full_content = metadata + markdown_content
            
            # Save to file
            filename = self.clean_filename(page_title)
            file_path = self.output_dir / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            print(f"  ✓ Exported to: {filename}")
            return True
            
        except Exception as e:
            print(f"  ✗ Error exporting page '{page.get('title', 'Unknown')}': {str(e)}")
            return False
    
    def export_all_pages(self) -> None:
        """Export all pages from the Confluence space."""
        start_time = datetime.now()
        
        try:
            # Get all pages
            pages = self.get_all_pages()
            
            if not pages:
                print("No pages found to export.")
                return
            
            # Export each page
            successful_exports = 0
            failed_exports = 0
            
            for i, page in enumerate(pages, 1):
                print(f"\n[{i}/{len(pages)}] ", end="")
                
                if self.export_page(page):
                    successful_exports += 1
                else:
                    failed_exports += 1
            
            # Print summary
            end_time = datetime.now()
            duration = end_time - start_time
            
            print(f"\n" + "="*50)
            print("EXPORT SUMMARY")
            print("="*50)
            print(f"Total pages processed: {len(pages)}")
            print(f"Successful exports: {successful_exports}")
            print(f"Failed exports: {failed_exports}")
            print(f"Output directory: {self.output_dir.absolute()}")
            print(f"Duration: {duration}")
            print("="*50)
            
        except Exception as e:
            print(f"Export failed: {str(e)}")
            raise


def main():
    """Main function to run the exporter."""
    try:
        exporter = ConfluenceExporter()
        exporter.export_all_pages()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
