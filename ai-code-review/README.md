# AI Code Review Tool for GitLab

An automated code review tool that uses GitLab API to fetch merge request changes and Ollama AI to generate comprehensive code reviews.

## Features

- 🔍 Fetches merge request details and code changes from GitLab
- 🤖 Uses Ollama AI to analyze code and generate reviews
- 👥 Extracts author and reviewer information
- 📝 Posts AI-generated reviews as comments on merge requests
- ⚙️ Configurable review guidelines
- 🔐 Secure authentication with Personal Access Tokens

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

3. Configure your environment by editing the `.env` file:

```bash
# GitLab Configuration
GITLAB_URL=https://your-gitlab-instance.com
GITLAB_PAT=your_personal_access_token_here

# Ollama Configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Review Configuration
REVIEWER_NAME=AI Code Reviewer
REVIEWER_EMAIL=ai-reviewer@example.com
```

## Configuration

### GitLab Setup

1. **Personal Access Token**: Create a GitLab Personal Access Token with the following scopes:

   - `api` - Full API access
   - `read_api` - Read API access
   - `read_repository` - Read repository access

2. **Project Access**: Ensure your token has access to the projects you want to review.

### Ollama Setup

1. **Install Ollama**: Follow the installation guide at [ollama.ai](https://ollama.ai)

2. **Pull a Model**: Download a suitable model for code review:

```bash
ollama pull llama2
# or
ollama pull codellama
# or
ollama pull llama3
```

3. **Start Ollama**: Ensure Ollama is running:

```bash
ollama serve
```

## Usage

### Basic Usage

Review a merge request by providing the MR ID:

```bash
python run.py 123
```

You'll be prompted to enter the project ID if not provided.

### Advanced Usage

Provide both project ID and MR ID:

```bash
python run.py 456/123
```

Where:

- `456` is the GitLab project ID
- `123` is the merge request IID

### Command Line Options

```bash
python run.py --help
```

Available options:

- `mr_input`: Merge Request ID or Project_ID/MR_ID format (required)
- `--config`: Path to custom .env config file (optional, default: `.env`)

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
3. Post the review as a comment on the merge request
4. Display the review URL for easy access

Example output:

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

## Troubleshooting

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

### Error Messages

- `Missing required environment variable`: Check your `.env` file configuration
- `GitLab API Error`: Verify your PAT and project access
- `Error communicating with Ollama`: Check Ollama service status

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
