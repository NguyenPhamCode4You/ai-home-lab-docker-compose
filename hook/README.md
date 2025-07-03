# GitLab to Azure DevOps Sync Server

This Python server listens for GitLab webhook events (commits and merge requests) and automatically syncs the code to an Azure DevOps repository to trigger build and test pipelines.

## Features

- ✅ Listens for GitLab webhook events (Push Hook, Merge Request Hook)
- ✅ Downloads code from GitLab using API
- ✅ Pushes code to Azure DevOps repository
- ✅ Webhook signature verification for security
- ✅ Comprehensive logging
- ✅ Health check endpoint
- ✅ Manual sync endpoint for testing

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the example environment file and configure it:

```bash
copy .env.example .env
```

Edit `.env` and fill in your configuration:

```env
# GitLab Configuration
GITLAB_URL=https://gitlab.com
GITLAB_ACCESS_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxx
GITLAB_PROJECT_ID=12345678
GITLAB_WEBHOOK_SECRET=optional_webhook_secret

# Azure DevOps Configuration
AZURE_DEVOPS_URL=https://dev.azure.com/your_organization
AZURE_DEVOPS_TOKEN=your_azure_devops_pat
AZURE_DEVOPS_PROJECT=YourProject
AZURE_DEVOPS_REPO=your-repo-name

# Server Configuration
PORT=5000
HOST=0.0.0.0
WORK_DIR=./sync_workspace
```

### 3. GitLab Access Token

Create a GitLab Personal Access Token with the following scopes:

- `read_api`
- `read_repository`

### 4. Azure DevOps Access Token

Create an Azure DevOps Personal Access Token with the following permissions:

- **Code**: Read & Write
- **Build**: Read (if you want to trigger builds)

### 5. GitLab Webhook Configuration

In your GitLab project, go to Settings > Webhooks and add a new webhook:

- **URL**: `http://your-server:5000/webhook/gitlab`
- **Secret Token**: (optional, but recommended for security)
- **Trigger Events**:
  - ✅ Push events
  - ✅ Merge request events
- **SSL verification**: Enable if using HTTPS

## Running the Server

### Development Mode

```bash
python server.py
```

### Production Mode

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

## API Endpoints

### Webhook Endpoint

- **POST** `/webhook/gitlab` - Receives GitLab webhook events

### Health Check

- **GET** `/health` - Returns server health status

### Manual Sync (for testing)

- **POST** `/sync/manual` - Manually trigger a sync

Example manual sync request:

```bash
curl -X POST http://localhost:5000/sync/manual \
  -H "Content-Type: application/json" \
  -d '{
    "ref": "main",
    "message": "Manual sync test",
    "branch": "main"
  }'
```

## How It Works

1. **Webhook Reception**: Server receives GitLab webhook for push or merge request events
2. **Code Download**: Downloads the latest code from GitLab using the Repository API
3. **Git Operations**: Extracts code, initializes git repo, and configures Azure DevOps remote
4. **Code Push**: Pushes the code to Azure DevOps repository
5. **Pipeline Trigger**: Azure DevOps automatically triggers build/test pipelines on push

## Supported Events

### Push Events

- Triggered on direct commits to any branch
- Syncs the specific commit to Azure DevOps

### Merge Request Events

- Triggered when merge requests are merged
- Syncs the target branch after merge

## Security

- Webhook signature verification (optional but recommended)
- Personal Access Tokens for API authentication
- HTTPS support for webhook endpoints
- Comprehensive logging for audit trails

## Troubleshooting

### Common Issues

1. **Authentication Errors**

   - Verify GitLab and Azure DevOps tokens have correct permissions
   - Check token expiration dates

2. **Webhook Not Triggering**

   - Verify webhook URL is accessible from GitLab
   - Check webhook configuration in GitLab project settings
   - Review server logs for error messages

3. **Git Push Failures**
   - Ensure Azure DevOps repository exists
   - Verify Azure DevOps token has write permissions
   - Check network connectivity to Azure DevOps

### Logs

The server logs to both console and `gitlab_sync.log` file. Check logs for detailed error information:

```bash
tail -f gitlab_sync.log
```

## Docker Support

You can also run this server in a Docker container. Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY server.py .
COPY .env .

EXPOSE 5000
CMD ["python", "server.py"]
```

Build and run:

```bash
docker build -t gitlab-azure-sync .
docker run -p 5000:5000 gitlab-azure-sync
```

## License

MIT License
