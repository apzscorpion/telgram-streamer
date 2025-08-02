#!/usr/bin/env python3
"""
Test script to debug bot and file ID issues
"""

import requests
import json
from config import *

def test_bot_token():
    """Test if bot token is working"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            print(f"✅ Bot token is valid!")
            print(f"   Bot: @{data['result']['username']}")
            print(f"   Name: {data['result']['first_name']}")
            return True
        else:
            print(f"❌ Bot error: {data.get('description')}")
            return False
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return False

def test_file_id(file_id):
    """Test if a file ID is valid"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile"
    params = {'file_id': file_id}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            file_info = data['result']
            print(f"✅ File ID is valid!")
            print(f"   File path: {file_info['file_path']}")
            print(f"   File size: {file_info['file_size']} bytes")
            print(f"   File ID: {file_info['file_id']}")
            return True
        else:
            print(f"❌ File ID error: {data.get('description')}")
            return False
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return False

def test_flask_endpoint():
    """Test Flask endpoint"""
    try:
        response = requests.get("http://localhost:5000/streams")
        if response.status_code == 200:
            print("✅ Flask app is running")
            return True
        else:
            print(f"❌ Flask app error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Flask app not running: {e}")
        return False

def create_test_stream():
    """Create a test stream"""
    # This is a sample file ID - you need to replace with a real one
    test_file_id = "BQACAgIAAxkBAAIB..."  # This is just a placeholder
    
    url = "http://localhost:5000/create_stream"
    data = {
        'file_id': test_file_id,
        'user_id': 12345
    }
    
    response = requests.post(url, json=data)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print("✅ Stream created successfully!")
            print(f"   Stream ID: {result['stream_id']}")
            print(f"   Stream URL: {result['stream_url']}")
        else:
            print(f"❌ Stream creation failed: {result.get('error')}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")

def main():
    """Main test function"""
    print("🧪 Bot and File ID Test")
    print("=" * 50)
    
    # Test bot token
    print("\n1. Testing bot token...")
    if not test_bot_token():
        print("❌ Bot token is invalid. Please check your configuration.")
        return
    
    # Test Flask app
    print("\n2. Testing Flask app...")
    if not test_flask_endpoint():
        print("❌ Flask app is not running. Start it with: python app.py")
        return
    
    # Test file ID (you need to provide a real file ID)
    print("\n3. Testing file ID...")
    print("📝 To test with a real file ID:")
    print("   1. Send a video to your bot")
    print("   2. Copy the file ID from the bot's response")
    print("   3. Run: python test_bot.py <file_id>")
    
    # If file ID provided as argument
    import sys
    if len(sys.argv) > 1:
        file_id = sys.argv[1]
        print(f"\nTesting file ID: {file_id}")
        if test_file_id(file_id):
            create_test_stream()
    else:
        print("\n💡 To test with a real file ID, run:")
        print("   python test_bot.py <your_file_id>")

if __name__ == "__main__":
    main() 