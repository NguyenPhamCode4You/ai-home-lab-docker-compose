# Telegram Watcher for AI Code Review

This bot monitors a Telegram chat for code review requests and automatically triggers the AI code review system.

## Setup

1. **Run the setup script** (Windows):

   ```bash
   setup.bat
   ```

2. **Configure environment variables** in `.env`:

   - `TELEGRAM_BOT_TOKEN`: Get from @BotFather on Telegram
   - `TELEGRAM_CHAT_ID`: Your chat or group ID (use @userinfobot to find it)
   - `TELEGRAM_THREAD_ID` (optional): Specific thread ID for filtering messages in threaded conversations
   - `REVIEW_API_URL`: Your review API endpoint (default: http://localhost:8000/review)

3. **Start the bot**:
   ```bash
   python run.py
   ```

## Usage

Send a message in the configured Telegram chat with the format:

```
review-pr-PROJECT_ID/MERGE_REQUEST_ID
```

Example:

```
review-pr-123/456
```

The bot will:

1. Parse the project ID and merge request ID
2. Send a request to the AI code review API
3. The review will be automatically posted to GitLab

## Thread Filtering

If you want to monitor only a specific thread in a group chat:

1. **Find the thread ID**:
   - Enable "Show Message IDs" in Telegram settings
   - Send a message in the desired thread
   - Look for the `message_thread_id` in the message details
2. **Set the thread ID** in your `.env` file:

   ```
   TELEGRAM_THREAD_ID=your_thread_id_here
   ```

3. **Behavior**:
   - If `TELEGRAM_THREAD_ID` is set: Only messages from that specific thread will be processed
   - If `TELEGRAM_THREAD_ID` is not set: All messages from the chat will be monitored

## Features

- **Persistent state**: The bot remembers the last processed message (stored in `last_update_id.txt`)
- **Environment-based configuration**: Uses `.env` file for secure configuration
- **Thread filtering**: Optional support for monitoring specific threads in group chats
- **Error handling**: Robust error handling and logging
- **Auto-posting**: Automatically posts reviews to GitLab

## File Structure

- `run.py` - Main bot script
- `.env` - Configuration file (create from `.env.example`)
- `.env.example` - Template configuration file
- `requirements.txt` - Python dependencies
- `setup.bat` - Windows setup script
- `last_update_id.txt` - Stores last processed update ID (auto-generated)
