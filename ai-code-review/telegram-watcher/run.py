import requests
import time
import re
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID", "0"))  # Convert to int
THREAD_ID = os.getenv("TELEGRAM_THREAD_ID")  # Optional thread ID for filtering
THREAD_ID = int(THREAD_ID) if THREAD_ID and THREAD_ID.strip() else None
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
TARGET_API = os.getenv("TARGET_API_URL", "http://localhost:8000")  # Default to port 8000

# File to store processed messages
PROCESSED_MESSAGES_FILE = os.path.join(os.getenv("DATA_DIR", "/app/data"), "processed_messages.txt")

def read_processed_messages():
    """Read the set of processed message IDs from file"""
    try:
        # Ensure the data directory exists
        data_dir = os.path.dirname(PROCESSED_MESSAGES_FILE)
        os.makedirs(data_dir, exist_ok=True)
        
        if os.path.exists(PROCESSED_MESSAGES_FILE):
            with open(PROCESSED_MESSAGES_FILE, 'r') as f:
                return set(line.strip() for line in f if line.strip())
        return set()
    except Exception as e:
        print(f"[ERROR] Failed to read processed messages: {e}")
        return set()

def save_processed_message(chat_id, message_id, update_id):
    """Save a processed message ID to file"""
    try:
        message_key = f"{chat_id}:{message_id}:{update_id}"
        with open(PROCESSED_MESSAGES_FILE, 'a') as f:
            f.write(f"{message_key}\n")
    except Exception as e:
        print(f"[ERROR] Failed to save processed message: {e}")

def is_message_processed(chat_id, message_id, update_id):
    """Check if a message has already been processed"""
    message_key = f"{chat_id}:{message_id}:{update_id}"
    processed_messages = read_processed_messages()
    return message_key in processed_messages

def validate_env_vars():
    """Validate required environment variables"""
    if not BOT_TOKEN:
        raise ValueError("Missing required environment variable: TELEGRAM_BOT_TOKEN")
    if not CHAT_ID:
        raise ValueError("Missing required environment variable: TELEGRAM_CHAT_ID")
    print(f"[✅] Using Telegram Bot Token: {BOT_TOKEN[:10]}...")
    print(f"[✅] Using Chat ID: {CHAT_ID}")
    if THREAD_ID:
        print(f"[✅] Using Thread ID: {THREAD_ID}")
    else:
        print(f"[ℹ️] No Thread ID specified - monitoring all messages in chat")
    print(f"[✅] Using Review API: {TARGET_API}")

def fetch_telegram_updates(offset=None):
    """Fetch all telegram updates and filter relevant messages"""
    try:
        params = {"timeout": 10}  # Reduced timeout to avoid hanging
        if offset:
            params["offset"] = offset
            
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("ok"):
            print(f"[ERROR] Telegram API returned error: {data}")
            return []
            
        updates = data.get("result", [])
        
        # Filter updates that contain messages from target chat/thread
        relevant_updates = []
        for update in updates:
            message = update.get("message")
            if is_message_from_target(message):
                relevant_updates.append(update)
                
        if relevant_updates:
            print(f"[📥] Found {len(relevant_updates)} relevant message(s)")
        return relevant_updates
    except requests.exceptions.Timeout:
        # Timeouts are normal for long polling
        return []
    except Exception as e:
        print(f"[ERROR] Failed to fetch updates: {e}")
        return []

def check_server_health():
    """Check if the review server is healthy and responding"""
    try:
        health_url = f"{TARGET_API}/health"
        
        print(f"[🩺] Checking server health at: {health_url}")
        response = requests.get(health_url, timeout=10)
        response.raise_for_status()
        
        # Try to parse response as JSON, but accept any successful response
        try:
            result = response.json()
            print(f"[✅] Server is healthy: {result}")
        except:
            print(f"[✅] Server is healthy (status: {response.status_code})")
        
        return True
    except Exception as e:
        print(f"[❌] Server health check failed: {e}")
        return False

def extract_review_info(text):
    pattern = r"^review-(\w+)/(\w+)$"
    match = re.match(pattern, text.strip())
    if match:
        return match.group(1), match.group(2)
    return None, None

def extract_checklist_info(text):
    pattern = r"^checklist-(\w+)/(\w+)$"
    match = re.match(pattern, text.strip())
    if match:
        return match.group(1), match.group(2)
    return None, None

def send_review_request(project_id, merge_id):
    """Send review request to the system API using query parameters"""
    params = {
        "project_id": project_id,
        "mr_id": merge_id,
        "post_review_to_gitlab": True  # Automatically post to GitLab
    }
    try:
        # Increased timeout to 5 minutes (300 seconds) since review requests can take very long
        response = requests.post(f"{TARGET_API}/review", params=params, timeout=300)
        response.raise_for_status()
        result = response.json()
        
        success = result.get("success", False)
        if success:
            print(f"[✅] Review generated successfully for {project_id}/{merge_id}")
            if result.get("posted_to_gitlab"):
                print(f"[✅] Review posted to GitLab: {result.get('merge_request_url', 'N/A')}")
        else:
            print(f"[⚠️] Review failed: {result.get('message', 'Unknown error')}")
            
        return success, result
    except Exception as e:
        print(f"[❌] Failed to POST: {e}")
        return False, {"message": str(e)}
    
def send_checklist_request(project_id, merge_id):
    """Send checklist request to the system API using query parameters"""
    params = {
        "project_id": project_id,
        "mr_id": merge_id,
        "post_review_to_gitlab": True  # Automatically post to GitLab
    }
    try:
        # Increased timeout to 5 minutes (300 seconds) since checklist requests can take very long
        response = requests.post(f"{TARGET_API}/checklist", params=params, timeout=300)
        response.raise_for_status()
        result = response.json()
        
        success = result.get("success", False)
        if success:
            print(f"[✅] Checklist generated successfully for {project_id}/{merge_id}")
            if result.get("posted_to_gitlab"):
                print(f"[✅] Checklist posted to GitLab: {result.get('merge_request_url', 'N/A')}")
        else:
            print(f"[⚠️] Checklist failed: {result.get('message', 'Unknown error')}")
            
        return success, result
    except Exception as e:
        print(f"[❌] Failed to POST: {e}")
        return False, {"message": str(e)}

def is_message_from_target(message):
    """Check if the message is from the target chat and thread"""
    if not message:
        return False
    
    chat_id = message["chat"]["id"]
    
    # Check if message is from the correct chat
    if chat_id != CHAT_ID:
        return False
    
    # If thread ID is specified, check if message is from the correct thread
    if THREAD_ID is not None:
        message_thread_id = message.get("message_thread_id")
        
        # Handle the case where we expect a thread but message has no thread
        if message_thread_id is None:
            print(f"[⚠️] Message is not in thread {THREAD_ID}, skipping")
            return False
            
        if message_thread_id != THREAD_ID:
            return False
    
    return True

def cleanup_old_processed_messages(max_entries=1000):
    """Keep only the most recent processed messages to prevent file from growing indefinitely"""
    try:
        if os.path.exists(PROCESSED_MESSAGES_FILE):
            with open(PROCESSED_MESSAGES_FILE, 'r') as f:
                lines = f.readlines()
            
            if len(lines) > max_entries:
                # Keep only the last max_entries
                recent_lines = lines[-max_entries:]
                with open(PROCESSED_MESSAGES_FILE, 'w') as f:
                    f.writelines(recent_lines)
                print(f"[🧹] Cleaned up processed messages file, kept {len(recent_lines)} recent entries")
    except Exception as e:
        print(f"[ERROR] Failed to cleanup processed messages: {e}")

def test_bot_connection():
    """Test bot connection and get bot info"""
    try:
        test_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
        response = requests.get(test_url, timeout=10)
        response.raise_for_status()
        bot_info = response.json()
        
        if bot_info.get("ok"):
            bot_data = bot_info.get("result", {})
            print(f"[✅] Bot connected successfully: {bot_data.get('first_name', 'Unknown')} (@{bot_data.get('username', 'Unknown')})")
            return True
        else:
            print(f"[❌] Bot API error: {bot_info}")
            return False
    except Exception as e:
        print(f"[❌] Failed to connect to bot: {e}")
        return False

def test_fetch_raw_updates():
    """Test fetching raw updates for debugging"""
    try:
        test_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        params = {"limit": 5}  # Get last 5 updates
        
        print(f"[🔍] Testing raw update fetch...")
        response = requests.get(test_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("ok"):
            updates = data.get("result", [])
            print(f"[✅] Successfully fetched {len(updates)} updates")
            
            for update in updates:
                print(f"[DEBUG] Update ID: {update.get('update_id')}")
                message = update.get("message")
                if message:
                    chat_info = message.get("chat", {})
                    print(f"[DEBUG] Chat: {chat_info.get('id')} ({chat_info.get('title', 'Unknown')})")
                    print(f"[DEBUG] Text: {message.get('text', 'No text')}")
                    print(f"[DEBUG] Thread ID: {message.get('message_thread_id', 'None')}")
                else:
                    print(f"[DEBUG] No message in update")
                print("---")
            return True
        else:
            print(f"[❌] API Error: {data}")
            return False
    except Exception as e:
        print(f"[❌] Failed to test raw updates: {e}")
        return False

def test_message_filtering():
    """Test the message filtering with current updates"""
    try:
        test_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        params = {"limit": 5}
        
        response = requests.get(test_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("ok"):
            updates = data.get("result", [])
            print(f"[🧪] Testing filtering on {len(updates)} updates")
            
            for update in updates:
                message = update.get("message")
                if message:
                    print(f"\n[🔍] Testing update {update.get('update_id')}:")
                    result = is_message_from_target(message)
                    print(f"[📊] Filter result: {result}")
                    
                    if result:
                        text = message.get("text", "")
                        project_id, merge_id = extract_review_info(text)
                        if project_id and merge_id:
                            print(f"[✅] Review Would process: {project_id}/{merge_id}")
                        else:
                            print(f"[❌] Review Invalid format: {text}")
                        
                        project_id, merge_id = extract_checklist_info(text)
                        if project_id and merge_id:
                            print(f"[✅] Checklist Would process: {project_id}/{merge_id}")
                        else:
                            print(f"[❌] Checklist Invalid format: {text}")
        
    except Exception as e:
        print(f"[❌] Failed to test filtering: {e}")

def send_telegram_message(chat_id, text, thread_id=None):
    """Send a message to Telegram chat with fallback formatting"""
    try:
        send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"  # Allow Markdown formatting
        }
        
        # Add thread ID if specified and message is in a thread
        if thread_id:
            payload["message_thread_id"] = thread_id
            
        response = requests.post(send_url, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get("ok"):
            print(f"[📤] Message sent successfully to chat {chat_id}")
            return True
        else:
            print(f"[❌] Failed to send message: {result}")
            # If markdown parsing failed, try sending without markdown
            if "can't parse" in str(result).lower() or "bad request" in str(result).lower():
                print(f"[🔄] Retrying without markdown formatting...")
                payload["parse_mode"] = None
                # Remove markdown formatting from text
                clean_text = text.replace('*', '').replace('_', '').replace('`', '').replace('```', '')
                payload["text"] = clean_text
                
                retry_response = requests.post(send_url, json=payload, timeout=10)
                retry_result = retry_response.json()
                
                if retry_result.get("ok"):
                    print(f"[📤] Message sent successfully without markdown formatting")
                    return True
                else:
                    print(f"[❌] Failed to send message even without formatting: {retry_result}")
            return False
    except Exception as e:
        print(f"[❌] Error sending message: {e}")
        return False

def format_markdown_for_telegram(content, max_length=3500):
    """
    Convert markdown content to proper Telegram format.
    Telegram supports basic markdown but has specific requirements.
    """
    if not content:
        return ""
    
    # Telegram message limit is 4096 characters, reserve space for headers/footers
    if len(content) > max_length:
        content = content[:max_length] + "..."
    
    import re
    
    # Convert **bold** to *bold* (Telegram uses single asterisks)
    content = re.sub(r'\*\*(.*?)\*\*', r'*\1*', content)
    
    # Convert __bold__ to *bold*
    content = re.sub(r'__(.*?)__', r'*\1*', content)
    
    # Handle checklist items - convert [ ] and [x] to emojis for better visibility
    content = re.sub(r'- \[ \]', '☐', content)  # Empty checkbox
    content = re.sub(r'- \[x\]', '✅', content)  # Checked checkbox
    content = re.sub(r'- \[X\]', '✅', content)  # Checked checkbox (uppercase)
    
    # Handle code blocks properly - for short code snippets, use inline code
    # For longer blocks, keep them as code blocks but ensure proper formatting
    def replace_code_blocks(match):
        code_content = match.group(2) if match.group(2) else match.group(1)
        if len(code_content.strip()) < 100:  # Short code snippets as inline
            return f"`{code_content.strip()}`"
        else:  # Long code blocks
            return f"```\n{code_content.strip()}\n```"
    
    # Handle both ``` and single ` code formats
    content = re.sub(r'```(\w+)?\n(.*?)```', replace_code_blocks, content, flags=re.DOTALL)
    
    # Clean up formatting issues
    content = content.replace('\\n', '\n')  # Fix escaped newlines
    content = content.replace('\\t', '    ')  # Convert tabs to spaces
    
    # Handle bullet points - ensure they're properly formatted
    content = re.sub(r'^(\s*)- ', r'\1• ', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)\* ', r'\1• ', content, flags=re.MULTILINE)
    
    # Clean up excessive whitespace but preserve structure
    lines = content.split('\n')
    cleaned_lines = []
    prev_empty = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if not prev_empty:  # Allow one empty line
                cleaned_lines.append('')
                prev_empty = True
        else:
            cleaned_lines.append(line.rstrip())  # Remove trailing spaces
            prev_empty = False
    
    # Join and ensure we don't end with empty lines
    result = '\n'.join(cleaned_lines).rstrip()
    
    return result

def send_review_result_message(chat_id, project_id, merge_id, success, result_data, thread_id=None):
    """Send result message after review API processing"""
    if success:
        message = f"✅ *Review Completed*\n"
        message += f"📁 Project: `{project_id}`\n"
        message += f"🔀 MR: `{merge_id}`\n\n"

        # Include review content from the API response
        review_content = result_data.get("review_content")
        checklist_content = result_data.get("checklist_content")
        
        if review_content:
            formatted_content = format_markdown_for_telegram(review_content)
            message += f"📋 *Review Content:*\n"
            message += f"{formatted_content}\n"
        elif checklist_content:
            formatted_content = format_markdown_for_telegram(checklist_content)
            message += f"📋 *Review Content:*\n"
            message += f"{formatted_content}\n"
        elif result_data.get("review_summary"):
            # Fallback to summary if review_content is not available
            summary = format_markdown_for_telegram(result_data.get('review_summary'), 500)
            message += f"📋 *Summary:*\n{summary}\n"
        
        # Add confirmation that message was posted to GitLab
        if result_data.get("posted_to_gitlab"):
            gitlab_url = result_data.get('merge_request_url', '')
            if gitlab_url:
                message += f"\n🔗 [View on GitLab]({gitlab_url})"
            else:
                message += f"\n📤 Posted to GitLab"
    else:
        message = f"❌ *Review Failed*\n"
        message += f"📁 Project: `{project_id}`\n" 
        message += f"🔀 MR: `{merge_id}`\n"
        message += f"💥 Error: {result_data.get('message', 'Unknown error')}"
    
    return send_telegram_message(chat_id, message, thread_id)

def send_checklist_result_message(chat_id, project_id, merge_id, success, result_data, thread_id=None):
    """Send result message after checklist API processing"""
    if success:
        message = f"✅ *Checklist Completed*\n"
        message += f"📁 Project: `{project_id}`\n"
        message += f"🔀 MR: `{merge_id}`\n\n"

        # Include checklist content from the API response
        checklist_content = result_data.get("checklist_content")
        review_content = result_data.get("review_content")
        
        if checklist_content:
            formatted_content = format_markdown_for_telegram(checklist_content)
            message += f"📝 *Checklist Content:*\n"
            message += f"{formatted_content}\n"
        elif review_content:
            formatted_content = format_markdown_for_telegram(review_content)
            message += f"📝 *Checklist Content:*\n"
            message += f"{formatted_content}\n"
        elif result_data.get("checklist_summary"):
            # Fallback to summary if checklist_content is not available
            summary = format_markdown_for_telegram(result_data.get('checklist_summary'), 500)
            message += f"📝 *Summary:*\n{summary}\n"
        
        # Add confirmation that message was posted to GitLab
        if result_data.get("posted_to_gitlab"):
            gitlab_url = result_data.get('merge_request_url', '')
            if gitlab_url:
                message += f"\n🔗 [View on GitLab]({gitlab_url})"
            else:
                message += f"\n📤 Posted to GitLab"
    else:
        message = f"❌ *Checklist Failed*\n"
        message += f"📁 Project: `{project_id}`\n" 
        message += f"🔀 MR: `{merge_id}`\n"
        message += f"💥 Error: {result_data.get('message', 'Unknown error')}"
    
    return send_telegram_message(chat_id, message, thread_id)

def send_acknowledgment(chat_id, project_id, merge_id, thread_id=None):
    """Send acknowledgment message to user"""
    message = f"🤖 *Request Accepted*, I am working on it..."
    
    return send_telegram_message(chat_id, message, thread_id)

# Legacy function for backwards compatibility - now redirects to review function
def send_result_message(chat_id, project_id, merge_id, success, result_data, thread_id=None):
    """Legacy function - redirects to send_review_result_message for backwards compatibility"""
    return send_review_result_message(chat_id, project_id, merge_id, success, result_data, thread_id)

def main():
    # Validate environment variables
    validate_env_vars()
    
    # Test bot connection
    if not test_bot_connection():
        print("[❌] Bot connection failed. Exiting...")
        return
    
    # Test raw update fetching
    print("[🧪] Testing raw update fetching...")
    test_fetch_raw_updates()
    
    # Clean up old processed messages periodically
    cleanup_old_processed_messages()
    
    # Read processed messages from file
    processed_messages = read_processed_messages()
    print(f"[ℹ️] Loaded {len(processed_messages)} previously processed messages")
    
    print("[🤖 Bot is running...]")
    last_offset = None
    
    while True:
        updates = fetch_telegram_updates(offset=last_offset)
        
        if updates:
            for update in updates:
                current_update_id = update["update_id"]
                message = update.get("message")
                
                if message:
                    chat_id = message["chat"]["id"]
                    message_id = message["message_id"]
                    
                    # Check if we've already processed this message
                    if is_message_processed(chat_id, message_id, current_update_id):
                        print(f"[⏭️] Skipping already processed message {message_id}")
                        continue
                    
                    text = message.get("text", "")
                    project_id, merge_id = extract_review_info(text)
                    
                    if project_id and merge_id:
                        print(f"[📝] Processing review request: {project_id}/{merge_id}")
                        
                        # Get thread ID from the original message for replies
                        message_thread_id = message.get("message_thread_id")
                        
                        # 1. Check server health first before proceeding
                        print(f"[🩺] Checking server health before processing...")
                        if not check_server_health():
                            # Server is not healthy, send error message and skip processing
                            error_message = f"❌ *Server Unavailable*\n\n" \
                                          f"📝 Project: `{project_id}`, MR: `{merge_id}`\n" \
                                          f"💥 The review server is currently unavailable. Please try again later."
                            send_telegram_message(chat_id, error_message, message_thread_id)
                            save_processed_message(chat_id, message_id, current_update_id)
                            continue
                        
                        # 2. Send acknowledgment message after health check passes
                        print(f"[📤] Sending acknowledgment message...")
                        ack_sent = send_acknowledgment(chat_id, project_id, merge_id, message_thread_id)
                        
                        if THREAD_ID:
                            print(f"[🧵] Message from thread: {THREAD_ID}")
                        
                        # 3. Process the review request
                        success, result_data = send_review_request(project_id, merge_id)
                        
                        # 4. Send result message
                        print(f"[📤] Sending result message...")
                        result_sent = send_review_result_message(chat_id, project_id, merge_id, success, result_data, message_thread_id)
                        
                        # Mark message as processed
                        save_processed_message(chat_id, message_id, current_update_id)
                        print(f"[✅] Message {message_id} processed and saved")
                    else:
                        print(f"[❌] Invalid format. Expected: review-<project_id>/<merge_id>. Got: {text}")
                        # Still mark as processed to avoid reprocessing
                        save_processed_message(chat_id, message_id, current_update_id)

                    project_id, merge_id = extract_checklist_info(text)
                    if project_id and merge_id:
                        print(f"[📝] Processing checklist request: {project_id}/{merge_id}")
                        
                        # Get thread ID from the original message for replies
                        message_thread_id = message.get("message_thread_id")
                        
                        # 1. Check server health first before proceeding
                        print(f"[🩺] Checking server health before processing...")
                        if not check_server_health():
                            # Server is not healthy, send error message and skip processing
                            error_message = f"❌ *Server Unavailable*\n\n" \
                                          f"📝 Project: `{project_id}`, Checklist: `{merge_id}`\n" \
                                          f"💥 The checklist server is currently unavailable. Please try again later."
                            send_telegram_message(chat_id, error_message, message_thread_id)
                            save_processed_message(chat_id, message_id, current_update_id)
                            continue
                        
                        # 2. Send acknowledgment message after health check passes
                        print(f"[📤] Sending acknowledgment message...")
                        ack_sent = send_acknowledgment(chat_id, project_id, merge_id, message_thread_id)
                        
                        if THREAD_ID:
                            print(f"[🧵] Message from thread: {THREAD_ID}")
                        
                        # 3. Process the checklist request
                        success, result_data = send_checklist_request(project_id, merge_id)
                        
                        # 4. Send result message
                        print(f"[📤] Sending result message...")
                        result_sent = send_checklist_result_message(chat_id, project_id, merge_id, success, result_data, message_thread_id)
                        
                        # Mark message as processed
                        save_processed_message(chat_id, message_id, current_update_id)
                        print(f"[✅] Message {message_id} processed and saved")
                    else:
                        print(f"[❌] Invalid format. Expected: checklist-<project_id>/<merge_id>. Got: {text}")
                        # Still mark as processed to avoid reprocessing
                        save_processed_message(chat_id, message_id, current_update_id)
                    
                
                # Update offset to get newer messages next time
                last_offset = current_update_id + 1
        
        time.sleep(5)  # Poll every 5 seconds

def test_send_message():
    """Test sending a message to Telegram"""
    try:
        test_message = "🧪 *Test Message*\n\nThis is a test message from the bot to verify messaging functionality."
        result = send_telegram_message(CHAT_ID, test_message, THREAD_ID)
        if result:
            print("[✅] Test message sent successfully")
        else:
            print("[❌] Failed to send test message")
        return result
    except Exception as e:
        print(f"[❌] Error testing message sending: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        # Debug mode - just test connectivity and fetch updates once
        print("[🐛] Debug mode - testing connectivity...")
        validate_env_vars()
        if test_bot_connection():
            test_fetch_raw_updates()
            print("\n[🧪] Testing message filtering...")
            test_message_filtering()
            print("\n[🧪] Testing server health...")
            check_server_health()
            print("\n[🧪] Testing message sending...")
            test_send_message()
        print("[🐛] Debug mode complete")
    else:
        # Normal mode - run the bot
        main()
