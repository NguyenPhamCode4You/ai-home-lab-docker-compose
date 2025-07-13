#!/usr/bin/env python3
"""
Clean Blank Files Script
This script recursively searches through the ./docs folder and deletes any files with blank content.
"""

import os
import sys
from pathlib import Path


def is_file_blank(file_path):
    """
    Check if a file is blank (empty or contains only whitespace).
    
    Args:
        file_path (Path): Path to the file to check
        
    Returns:
        bool: True if file is blank, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read().strip()
            return len(content) == 0
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False


def find_and_delete_blank_files(docs_folder):
    """
    Recursively find and delete blank files in the specified folder.
    
    Args:
        docs_folder (str): Path to the docs folder to search
        
    Returns:
        tuple: (deleted_count, total_files_checked)
    """
    docs_path = Path(docs_folder)
    
    if not docs_path.exists():
        print(f"Error: Folder '{docs_folder}' does not exist.")
        return 0, 0
    
    if not docs_path.is_dir():
        print(f"Error: '{docs_folder}' is not a directory.")
        return 0, 0
    
    deleted_count = 0
    total_files_checked = 0
    
    print(f"Searching for blank files in: {docs_path.absolute()}")
    print("-" * 50)
    
    # Recursively walk through all files in the docs folder
    for file_path in docs_path.rglob('*'):
        if file_path.is_file():
            total_files_checked += 1
            
            if is_file_blank(file_path):
                try:
                    print(f"Deleting blank file: {file_path.relative_to(docs_path)}")
                    file_path.unlink()
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")
            else:
                # Optional: print non-blank files for debugging
                # print(f"Non-blank file: {file_path.relative_to(docs_path)}")
                pass
    
    return deleted_count, total_files_checked


def main():
    """Main function to run the blank file cleanup."""
    docs_folder = "./docs"
    
    print("Clean Blank Files Script")
    print("=" * 30)
    
    # Get user confirmation before proceeding
    response = input(f"This script will delete all blank files in '{docs_folder}' recursively. Continue? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("Operation cancelled.")
        return
    
    deleted_count, total_files_checked = find_and_delete_blank_files(docs_folder)
    
    print("-" * 50)
    print(f"Summary:")
    print(f"Total files checked: {total_files_checked}")
    print(f"Blank files deleted: {deleted_count}")
    print(f"Remaining files: {total_files_checked - deleted_count}")
    
    if deleted_count > 0:
        print(f"\n✓ Successfully cleaned up {deleted_count} blank file(s).")
    else:
        print("\n✓ No blank files found.")


if __name__ == "__main__":
    main()