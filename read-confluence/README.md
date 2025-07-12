# 🔒 READ-ONLY Confluence to Markdown Exporter

A **READ-ONLY** Python script to extract all pages from a Confluence workspace and convert them to Markdown format.

## ⚠️ SAFETY GUARANTEE ⚠️

**This project is 100% READ-ONLY:**

- ✅ **ONLY reads** data from your Confluence space
- ✅ **NEVER writes, modifies, or deletes** any Confluence content
- ✅ **Only creates local files** on your computer
- ✅ **Your Confluence space remains completely unchanged**
- ✅ Uses only GET requests to the Confluence API

## Features

- Extract all pages from a Confluence workspace using READ-ONLY API calls
- Convert Confluence pages to clean Markdown format locally
- Preserve page hierarchy and structure in exported files
- Support for authentication via API token
- Two versions available: full-featured and simplified
- Complete safety - no risk to your Confluence data

## Available Scripts

1. **confluence_exporter.py** - Full-featured READ-ONLY exporter (requires additional dependencies)
2. **simple_exporter.py** - Simplified READ-ONLY exporter using only basic libraries ⭐ **Recommended**
3. **test_connection.py** - Test your Confluence connection (READ-ONLY) before running the exporter

**All scripts are READ-ONLY and will never modify your Confluence space.**

📖 **For detailed safety information, see [SAFETY.md](SAFETY.md)**

## Setup

1. Install basic dependencies:

```bash
pip install -r requirements.txt
```

**Note**: This installs only the basic requirements. For the full-featured exporter, you'll need additional packages (see Usage section below).

2. Copy `.env.example` to `.env` and configure your settings:

```bash
cp .env.example .env
```

3. Edit `.env` with your Confluence details:

```
CONFLUENCE_URL=https://your-company.atlassian.net
CONFLUENCE_TOKEN=your-api-token
CONFLUENCE_USERNAME=your-email@company.com
CONFLUENCE_SPACE_KEY=your-space-key
```

## Usage

### Quick Start (Recommended - 100% Safe)

1. Test your READ-ONLY connection first:

```bash
python test_connection.py
```

2. Run the simplified READ-ONLY exporter:

```bash
python simple_exporter.py
```

**Both scripts are READ-ONLY and will not modify your Confluence space in any way.**

### Full-Featured Exporter

For advanced features like better HTML-to-Markdown conversion and official Atlassian API support:

```bash
# Install additional packages
pip install atlassian-python-api markdownify

# Then run the full exporter
python confluence_exporter.py
```

**Note**: The `confluence_exporter.py` requires additional packages. If you get import errors, use the simplified version instead.

The script will:

1. Connect to your Confluence workspace
2. Retrieve all pages from the specified space
3. Convert each page to Markdown
4. Save the files in the `output/` directory

## Configuration

You can modify the following settings in the script:

- Output directory path
- Page filtering options
- Markdown conversion settings
- File naming conventions

## Output Structure

```
output/
├── page-title-1.md
├── page-title-2.md
├── subpage-title.md
└── attachments/
    ├── image1.png
    └── document1.pdf
```

## API Token Setup

1. Go to your Atlassian account settings
2. Navigate to Security → API tokens
3. Create a new API token
4. Copy the token to your `.env` file
