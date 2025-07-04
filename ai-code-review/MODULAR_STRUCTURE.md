# AI Code Review Tool - Modular Structure

This directory contains a modular AI code review tool that has been split into multiple files for better maintainability.

## File Structure

- **`main.py`** - Main entry point with argument parsing and error handling
- **`run.py`** - Legacy entry point for backward compatibility
- **`config.py`** - Configuration management and environment variable loading
- **`gitlab_api.py`** - GitLab API client for merge request operations
- **`ollama_api.py`** - Ollama AI client for generating code reviews
- **`code_reviewer.py`** - Main orchestrator that coordinates the review process
- **`utils.py`** - Utility functions for formatting and helper operations
- **`__init__.py`** - Package initialization file

## Usage

### Direct usage (new modular approach):

```bash
python main.py <merge_request_id>
python main.py project_id/merge_request_id
```

### Legacy usage (backward compatibility):

```bash
python run.py <merge_request_id>
python run.py project_id/merge_request_id
```

### As a Python package:

```python
from config import load_config
from code_reviewer import CodeReviewer

config = load_config()
reviewer = CodeReviewer(config)
success = reviewer.review_merge_request("123")
```

## Benefits of Modular Structure

1. **Separation of Concerns**: Each module has a single responsibility
2. **Easier Testing**: Individual components can be tested in isolation
3. **Better Maintainability**: Changes to specific functionality are isolated
4. **Reusability**: Components can be reused in other projects
5. **Cleaner Code**: Smaller, focused files are easier to understand
6. **Easier Debugging**: Issues can be traced to specific modules

## Module Dependencies

```
main.py
├── config.py
└── code_reviewer.py
    ├── gitlab_api.py
    ├── ollama_api.py
    └── utils.py
```

## Configuration

All modules use the same `.env` file for configuration. See the main README.md for configuration details.
