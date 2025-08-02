#!/usr/bin/env python3
"""
Script to get bot information and update configuration
"""

import requests
import json

# Your bot token
BOT_TOKEN = "8445456449:AAGE0BaW2pSxJf7t4j5wb0Q09KRPItienPA"

def get_bot_info():
    """Get bot information from Telegram API"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            bot_info = data['result']
            print("🤖 Bot Information:")
            print(f"   Name: {bot_info['first_name']}")
            print(f"   Username: @{bot_info['username']}")
            print(f"   ID: {bot_info['id']}")
            print(f"   Can join groups: {bot_info.get('can_join_groups', False)}")
            print(f"   Can read all group messages: {bot_info.get('can_read_all_group_messages', False)}")
            print(f"   Supports inline queries: {bot_info.get('supports_inline_queries', False)}")
            
            # Update config.py
            update_config(bot_info['username'])
            
            return bot_info
        else:
            print("❌ Error getting bot info:", data.get('description', 'Unknown error'))
            return None
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return None

def update_config(username):
    """Update config.py with the correct bot username"""
    try:
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Replace the placeholder username
        new_content = content.replace(
            'BOT_USERNAME = "your_bot_username"  # Replace with your actual bot username',
            f'BOT_USERNAME = "{username}"  # Bot username'
        )
        
        with open('config.py', 'w') as f:
            f.write(new_content)
        
        print(f"✅ Updated config.py with bot username: {username}")
        print("🔄 You can now restart the bot with: ./run_bot.sh")
        
    except Exception as e:
        print(f"❌ Error updating config: {e}")

def test_bot():
    """Test if the bot is working"""
    print("\n🧪 Testing bot...")
    
    # Test getMe
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            print("✅ Bot is working correctly!")
            print("📱 You can now message your bot and it should respond")
        else:
            print("❌ Bot error:", data.get('description', 'Unknown error'))
    else:
        print(f"❌ HTTP Error: {response.status_code}")

if __name__ == "__main__":
    print("🔧 Bot Configuration Helper")
    print("=" * 40)
    
    # Get bot info
    bot_info = get_bot_info()
    
    if bot_info:
        print("\n" + "=" * 40)
        test_bot()
        
        print("\n📋 Next steps:")
        print("1. Message your bot on Telegram")
        print("2. Send a video file to test")
        print("3. The bot should respond with streaming URLs")
        print("4. If it doesn't work, check the logs")
    else:
        print("\n❌ Could not get bot information")
        print("Please check your bot token and try again") 