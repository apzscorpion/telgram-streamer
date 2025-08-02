#!/usr/bin/env python3
"""
Test if the bot is working and can receive messages
"""

import requests
import json
from config import *

def test_bot_webhook():
    """Test if bot is set up for webhooks"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            webhook_info = data['result']
            print("🔗 Webhook Information:")
            print(f"   URL: {webhook_info.get('url', 'Not set')}")
            print(f"   Has custom certificate: {webhook_info.get('has_custom_certificate', False)}")
            print(f"   Pending update count: {webhook_info.get('pending_update_count', 0)}")
            print(f"   Last error date: {webhook_info.get('last_error_date', 'None')}")
            print(f"   Last error message: {webhook_info.get('last_error_message', 'None')}")
            
            if webhook_info.get('url'):
                print("✅ Webhook is configured")
                return True
            else:
                print("⚠️  Webhook not configured - using polling")
                return False
        else:
            print(f"❌ Error getting webhook info: {data.get('description')}")
            return False
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return False

def test_bot_polling():
    """Test if bot is receiving updates via polling"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            updates = data['result']
            print(f"📱 Polling Test:")
            print(f"   Found {len(updates)} recent updates")
            
            if updates:
                print("✅ Bot is receiving updates via polling")
                return True
            else:
                print("📭 No updates found - bot is ready to receive messages")
                return True
        else:
            print(f"❌ Error getting updates: {data.get('description')}")
            return False
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return False

def send_test_message():
    """Send a test message to the bot"""
    print("\n📤 Sending test message to bot...")
    
    # Get bot info first
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            bot_info = data['result']
            print(f"✅ Bot info: @{bot_info['username']}")
            
            print("\n💡 To test the bot:")
            print("1. Open Telegram")
            print("2. Search for @MHStreamsBot")
            print("3. Send /start to the bot")
            print("4. Send a video file to the bot")
            print("5. The bot should respond with streaming URLs")
            
            return True
        else:
            print(f"❌ Bot error: {data.get('description')}")
            return False
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return False

def main():
    """Main test function"""
    print("🤖 Bot Working Test")
    print("=" * 50)
    
    # Test bot token
    print("\n1. Testing bot token...")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            bot_info = data['result']
            print(f"✅ Bot is working: @{bot_info['username']}")
            print(f"   Name: {bot_info['first_name']}")
            print(f"   ID: {bot_info['id']}")
        else:
            print(f"❌ Bot error: {data.get('description')}")
            return
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return
    
    # Test webhook
    print("\n2. Testing webhook configuration...")
    test_bot_webhook()
    
    # Test polling
    print("\n3. Testing polling...")
    test_bot_polling()
    
    # Send test instructions
    print("\n4. Testing bot interaction...")
    send_test_message()
    
    print("\n🎯 Next Steps:")
    print("1. Send a video to @MHStreamsBot")
    print("2. Run: python get_real_file_id.py")
    print("3. Check if the bot responds with streaming URLs")

if __name__ == "__main__":
    main() 