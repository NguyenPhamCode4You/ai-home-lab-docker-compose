# AI Code Review FastAPI Server

A FastAPI-based web service that provides AI-powered code reviews for GitLab merge requests.

## Features

- **REST API**: Simple HTTP endpoints for code review generation
- **Configurable**: Choose whether to post comments directly to GitLab or just return review content
- **Async Processing**: Efficient handling of AI review generation
- **Interactive Documentation**: Automatic OpenAPI/Swagger documentation
- **Health Monitoring**: Built-in health check endpoint

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file with your configuration:

```env
GITLAB_URL=https://your-gitlab-instance.com
GITLAB_PAT=your_personal_access_token
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1
REVIEWER_NAME=AI Code Reviewer
REVIEWER_EMAIL=ai-reviewer@example.com
OLLAMA_NUM_CTX=6122
```

### 3. Start the Server

**Windows:**

```cmd
start_server.bat
```

**Linux/Mac:**

```bash
python server.py
```

The server will start on `http://localhost:8000`

## API Endpoints

### Health Check

```http
GET /health
```

### Generate Code Review

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

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation with Swagger UI.

## Usage Examples

### 1. Generate Review Only (Don't Post to GitLab)

```bash
curl -X POST "http://localhost:8000/review?project_id=123&mr_id=456&should_post_comment=false"
```

### 2. Generate and Post Review to GitLab

```bash
curl -X POST "http://localhost:8000/review?project_id=123&mr_id=456&should_post_comment=true"
```

### 3. Using Python requests

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

### 4. Using JavaScript/fetch

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

## GitLab Personal Access Token

To create a GitLab Personal Access Token:

1. Go to your GitLab instance
2. Navigate to **User Settings** → **Access Tokens**
3. Create a new token with the following scopes:
   - `api` (for full API access)
   - `read_repository` (to read merge request changes)
   - `write_repository` (to post comments)

## Error Handling

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

## Deployment

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "server.py"]
```

Build and run:

```bash
docker build -t ai-code-review-server .
docker run -p 8000:8000 --env-file .env ai-code-review-server
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
gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Monitoring

The server includes logging for all operations. Check the console output for:

- 🔍 Review start notifications
- 📥 Data fetching progress
- 🧠 AI review generation
- ✅ Success confirmations
- ❌ Error details

## Troubleshooting

### Common Issues

1. **"Code reviewer not initialized"**

   - Check your `.env` file configuration
   - Ensure all required environment variables are set

2. **GitLab API errors**

   - Verify your GitLab URL and Personal Access Token
   - Check token permissions

3. **Ollama connection errors**

   - Ensure Ollama is running on the specified URL
   - Verify the model name is correct

4. **Large merge requests timeout**
   - Consider increasing `OLLAMA_NUM_CTX` for larger context
   - The system automatically truncates very large diffs

### Debug Mode

Start the server with debug logging:

```bash
python server.py --log-level debug
```
