import requests
import time
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID", "0"))  # Convert to int
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
TARGET_API = os.getenv("REVIEW_API_URL", "http://localhost:8000/review")  # Default to port 8000

# File to store last update ID
UPDATE_ID_FILE = "last_update_id.txt"

def read_last_update_id():
    """Read the last update ID from file"""
    try:
        if os.path.exists(UPDATE_ID_FILE):
            with open(UPDATE_ID_FILE, 'r') as f:
                return int(f.read().strip())
        return 0
    except (ValueError, FileNotFoundError):
        return 0

def save_last_update_id(update_id):
    """Save the last update ID to file"""
    try:
        with open(UPDATE_ID_FILE, 'w') as f:
            f.write(str(update_id))
    except Exception as e:
        print(f"[ERROR] Failed to save update ID: {e}")

def validate_env_vars():
    """Validate required environment variables"""
    if not BOT_TOKEN:
        raise ValueError("Missing required environment variable: TELEGRAM_BOT_TOKEN")
    if not CHAT_ID:
        raise ValueError("Missing required environment variable: TELEGRAM_CHAT_ID")
    print(f"[✅] Using Telegram Bot Token: {BOT_TOKEN[:10]}...")
    print(f"[✅] Using Chat ID: {CHAT_ID}")
    print(f"[✅] Using Review API: {TARGET_API}")

def fetch_latest_message(offset):
    try:
        response = requests.get(API_URL, params={"offset": offset, "limit": 1}, timeout=10)
        response.raise_for_status()
        updates = response.json().get("result", [])
        if updates:
            update = updates[0]
            return update
    except Exception as e:
        print(f"[ERROR] Failed to fetch message: {e}")
    return None

def extract_review_info(text):
    pattern = r"^review-pr-(\w+)/(\w+)$"
    match = re.match(pattern, text.strip())
    if match:
        return match.group(1), match.group(2)
    return None, None

def send_to_system(project_id, merge_id):
    """Send review request to the system API using query parameters"""
    params = {
        "project_id": project_id,
        "mr_id": merge_id,
        "post_review_to_gitlab": True  # Automatically post to GitLab
    }
    try:
        response = requests.post(TARGET_API, params=params, timeout=30)
        response.raise_for_status()
        result = response.json()
        if result.get("success"):
            print(f"[✅] Review generated successfully for {project_id}/{merge_id}")
            if result.get("posted_to_gitlab"):
                print(f"[✅] Review posted to GitLab: {result.get('merge_request_url', 'N/A')}")
        else:
            print(f"[⚠️] Review failed: {result.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"[❌] Failed to POST: {e}")

def main():
    # Validate environment variables
    validate_env_vars()
    
    # Read last update ID from file
    last_update_id = read_last_update_id()
    print(f"[ℹ️] Starting from update ID: {last_update_id}")
    
    print("[🤖 Bot is running...]")
    while True:
        update = fetch_latest_message(offset=last_update_id + 1)
        if update:
            current_update_id = update["update_id"]
            message = update.get("message")
            if message and message["chat"]["id"] == CHAT_ID:
                text = message.get("text", "")
                project_id, merge_id = extract_review_info(text)
                if project_id and merge_id:
                    print(f"[📝] Processing review request: {project_id}/{merge_id}")
                    send_to_system(project_id, merge_id)
                    # Save update ID only after successful processing
                    save_last_update_id(current_update_id)
                    last_update_id = current_update_id
                else:
                    print(f"[❌] Invalid format. Expected: review-pr-<project_id>/<merge_id>. Got: {text}")
                    # Still update the ID to avoid processing the same message again
                    save_last_update_id(current_update_id)
                    last_update_id = current_update_id
            else:
                # Update ID even if message is not from target chat
                save_last_update_id(update["update_id"])
                last_update_id = update["update_id"]
        time.sleep(2)  # Increased sleep time to be more gentle on APIs

if __name__ == "__main__":
    main()
