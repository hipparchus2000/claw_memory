#!/usr/bin/env python3
"""
Robust Slack Messenger for OpenClaw
Handles message chunking, file uploads, and reliable delivery.

Usage:
  python3 robust_slack_messenger.py send "message" --channel "#general"
  python3 robust_slack_messenger.py file "/path/to/file.pdf" --channel "#general"
  python3 robust_slack_messenger.py test
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from typing import Optional, List, Dict, Any
import argparse

# Configuration
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL", "#general")
MAX_MESSAGE_LENGTH = 3500  # Under Slack's 4000 limit for safety
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

class RobustSlackMessenger:
    """Robust Slack messaging with chunking and file upload support"""
    
    def __init__(self, token: str = None, default_channel: str = None):
        """Initialize with Slack token and default channel"""
        self.token = token or SLACK_BOT_TOKEN
        self.default_channel = default_channel or SLACK_CHANNEL
        
        if not self.token:
            raise ValueError("Slack bot token required. Set SLACK_BOT_TOKEN environment variable.")
    
    def _split_message(self, text: str, max_length: int = MAX_MESSAGE_LENGTH) -> List[str]:
        """Split long messages into chunks that fit Slack's limits"""
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        lines = text.split('\n')
        current_chunk = ""
        
        for line in lines:
            # If adding this line would exceed limit, start new chunk
            if len(current_chunk) + len(line) + 1 > max_length:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""
            
            # Add line to current chunk
            if current_chunk:
                current_chunk += "\n" + line
            else:
                current_chunk = line
        
        # Add final chunk
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def send_message(self, 
                    text: str, 
                    channel: str = None,
                    thread_ts: str = None,
                    as_user: bool = True,
                    retry: bool = True) -> Dict[str, Any]:
        """
        Send message to Slack with automatic chunking and retry logic
        
        Args:
            text: Message text (will be chunked if too long)
            channel: Slack channel (defaults to configured channel)
            thread_ts: Thread timestamp to reply in thread
            as_user: Send as user (True) or as bot (False)
            retry: Enable retry on failure
        
        Returns:
            Dictionary with response data
        """
        channel = channel or self.default_channel
        
        # Split message if too long
        chunks = self._split_message(text)
        
        responses = []
        last_thread_ts = thread_ts
        
        for i, chunk in enumerate(chunks):
            # Add chunk indicator for multi-part messages
            if len(chunks) > 1:
                chunk = f"({i+1}/{len(chunks)})\n{chunk}"
            
            payload = {
                "channel": channel,
                "text": chunk,
                "as_user": as_user
            }
            
            if last_thread_ts:
                payload["thread_ts"] = last_thread_ts
            
            # Send with retry logic
            response = self._send_slack_api("chat.postMessage", payload, retry)
            
            if response and response.get("ok"):
                responses.append(response)
                # Use first message's timestamp for threading subsequent chunks
                if i == 0 and "ts" in response:
                    last_thread_ts = response["ts"]
            else:
                print(f"❌ Failed to send chunk {i+1}/{len(chunks)}")
        
        # Return first response (contains thread timestamp)
        return responses[0] if responses else {}
    
    def upload_file(self, 
                   file_path: str,
                   channel: str = None,
                   thread_ts: str = None,
                   title: str = None,
                   initial_comment: str = None,
                   retry: bool = True) -> Dict[str, Any]:
        """
        Upload file to Slack with retry logic
        
        Args:
            file_path: Path to file to upload
            channel: Slack channel (defaults to configured channel)
            thread_ts: Thread timestamp to reply in thread
            title: File title (defaults to filename)
            initial_comment: Comment to include with file
            retry: Enable retry on failure
        
        Returns:
            Dictionary with response data
        """
        channel = channel or self.default_channel
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        filename = os.path.basename(file_path)
        title = title or filename
        
        # Read file
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Prepare payload
        files = {
            'file': (filename, file_data)
        }
        
        data = {
            'channels': channel,
            'title': title,
            'filename': filename
        }
        
        if initial_comment:
            data['initial_comment'] = initial_comment
        
        if thread_ts:
            data['thread_ts'] = thread_ts
        
        # Upload with retry logic
        return self._send_slack_api_files("files.upload", data, files, retry)
    
    def send_message_with_files(self,
                               text: str,
                               file_paths: List[str],
                               channel: str = None,
                               thread_ts: str = None) -> Dict[str, Any]:
        """
        Send message with multiple files attached
        
        Args:
            text: Message text
            file_paths: List of file paths to upload
            channel: Slack channel
            thread_ts: Thread timestamp
        
        Returns:
            Dictionary with response data
        """
        # First send the message
        response = self.send_message(text, channel, thread_ts)
        
        if not response.get("ok"):
            return response
        
        # Get thread timestamp from message response
        thread_ts = response.get("ts", thread_ts)
        
        # Upload each file in the thread
        for file_path in file_paths:
            try:
                self.upload_file(file_path, channel, thread_ts)
            except Exception as e:
                print(f"❌ Failed to upload {file_path}: {e}")
        
        return response
    
    def _send_slack_api(self, 
                       method: str, 
                       payload: Dict[str, Any],
                       retry: bool = True) -> Dict[str, Any]:
        """Send request to Slack API with retry logic"""
        url = f"https://slack.com/api/{method}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        for attempt in range(MAX_RETRIES if retry else 1):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                if data.get("ok"):
                    return data
                else:
                    error = data.get("error", "Unknown error")
                    print(f"❌ Slack API error ({attempt+1}/{MAX_RETRIES}): {error}")
                    
                    # Don't retry on certain errors
                    if error in ["not_authed", "invalid_auth", "account_inactive"]:
                        break
            
            except requests.exceptions.RequestException as e:
                print(f"❌ Request failed ({attempt+1}/{MAX_RETRIES}): {e}")
            
            # Wait before retry
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))  # Exponential backoff
        
        return {"ok": False, "error": "Max retries exceeded"}
    
    def _send_slack_api_files(self,
                             method: str,
                             data: Dict[str, Any],
                             files: Dict[str, Any],
                             retry: bool = True) -> Dict[str, Any]:
        """Send file upload request to Slack API with retry logic"""
        url = f"https://slack.com/api/{method}"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        
        for attempt in range(MAX_RETRIES if retry else 1):
            try:
                response = requests.post(url, headers=headers, data=data, files=files, timeout=60)
                response.raise_for_status()
                data = response.json()
                
                if data.get("ok"):
                    return data
                else:
                    error = data.get("error", "Unknown error")
                    print(f"❌ Slack API file upload error ({attempt+1}/{MAX_RETRIES}): {error}")
            
            except requests.exceptions.RequestException as e:
                print(f"❌ File upload request failed ({attempt+1}/{MAX_RETRIES}): {e}")
            
            # Wait before retry
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
        
        return {"ok": False, "error": "Max retries exceeded"}
    
    def test_connection(self) -> bool:
        """Test Slack connection and token validity"""
        try:
            response = self._send_slack_api("auth.test", {}, retry=False)
            return response.get("ok", False)
        except:
            return False

# Convenience functions
def send_message(text: str, channel: str = None, thread_ts: str = None) -> Dict[str, Any]:
    """Convenience function for sending messages"""
    messenger = RobustSlackMessenger()
    return messenger.send_message(text, channel, thread_ts)

def upload_file(file_path: str, channel: str = None, thread_ts: str = None, 
                title: str = None, comment: str = None) -> Dict[str, Any]:
    """Convenience function for uploading files"""
    messenger = RobustSlackMessenger()
    return messenger.upload_file(file_path, channel, thread_ts, title, comment)

def send_with_files(text: str, file_paths: List[str], channel: str = None, 
                    thread_ts: str = None) -> Dict[str, Any]:
    """Convenience function for sending messages with files"""
    messenger = RobustSlackMessenger()
    return messenger.send_message_with_files(text, file_paths, channel, thread_ts)

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(description="Robust Slack Messenger")
    parser.add_argument("action", choices=["send", "file", "test", "chunk-test"],
                       help="Action to perform")
    parser.add_argument("target", nargs="?", help="Message text or file path")
    parser.add_argument("--channel", "-c", default=SLACK_CHANNEL,
                       help=f"Slack channel (default: {SLACK_CHANNEL})")
    parser.add_argument("--thread", "-t", help="Thread timestamp")
    parser.add_argument("--title", help="File title (for uploads)")
    parser.add_argument("--comment", help="Initial comment (for uploads)")
    parser.add_argument("--token", help="Slack bot token (overrides env var)")
    
    args = parser.parse_args()
    
    # Use provided token or environment variable
    token = args.token or SLACK_BOT_TOKEN
    if not token:
        print("❌ Error: Slack bot token required.")
        print("   Set SLACK_BOT_TOKEN environment variable or use --token")
        sys.exit(1)
    
    messenger = RobustSlackMessenger(token, args.channel)
    
    if args.action == "test":
        # Test connection
        if messenger.test_connection():
            print("✅ Slack connection successful")
            
            # Test message
            response = messenger.send_message("Test message from RobustSlackMessenger")
            if response.get("ok"):
                print("✅ Test message sent successfully")
                print(f"   Timestamp: {response.get('ts')}")
            else:
                print(f"❌ Failed to send test message: {response.get('error')}")
        else:
            print("❌ Slack connection failed. Check token and permissions.")
    
    elif args.action == "send":
        if not args.target:
            print("❌ Error: Message text required for 'send' action")
            sys.exit(1)
        
        response = messenger.send_message(args.target, args.channel, args.thread)
        if response.get("ok"):
            print(f"✅ Message sent successfully")
            print(f"   Timestamp: {response.get('ts')}")
            print(f"   Chunks: {len(messenger._split_message(args.target))}")
        else:
            print(f"❌ Failed to send message: {response.get('error')}")
    
    elif args.action == "file":
        if not args.target:
            print("❌ Error: File path required for 'file' action")
            sys.exit(1)
        
        response = messenger.upload_file(
            args.target, args.channel, args.thread, args.title, args.comment
        )
        if response.get("ok"):
            print(f"✅ File uploaded successfully: {args.target}")
            if "file" in response:
                print(f"   File ID: {response['file'].get('id')}")
        else:
            print(f"❌ Failed to upload file: {response.get('error')}")
    
    elif args.action == "chunk-test":
        # Test message chunking
        test_text = "Line 1\n" * 1000  # Very long message
        chunks = messenger._split_message(test_text)
        print(f"📊 Chunking test:")
        print(f"   Original length: {len(test_text)} characters")
        print(f"   Number of chunks: {len(chunks)}")
        print(f"   Chunk sizes: {[len(c) for c in chunks[:3]]}...")
        
        # Show first chunk preview
        if chunks:
            preview = chunks[0][:100] + "..." if len(chunks[0]) > 100 else chunks[0]
            print(f"   First chunk preview: {preview}")

if __name__ == "__main__":
    main()