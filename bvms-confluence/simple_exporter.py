#!/usr/bin/env python3
"""
Simple Confluence Page Fetcher

A simplified script to fetch pages from Confluence using basic requests
and convert them to Markdown.
"""

import os
import re
import json
import requests
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urljoin
from datetime import datetime

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SimpleConfluenceExporter:
    """Simplified Confluence exporter using requests library."""
    
    def __init__(self):
        """Initialize the exporter with configuration."""
        self.confluence_url = os.getenv('CONFLUENCE_URL')
        self.token = os.getenv('CONFLUENCE_TOKEN')
        self.username = os.getenv('CONFLUENCE_USERNAME')
        self.space_key = os.getenv('CONFLUENCE_SPACE_KEY')
        self.output_dir = Path(os.getenv('OUTPUT_DIR', 'output'))
        self.max_pages = int(os.getenv('MAX_PAGES', 1000))
        
        # Validate required configuration
        if not all([self.confluence_url, self.token, self.username, self.space_key]):
            raise ValueError("Missing required configuration. Please check your .env file.")
        
        # Setup API base URL
        self.api_url = f"{self.confluence_url}/wiki/rest/api"
        self.auth = (self.username, self.token)
        
        # Create output directories
        self.output_dir.mkdir(exist_ok=True)
        self.attachments_dir = self.output_dir / 'attachments'
        self.attachments_dir.mkdir(exist_ok=True)
        
        print(f"Initialized Confluence exporter for space: {self.space_key}")
        print(f"Output directory: {self.output_dir.absolute()}")
    
    def make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make authenticated request to Confluence API."""
        url = f"{self.api_url}/{endpoint}"
        
        try:
            response = requests.get(url, auth=self.auth, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {str(e)}")
            raise
    
    def get_all_pages(self) -> List[Dict]:
        """Retrieve all pages from the specified space."""
        print("Fetching all pages from Confluence...")
        
        pages = []
        start = 0
        limit = 50
        
        while len(pages) < self.max_pages:
            params = {
                'spaceKey': self.space_key,
                'start': start,
                'limit': limit,
                'expand': 'body.storage,version,ancestors'
            }
            
            try:
                response = self.make_request('content', params)
                page_batch = response.get('results', [])
                
                if not page_batch:
                    break
                
                pages.extend(page_batch)
                
                if len(page_batch) < limit:
                    break
                
                start += limit
                print(f"Fetched {len(pages)} pages so far...")
                
            except Exception as e:
                print(f"Error fetching pages: {str(e)}")
                break
        
        print(f"Found {len(pages)} pages in space '{self.space_key}'")
        return pages
    
    def clean_filename(self, title: str) -> str:
        """Clean page title to create a valid filename."""
        # Remove or replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '-', title)
        filename = re.sub(r'\s+', '-', filename)
        filename = re.sub(r'-+', '-', filename)
        filename = filename.strip('-')
        
        # Limit length
        if len(filename) > 100:
            filename = filename[:100]
        
        return f"{filename}.md"
    
    def html_to_markdown_simple(self, html: str) -> str:
        """Simple HTML to Markdown conversion."""
        if not html:
            return ""
        
        # Basic HTML tag replacements
        markdown = html
        
        # Headers
        markdown = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n\n', markdown, flags=re.DOTALL)
        markdown = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n\n', markdown, flags=re.DOTALL)
        markdown = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1\n\n', markdown, flags=re.DOTALL)
        markdown = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1\n\n', markdown, flags=re.DOTALL)
        markdown = re.sub(r'<h5[^>]*>(.*?)</h5>', r'##### \1\n\n', markdown, flags=re.DOTALL)
        markdown = re.sub(r'<h6[^>]*>(.*?)</h6>', r'###### \1\n\n', markdown, flags=re.DOTALL)
        
        # Bold and italic
        markdown = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', markdown, flags=re.DOTALL)
        markdown = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', markdown, flags=re.DOTALL)
        markdown = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', markdown, flags=re.DOTALL)
        markdown = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', markdown, flags=re.DOTALL)
        
        # Code
        markdown = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', markdown, flags=re.DOTALL)
        markdown = re.sub(r'<pre[^>]*>(.*?)</pre>', r'```\n\1\n```\n\n', markdown, flags=re.DOTALL)
        
        # Links
        markdown = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', markdown, flags=re.DOTALL)
        
        # Images
        markdown = re.sub(r'<img[^>]*src=["\']([^"\']*)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*/?>', r'![\2](\1)', markdown)
        markdown = re.sub(r'<img[^>]*src=["\']([^"\']*)["\'][^>]*/?>', r'![](\1)', markdown)
        
        # Lists
        markdown = re.sub(r'<ul[^>]*>', '\n', markdown)
        markdown = re.sub(r'</ul>', '\n', markdown)
        markdown = re.sub(r'<ol[^>]*>', '\n', markdown)
        markdown = re.sub(r'</ol>', '\n', markdown)
        markdown = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', markdown, flags=re.DOTALL)
        
        # Paragraphs and breaks
        markdown = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', markdown, flags=re.DOTALL)
        markdown = re.sub(r'<br[^>]*/?>', r'\n', markdown)
        
        # Tables (basic)
        markdown = re.sub(r'<table[^>]*>', '\n', markdown)
        markdown = re.sub(r'</table>', '\n', markdown)
        markdown = re.sub(r'<tr[^>]*>', '| ', markdown)
        markdown = re.sub(r'</tr>', ' |\n', markdown)
        markdown = re.sub(r'<td[^>]*>(.*?)</td>', r'\1 | ', markdown, flags=re.DOTALL)
        markdown = re.sub(r'<th[^>]*>(.*?)</th>', r'\1 | ', markdown, flags=re.DOTALL)
        
        # Remove remaining HTML tags
        markdown = re.sub(r'<[^>]+>', '', markdown)
        
        # Clean up excessive whitespace
        markdown = re.sub(r'\n\s*\n\s*\n', '\n\n', markdown)
        markdown = re.sub(r'[ \t]+', ' ', markdown)
        markdown = markdown.strip()
        
        return markdown
    
    def create_page_metadata(self, page: Dict) -> str:
        """Create YAML front matter for the page."""
        metadata = {
            'title': page['title'],
            'id': page['id'],
            'type': page['type'],
            'status': page['status'],
            'space': self.space_key,
            'created': page['version']['when'] if 'version' in page else '',
            'url': f"{self.confluence_url}/wiki/pages/viewpage.action?pageId={page['id']}"
        }
        
        # Add ancestor information if available
        if 'ancestors' in page and page['ancestors']:
            metadata['parent'] = page['ancestors'][-1]['title']
        
        yaml_header = "---\n"
        for key, value in metadata.items():
            if isinstance(value, str):
                yaml_header += f"{key}: \"{value}\"\n"
            else:
                yaml_header += f"{key}: {value}\n"
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
            
            # Convert to Markdown
            markdown_content = self.html_to_markdown_simple(html_content)
            
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
        exporter = SimpleConfluenceExporter()
        exporter.export_all_pages()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
