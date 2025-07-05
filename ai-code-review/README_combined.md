# AI Code Review Tool

An automated code review tool that uses GitLab API to fetch merge request changes and Ollama AI to generate comprehensive code reviews. This tool can be used both as a command-line utility and as a REST API server.

## Features

- 🔍 Fetches merge request details and code changes from GitLab
- 🤖 Uses Ollama AI to analyze code and generate reviews
- 👥 Extracts author and reviewer information
- 📝 Posts AI-generated reviews as comments on merge requests
- ⚙️ Configurable review guidelines
- 🔐 Secure authentication with Personal Access Tokens
- 🌐 **REST API**: Simple HTTP endpoints for code review generation
- ⚡ **Async Processing**: Efficient handling of AI review generation
- 📚 **Interactive Documentation**: Automatic OpenAPI/Swagger documentation
- 🏥 **Health Monitoring**: Built-in health check endpoint

## Project Structure

This project follows a modular structure for better maintainability:

```
ai-code-review/
├── src/                     # Source code
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Main CLI entry point
│   ├── run.py              # Legacy CLI entry point
│   ├── server.py           # FastAPI server
│   ├── config.py           # Configuration management
│   ├── code_reviewer.py    # Main orchestrator
│   ├── gitlab_api.py       # GitLab API client
│   ├── ollama_api.py       # Ollama AI client
│   └── utils.py            # Utility functions
├── tests/                  # Test files
│   ├── test_server.py      # Server tests
│   └── test_setup.py       # Setup tests
├── requirements.txt        # Python dependencies
├── review_guidelines.txt   # AI review guidelines
├── .env.example           # Environment configuration example
└── README.md              # This file
```

### Module Dependencies

```
main.py
├── config.py
└── code_reviewer.py
    ├── gitlab_api.py
    ├── ollama_api.py
    └── utils.py

server.py
├── config.py
└── code_reviewer.py
    ├── gitlab_api.py
    ├── ollama_api.py
    └── utils.py
```

## Prerequisites

- Python 3.7+
- GitLab instance with API access
- Ollama running locally or accessible endpoint
- GitLab Personal Access Token with appropriate permissions

## Installation

1. Clone or navigate to the project directory:

```bash
cd ai-code-review
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your environment by copying the example and editing the `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# GitLab Configuration
GITLAB_URL=https://your-gitlab-instance.com
GITLAB_PAT=your_personal_access_token_here

# Ollama Configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# Review Configuration
REVIEWER_NAME=AI Code Reviewer
REVIEWER_EMAIL=ai-reviewer@example.com
OLLAMA_NUM_CTX=6122
```

## Configuration

### GitLab Setup

1. **Personal Access Token**: Create a GitLab Personal Access Token with the following scopes:

   - `api` - Full API access
   - `read_api` - Read API access
   - `read_repository` - Read repository access
   - `write_repository` - Write repository access (for posting comments)

2. **Project Access**: Ensure your token has access to the projects you want to review.

### Ollama Setup

1. **Install Ollama**: Follow the installation guide at [ollama.ai](https://ollama.ai)

2. **Pull a Model**: Download a suitable model for code review:

```bash
ollama pull llama3.1
# or
ollama pull codellama
# or
ollama pull llama2
```

3. **Start Ollama**: Ensure Ollama is running:

```bash
ollama serve
```

## Usage

### Command Line Interface

#### Basic Usage

Review a merge request by providing the MR ID:

```bash
python src/main.py 123
```

You'll be prompted to enter the project ID if not provided.

#### Advanced Usage

Provide both project ID and MR ID:

```bash
python src/main.py 456/123
```

Where:

- `456` is the GitLab project ID
- `123` is the merge request IID

#### Legacy Usage (backward compatibility)

```bash
python src/run.py 123
python src/run.py 456/123
```

#### Command Line Options

```bash
python src/main.py --help
```

Available options:

- `mr_input`: Merge Request ID or Project_ID/MR_ID format (required)
- `--config`: Path to custom .env config file (optional, default: `.env`)

#### As a Python Package

```python
from src.config import load_config
from src.code_reviewer import CodeReviewer

config = load_config()
reviewer = CodeReviewer(config)
success = reviewer.review_merge_request("123")
```

### REST API Server

#### Quick Start

Start the FastAPI server:

```bash
python src/server.py
```

The server will start on `http://localhost:8000`

#### API Endpoints

##### Health Check

```http
GET /health
```

##### Generate Code Review

```http
POST /review?project_id={project_id}&mr_id={mr_id}&should_post_comment={true|false}
```

**Parameters:**

- `project_id` (required): GitLab project ID
- `mr_id` (required): Merge request ID/IID
- `should_post_comment` (optional, default: false): Whether to post the review as a comment to GitLab

**Example Request:**

```bash
curl -X POST "http://localhost:8000/review?project_id=123&mr_id=456&should_post_comment=true"
```

**Example Response:**

```json
{
  "success": true,
  "review_content": "## 🤖 AI Code Review by AI Code Reviewer\n\n**Reviewed by:** AI Code Reviewer (ai-reviewer@example.com)\n**Review Date:** 2025-07-04 10:30:00\n\n### Summary\nThe code changes look good overall...",
  "posted_to_gitlab": true,
  "message": "Code review generated successfully and posted to GitLab",
  "merge_request_url": "https://your-gitlab.com/-/merge_requests/456"
}
```

#### Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation with Swagger UI.

#### API Usage Examples

##### 1. Generate Review Only (Don't Post to GitLab)

```bash
curl -X POST "http://localhost:8000/review?project_id=123&mr_id=456&should_post_comment=false"
```

##### 2. Generate and Post Review to GitLab

```bash
curl -X POST "http://localhost:8000/review?project_id=123&mr_id=456&should_post_comment=true"
```

##### 3. Using Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/review",
    params={
        "project_id": "123",
        "mr_id": "456",
        "should_post_comment": True
    }
)

result = response.json()
print(result["review_content"])
```

##### 4. Using JavaScript/fetch

```javascript
const response = await fetch(
  "http://localhost:8000/review?project_id=123&mr_id=456&should_post_comment=true",
  { method: "POST" }
);

const result = await response.json();
console.log(result.review_content);
```

## Configuration Options

All configuration is done through environment variables in the `.env` file:

| Variable         | Description                  | Required | Default                 |
| ---------------- | ---------------------------- | -------- | ----------------------- |
| `GITLAB_URL`     | Your GitLab instance URL     | Yes      | -                       |
| `GITLAB_PAT`     | GitLab Personal Access Token | Yes      | -                       |
| `OLLAMA_URL`     | Ollama server URL            | Yes      | -                       |
| `OLLAMA_MODEL`   | Ollama model name            | Yes      | -                       |
| `REVIEWER_NAME`  | Name shown in reviews        | No       | AI Code Reviewer        |
| `REVIEWER_EMAIL` | Email shown in reviews       | No       | ai-reviewer@example.com |
| `OLLAMA_NUM_CTX` | Context window size          | No       | 6122                    |

## Review Guidelines

The AI review is guided by the content in `review_guidelines.txt`. You can customize this file to match your team's coding standards and review criteria.

The default guidelines cover:

- Code quality and maintainability
- Best practices and coding standards
- Performance considerations
- Security implications
- Documentation and testing

## Output

The tool will:

1. Fetch the merge request details and changes
2. Generate an AI review based on the guidelines
3. Post the review as a comment on the merge request (if requested)
4. Display the review URL for easy access

Example CLI output:

```
Reviewing MR 123 in project 456...
Fetching merge request details...
Fetching merge request changes...
Author: John Doe (john.doe@example.com)
Reviewer: Jane Smith (jane.smith@example.com)
Preparing code for AI review...
Generating AI review...
Posting review to GitLab...
✅ Code review completed successfully!
Review posted to: https://gitlab.example.com/merge_requests/123
```

## Benefits of Modular Structure

1. **Separation of Concerns**: Each module has a single responsibility
2. **Easier Testing**: Individual components can be tested in isolation
3. **Better Maintainability**: Changes to specific functionality are isolated
4. **Reusability**: Components can be reused in other projects
5. **Cleaner Code**: Smaller, focused files are easier to understand
6. **Easier Debugging**: Issues can be traced to specific modules

## Error Handling

### API Error Responses

The API returns appropriate HTTP status codes:

- **200**: Success
- **400**: Bad Request (invalid parameters)
- **500**: Internal Server Error

Error responses include detailed error messages:

```json
{
  "detail": "Invalid input: Project ID must be numeric"
}
```

### Common Issues

1. **Import errors**: Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

2. **GitLab API errors**: Check your PAT permissions and GitLab URL

3. **Ollama connection issues**: Verify Ollama is running and accessible

4. **Model not found**: Ensure the specified model is pulled in Ollama:

```bash
ollama list
ollama pull <model-name>
```

5. **"Code reviewer not initialized"**:

   - Check your `.env` file configuration
   - Ensure all required environment variables are set

6. **Large merge requests timeout**:
   - Consider increasing `OLLAMA_NUM_CTX` for larger context
   - The system automatically truncates very large diffs

### Error Messages

- `Missing required environment variable`: Check your `.env` file configuration
- `GitLab API Error`: Verify your PAT and project access
- `Error communicating with Ollama`: Check Ollama service status

## Deployment

### Docker Deployment

The project includes Docker support. Use the provided `Dockerfile` and `docker-compose.server.yml`:

```bash
# Build the image
docker build -t ai-code-review .

# Run with docker-compose
docker-compose -f docker-compose.server.yml up
```

### Production Deployment

For production, consider:

1. **Use a production ASGI server** like Gunicorn with Uvicorn workers
2. **Set up reverse proxy** with nginx
3. **Enable HTTPS** with SSL certificates
4. **Configure logging** and monitoring
5. **Set up health checks** and auto-restart

Example production command:

```bash
gunicorn src.server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_server.py

# Run with verbose output
python -m pytest tests/ -v
```

## Monitoring

The server includes logging for all operations. Check the console output for:

- 🔍 Review start notifications
- 📥 Data fetching progress
- 🧠 AI review generation
- ✅ Success confirmations
- ❌ Error details

### Debug Mode

Start the server with debug logging:

```bash
python src/server.py --log-level debug
```

## Security Considerations

- Store your GitLab PAT securely and never commit it to version control
- Use environment variables or secure vault systems for sensitive data
- Regularly rotate your access tokens
- Review the AI-generated comments before relying on them for critical decisions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is provided as-is for educational and development purposes.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review GitLab API documentation
3. Check Ollama documentation
4. Create an issue in the project repository
