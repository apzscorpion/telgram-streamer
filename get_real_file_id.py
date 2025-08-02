#!/usr/bin/env python3
"""
Script to help get a real file ID from the bot
"""

import requests
import json
from config import *

def get_bot_updates():
    """Get recent updates from the bot"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            updates = data['result']
            print(f"📱 Found {len(updates)} recent updates")
            
            for i, update in enumerate(updates):
                message = update.get('message', {})
                if message:
                    user = message.get('from', {})
                    chat = message.get('chat', {})
                    
                    print(f"\n📨 Update {i+1}:")
                    print(f"   From: {user.get('first_name', 'Unknown')} (@{user.get('username', 'unknown')})")
                    print(f"   Chat: {chat.get('type', 'unknown')}")
                    
                    # Check for video
                    if 'video' in message:
                        video = message['video']
                        print(f"   🎥 Video found!")
                        print(f"   File ID: {video['file_id']}")
                        print(f"   File size: {video.get('file_size', 'unknown')} bytes")
                        print(f"   Duration: {video.get('duration', 'unknown')} seconds")
                        print(f"   Resolution: {video.get('width', 'unknown')}x{video.get('height', 'unknown')}")
                        
                        # Test this file ID
                        test_file_id(video['file_id'])
                        
                    # Check for document
                    elif 'document' in message:
                        document = message['document']
                        print(f"   📄 Document found!")
                        print(f"   File ID: {document['file_id']}")
                        print(f"   File name: {document.get('file_name', 'unknown')}")
                        print(f"   File size: {document.get('file_size', 'unknown')} bytes")
                        
                        # Test this file ID
                        test_file_id(document['file_id'])
                        
                    # Check for text
                    elif 'text' in message:
                        text = message['text']
                        print(f"   💬 Text: {text[:50]}...")
                        
                    else:
                        print(f"   📎 Other content type")
            
            if not updates:
                print("📭 No recent updates found")
                print("💡 Send a video to your bot to see updates here")
                
        else:
            print(f"❌ Error getting updates: {data.get('description')}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")

def test_file_id(file_id):
    """Test if a file ID is valid"""
    print(f"\n🧪 Testing file ID: {file_id}")
    
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
            
            # Test creating a stream
            create_stream(file_id)
            
        else:
            print(f"❌ File ID error: {data.get('description')}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")

def create_stream(file_id):
    """Create a stream with the file ID"""
    print(f"\n🌐 Creating stream for file ID: {file_id}")
    
    url = "http://localhost:5000/create_stream"
    data = {
        'file_id': file_id,
        'user_id': 12345
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Stream created successfully!")
                print(f"   Stream ID: {result['stream_id']}")
                print(f"   Stream URL: http://localhost:5000{result['stream_url']}")
                print(f"   VLC URL: http://localhost:5000{result['vlc_url']}")
            else:
                print(f"❌ Stream creation failed: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error creating stream: {e}")

def main():
    """Main function"""
    print("🔍 Bot File ID Inspector")
    print("=" * 50)
    
    # Check if bot token is valid
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            bot_info = data['result']
            print(f"✅ Bot is working: @{bot_info['username']}")
        else:
            print(f"❌ Bot error: {data.get('description')}")
            return
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return
    
    # Get recent updates
    print("\n📱 Checking recent bot updates...")
    get_bot_updates()
    
    print("\n💡 Instructions:")
    print("1. Send a video to @MHStreamsBot")
    print("2. Run this script again to see the file ID")
    print("3. The script will automatically test the file ID")

if __name__ == "__main__":
    main() 