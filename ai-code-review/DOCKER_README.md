# AI Code Review Docker Setup

This Docker Compose setup provides a complete AI-powered code review system with Telegram integration.

## Services

### 1. AI Code Review Server (`ai-code-review-server`)

- **Purpose**: FastAPI server that provides AI-powered code reviews for GitLab merge requests
- **Port**: 8000
- **Base Image**: Python 3.11-slim
- **Security**: Runs as non-root user

### 2. Telegram Watcher (`telegram-watcher`)

- **Purpose**: Monitors Telegram messages and forwards code review requests to the AI server
- **Base Image**: Python 3.11-slim
- **Security**: Runs as non-root user
- **Data Persistence**: Uses mounted volume for processed messages tracking

## Quick Start

1. **Copy environment configuration**:

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** with your actual values:

   - GitLab URL and Personal Access Token
   - Ollama configuration
   - Telegram bot credentials

3. **Start services**:

   ```bash
   docker-compose up -d
   ```

4. **Check logs**:
   ```bash
   docker-compose logs -f
   ```

## Directory Structure

```
ai-code-review/
├── docker-compose.yml          # Main orchestration file
├── .env.example               # Environment template
├── logs/                      # Shared logs directory
├── src/                       # AI Code Review Server
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── server.py
│   └── ...
└── telegram-watcher/          # Telegram Watcher Service
    ├── Dockerfile
    ├── requirements.txt
    ├── run.py
    ├── data/                  # Persistent data storage
    └── ...
```

## Networks

- **ai-code-review-network**: Isolated bridge network for inter-service communication

## Volumes

### AI Code Review Server

- `./src/review_guidelines.txt:/app/src/review_guidelines.txt:ro` - Review guidelines (read-only)
- `./logs:/app/logs` - Shared logs directory

### Telegram Watcher

- `./telegram-watcher/data:/app/data` - Persistent data for message tracking
- `./logs:/app/logs` - Shared logs directory

## Health Checks

Both services include health checks:

- **AI Server**: HTTP check on `/health` endpoint
- **Telegram Watcher**: File existence check for main script

## Environment Variables

See `.env.example` for complete list of required and optional environment variables.

## Troubleshooting

1. **Check service status**:

   ```bash
   docker-compose ps
   ```

2. **View logs**:

   ```bash
   docker-compose logs [service-name]
   ```

3. **Restart services**:

   ```bash
   docker-compose restart
   ```

4. **Rebuild after code changes**:
   ```bash
   docker-compose up --build
   ```

## Security Notes

- Both containers run as non-root users
- Read-only mounts where applicable
- Isolated network for inter-service communication
- Health checks for monitoring service health
