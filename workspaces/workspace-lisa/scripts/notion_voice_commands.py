#!/usr/bin/env python3
"""
Notion Voice Commands - Telegram voice message handler for Notion task updates.

Usage:
    python3 notion_voice_commands.py --test [audio_file]   # Test with sample audio
    python3 notion_voice_commands.py --server              # Start Telegram polling server
    python3 notion_voice_commands.py --transcribe [file]  # Just transcribe audio

Created: 2026-04-10 (Mission #8 Phase 3c)
"""

import os
import sys
import json
import re
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, Dict, Any

# Telegram
import requests as http

# Notion
sys.path.insert(0, str(Path(__file__).parent))
from notion_api import (
    DB_IDS, query_db, create_page, api,
    extract_title, make_title_prop, make_rich_text_prop, make_select_prop
)

# Config paths
NOTION_TOKEN = open(os.path.expanduser("~/.config/notion/api_key")).read().strip()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "REDACTED_SET_FROM_ENV")
TELEGRAM_API_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# User mapping (Telegram user_id -> Notion team member)
USER_MAPPING = {
    # Default: first team member in DB
    "default": "Wilson"
}


def transcribe_audio_openai(audio_path: str) -> str:
    """Transcribe audio using OpenAI Whisper API."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    
    # Determine file extension and content type
    ext = Path(audio_path).suffix.lower()
    content_type_map = {
        ".ogg": "audio/ogg",
        ".oga": "audio/ogg",
        ".mp3": "audio/mpeg",
        ".m4a": "audio/mp4",
        ".wav": "audio/wav",
        ".webm": "audio/webm",
    }
    content_type = content_type_map.get(ext, "audio/ogg")
    
    with open(audio_path, "rb") as f:
        files = {"file": (Path(audio_path).name, f, content_type)}
        data = {"model": "whisper-1"}
        response = http.post(url, headers=headers, files=files, data=data)
    
    if response.status_code >= 400:
        raise Exception(f"OpenAI API error {response.status_code}: {response.text[:300]}")
    
    result = response.json()
    return result.get("text", "")


def transcribe_audio_local(audio_path: str) -> str:
    """Fallback: transcribe using local whisper CLI."""
    try:
        result = subprocess.run(
            ["whisper", audio_path, "--model", "base", "--output_format", "txt", "--output_dir", "-"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            raise Exception(f"Whisper failed: {result.stderr[:200]}")
        # Whisper outputs to file, read it
        txt_file = Path(audio_path).with_suffix(".txt")
        if txt_file.exists():
            text = txt_file.read_text()
            txt_file.unlink()
            return text.strip()
        return result.stdout.strip()
    except FileNotFoundError:
        raise Exception("Local whisper not installed. Install with: pip install openai-whisper")


def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio using OpenAI API or local Whisper."""
    if OPENAI_API_KEY:
        try:
            return transcribe_audio_openai(audio_path)
        except Exception as e:
            print(f"Warning: OpenAI transcription failed ({e}), trying local...")
    return transcribe_audio_local(audio_path)


def convert_ogg_to_wav(ogg_path: str) -> str:
    """Convert OGG/OGA to WAV using ffmpeg (needed for local whisper)."""
    wav_path = ogg_path.rsplit(".", 1)[0] + ".wav"
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", ogg_path, "-ar", "16000", "-ac", "1", wav_path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise Exception(f"FFmpeg conversion failed: {result.stderr[:200]}")
    return wav_path


def parse_command(text: str) -> Dict[str, Any]:
    """
    Parse transcribed text into structured command.
    
    Patterns:
    - "Working on [task]" / "I'm working on [task]" -> status: In Progress
    - "Completed [task]" / "I finished [task]" / "Done with [task]" -> status: Done
    - "Started [task]" / "Create new task [task]" / "New task [task]" -> create task
    - "Block [task]" / "Blocked on [task]" -> status: Blocked
    - "Review [task]" / "Ready for review [task]" -> status: Review
    
    Returns: {action, task_name, status, description}
    """
    text = text.strip()
    text_lower = text.lower()
    
    # Status update patterns
    status_patterns = [
        # In Progress
        (r"(?:i'?m\s+)?working\s+on\s+(.+)", "In Progress"),
        (r"(?:i'?m\s+)?working\s+on\s+the\s+(.+)", "In Progress"),
        (r"started\s+working\s+on\s+(.+)", "In Progress"),
        (r"began\s+(.+)", "In Progress"),
        
        # Done
        (r"(?:i\s+)?(?:finished|completed|done\s+(?:with\s+)?)\s*(?:the\s+)?(.+)", "Done"),
        (r"completed\s+(?:the\s+)?(.+)", "Done"),
        (r"(.+?)\s+(?:is\s+)?(?:done|completed|finished)", "Done"),
        
        # Review
        (r"(.+?)\s+(?:is\s+)?ready\s+for\s+review", "Review"),
        (r"(?:i\s+)?(?:finished|completed)\s+(?:the\s+)?(.+?)\s+for\s+review", "Review"),
        (r"review\s+(?:the\s+)?(.+)", "Review"),
        
        # Blocked
        (r"(.+?)\s+(?:is\s+)?blocked", "Blocked"),
        (r"blocked\s+on\s+(.+)", "Blocked"),
        
        # Started (could be create or In Progress)
        (r"started\s+(?:on\s+)?(?:the\s+)?(.+)", "In Progress"),
    ]
    
    # Create task patterns
    create_patterns = [
        r"create\s+(?:a\s+)?new\s+task\s+(?:for\s+)?(.+)",
        r"new\s+task\s+(?:(?:for|called)\s+)?(.+)",
        r"add\s+(?:a\s+)?task\s+(?:for\s+)?(.+)",
        r"need\s+(?:to\s+)?(?:work\s+on\s+)?(.+)",
    ]
    
    # Check for create patterns first
    for pattern in create_patterns:
        match = re.search(pattern, text_lower)
        if match:
            task_name = match.group(1).strip()
            # Capitalize first letter
            task_name = task_name[0].upper() + task_name[1:] if task_name else task_name
            return {
                "action": "create",
                "task_name": task_name,
                "status": "To Do",
                "description": f"Created via voice command: {text}"
            }
    
    # Check status update patterns
    for pattern, status in status_patterns:
        match = re.search(pattern, text_lower)
        if match:
            task_name = match.group(1).strip()
            # Capitalize first letter
            task_name = task_name[0].upper() + task_name[1:] if task_name else task_name
            # Clean up common endings
            task_name = re.sub(r'\s+(task|project|item)\s*$', '', task_name, flags=re.I)
            return {
                "action": "update_status",
                "task_name": task_name,
                "status": status,
                "description": f"Updated via voice command: {text}"
            }
    
    # Default: treat as new task creation
    return {
        "action": "create",
        "task_name": text[0].upper() + text[1:] if text else "Untitled Task",
        "status": "To Do",
        "description": f"Created via voice command: {text}"
    }


def find_task_by_name(task_name: str, fuzzy: bool = True) -> Optional[Dict]:
    """Find a task by name (exact or fuzzy match)."""
    # Query tasks
    result = query_db(DB_IDS["tasks"])
    pages = result.get("results", [])
    
    task_name_lower = task_name.lower()
    
    # Exact match first
    for page in pages:
        title = extract_title(page, "Name").lower()
        if title == task_name_lower:
            return page
    
    # Fuzzy match (contains)
    if fuzzy:
        for page in pages:
            title = extract_title(page, "Name").lower()
            if task_name_lower in title or title in task_name_lower:
                return page
        
        # Word-level fuzzy match
        task_words = set(task_name_lower.split())
        for page in pages:
            title = extract_title(page, "Name").lower()
            title_words = set(title.split())
            overlap = len(task_words & title_words)
            if overlap >= min(2, len(task_words)):
                return page
    
    return None


def update_task_status(task_id: str, new_status: str) -> Dict:
    """Update a task's status in Notion."""
    properties = {
        "Status": make_select_prop(new_status)
    }
    return api("patch", f"/pages/{task_id}", {"properties": properties})


def create_task(task_name: str, status: str = "To Do", description: str = "") -> Dict:
    """Create a new task in Notion."""
    properties = {
        "Name": make_title_prop(task_name),
        "Status": make_select_prop(status),
    }
    if description:
        properties["Description"] = make_rich_text_prop(description)
    
    return create_page(DB_IDS["tasks"], properties)


def process_voice_command(text: str, user_id: str = "default") -> Dict[str, Any]:
    """
    Process transcribed text and execute Notion update.
    
    Returns: {success, action, task_name, status, message, task_id?}
    """
    command = parse_command(text)
    
    if command["action"] == "create":
        # Create new task
        try:
            result = create_task(
                task_name=command["task_name"],
                status=command["status"],
                description=command.get("description", "")
            )
            task_id = result.get("id")
            return {
                "success": True,
                "action": "create",
                "task_name": command["task_name"],
                "status": command["status"],
                "message": f"✅ Created new task: '{command['task_name']}' with status '{command['status']}'",
                "task_id": task_id
            }
        except Exception as e:
            return {
                "success": False,
                "action": "create",
                "task_name": command["task_name"],
                "message": f"❌ Failed to create task: {str(e)}"
            }
    
    elif command["action"] == "update_status":
        # Find and update existing task
        task = find_task_by_name(command["task_name"])
        
        if not task:
            # Task not found - offer to create
            return {
                "success": False,
                "action": "update_status",
                "task_name": command["task_name"],
                "status": command["status"],
                "message": f"❓ Task '{command['task_name']}' not found. Would you like to create it?",
                "suggestion": "create"
            }
        
        # Update status
        task_id = task.get("id")
        current_status = task.get("properties", {}).get("Status", {}).get("select", {}).get("name", "")
        
        try:
            update_task_status(task_id, command["status"])
            return {
                "success": True,
                "action": "update_status",
                "task_name": extract_title(task, "Name"),
                "status": command["status"],
                "previous_status": current_status,
                "message": f"✅ Updated '{extract_title(task, 'Name')}' from '{current_status}' to '{command['status']}'",
                "task_id": task_id
            }
        except Exception as e:
            return {
                "success": False,
                "action": "update_status",
                "task_name": command["task_name"],
                "message": f"❌ Failed to update task: {str(e)}"
            }
    
    return {
        "success": False,
        "message": f"❓ Could not understand command: {text}"
    }


def process_voice_message(audio_file_path: str, user_id: str = "default") -> Dict[str, Any]:
    """
    Main entry point: process a voice message file and update Notion.
    
    Args:
        audio_file_path: Path to audio file (OGG, MP3, M4A, WAV)
        user_id: Telegram user ID (for future multi-user support)
    
    Returns:
        {success, transcription, action, task_name, status, message}
    """
    # Step 1: Transcribe audio
    print(f"🎤 Transcribing: {audio_file_path}")
    
    audio_path = audio_file_path
    temp_wav = None
    
    # Convert OGG to WAV if using local whisper
    ext = Path(audio_file_path).suffix.lower()
    if ext in (".ogg", ".oga") and not OPENAI_API_KEY:
        print("Converting OGG to WAV for local transcription...")
        audio_path = convert_ogg_to_wav(audio_file_path)
        temp_wav = audio_path
    
    try:
        transcription = transcribe_audio(audio_path)
        print(f"📝 Transcription: {transcription}")
        
        if not transcription.strip():
            return {
                "success": False,
                "transcription": "",
                "message": "❌ Could not transcribe audio (empty result)"
            }
        
        # Step 2: Process command
        result = process_voice_command(transcription, user_id)
        result["transcription"] = transcription
        return result
        
    finally:
        # Cleanup temp file
        if temp_wav and Path(temp_wav).exists():
            Path(temp_wav).unlink()


# === Telegram Bot Integration ===

def download_telegram_file(file_id: str, file_type: str = "voice") -> str:
    """Download a file from Telegram and return local path."""
    # Get file path
    r = http.get(f"{TELEGRAM_API_BASE}/getFile", params={"file_id": file_id})
    r.raise_for_status()
    file_path = r.json()["result"]["file_path"]
    
    # Download file
    file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
    r = http.get(file_url)
    r.raise_for_status()
    
    # Save to temp file
    ext = Path(file_path).suffix or ".ogg"
    temp_file = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
    temp_file.write(r.content)
    temp_file.close()
    
    return temp_file.name


def send_telegram_message(chat_id: str, text: str, reply_to: Optional[str] = None) -> Dict:
    """Send a message to Telegram chat."""
    params = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_to:
        params["reply_to_message_id"] = reply_to
    
    r = http.post(f"{TELEGRAM_API_BASE}/sendMessage", params=params)
    r.raise_for_status()
    return r.json()


def handle_telegram_update(update: Dict) -> None:
    """Process a single Telegram update (message)."""
    message = update.get("message", {})
    chat_id = str(message.get("chat", {}).get("id", ""))
    user_id = str(message.get("from", {}).get("id", ""))
    message_id = str(message.get("message_id", ""))
    
    # Handle voice message
    if "voice" in message:
        voice = message["voice"]
        file_id = voice["file_id"]
        
        # Send acknowledgment
        send_telegram_message(chat_id, "🎤 Processing voice message...", reply_to=message_id)
        
        try:
            # Download and process
            audio_path = download_telegram_file(file_id)
            result = process_voice_message(audio_path, user_id)
            
            # Cleanup
            Path(audio_path).unlink(missing_ok=True)
            
            # Send result
            response = f"📝 *Transcription:* {result.get('transcription', 'N/A')}\n\n{result['message']}"
            send_telegram_message(chat_id, response, reply_to=message_id)
            
        except Exception as e:
            send_telegram_message(chat_id, f"❌ Error processing voice: {str(e)}", reply_to=message_id)
    
    # Handle text message (for testing)
    elif "text" in message:
        text = message.get("text", "")
        
        # Skip commands
        if text.startswith("/"):
            if text == "/start":
                send_telegram_message(chat_id, "🎤 Send me a voice message to update your Notion tasks!")
            return
        
        # Process as text command
        result = process_voice_command(text, user_id)
        response = f"{result['message']}"
        send_telegram_message(chat_id, response, reply_to=message_id)


def run_telegram_server(poll_interval: int = 1) -> None:
    """Run Telegram polling server."""
    print("🤖 Starting Telegram voice command server...")
    print(f"📡 Using bot token: {TELEGRAM_BOT_TOKEN[:10]}...")
    print("💬 Send voice messages to your bot to update Notion tasks!")
    print("Press Ctrl+C to stop.\n")
    
    last_update_id = 0
    
    while True:
        try:
            # Get updates
            r = http.get(
                f"{TELEGRAM_API_BASE}/getUpdates",
                params={"offset": last_update_id + 1, "timeout": poll_interval}
            )
            r.raise_for_status()
            updates = r.json().get("result", [])
            
            for update in updates:
                last_update_id = update.get("update_id", 0)
                handle_telegram_update(update)
            
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")
            import time
            time.sleep(5)


# === CLI Interface ===

def create_test_audio(text: str = "I'm working on the marketing campaign") -> str:
    """Create a simple test audio file using TTS (if available) or return fake path."""
    # For testing without actual audio, we'll simulate transcription
    return "__SIMULATED__"


def run_test(audio_file: Optional[str] = None) -> None:
    """Run test with sample or provided audio file."""
    print("🧪 Running voice command test...\n")
    
    if audio_file and Path(audio_file).exists():
        # Test with real audio
        result = process_voice_message(audio_file)
    else:
        # Simulate transcription for testing
        test_commands = [
            ("I'm working on the marketing campaign", "In Progress"),
            ("I finished the content calendar", "Done"),
            ("Create a new task for website redesign", "To Do"),
            ("The database migration is ready for review", "Review"),
            ("Blocked on API integration", "Blocked"),
        ]
        
        print("📋 Testing command parsing:\n")
        
        for text, expected_status in test_commands:
            print(f"Input: '{text}'")
            command = parse_command(text)
            print(f"  → Action: {command['action']}")
            print(f"  → Task: {command['task_name']}")
            print(f"  → Status: {command['status']}")
            print(f"  → Expected: {expected_status}")
            print(f"  ✓ Match: {command['status'] == expected_status}")
            print()
        
        # Test actual Notion update with one command
        print("\n📝 Testing Notion integration with first command...\n")
        result = process_voice_command("I'm working on the marketing campaign")
        print(f"Result: {json.dumps(result, indent=2)}")
        return
    
    print(f"\n📊 Result:\n{json.dumps(result, indent=2)}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Notion Voice Commands")
    parser.add_argument("--test", nargs="?", const=None, help="Run test mode")
    parser.add_argument("--server", action="store_true", help="Start Telegram polling server")
    parser.add_argument("--transcribe", metavar="FILE", help="Just transcribe audio file")
    parser.add_argument("--command", metavar="TEXT", help="Test text command parsing")
    
    args = parser.parse_args()
    
    if args.server:
        run_telegram_server()
    elif args.transcribe:
        transcription = transcribe_audio(args.transcribe)
        print(f"Transcription: {transcription}")
    elif args.command:
        result = process_voice_command(args.command)
        print(json.dumps(result, indent=2))
    elif args.test is not None:
        run_test(args.test)
    else:
        # Default: run test
        run_test()


if __name__ == "__main__":
    main()