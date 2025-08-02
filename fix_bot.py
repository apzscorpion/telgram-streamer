#!/usr/bin/env python3
"""
Script to fix bot configuration and test the bot
"""

import requests
import json
import os

def test_bot_token(token):
    """Test if a bot token is valid"""
    url = f"https://api.telegram.org/bot{token}/getMe"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            return True, data['result']
        else:
            return False, data.get('description', 'Unknown error')
    else:
        return False, f"HTTP {response.status_code}"

def get_new_token():
    """Guide user to get a new token"""
    print("🔧 Bot Token Fix")
    print("=" * 50)
    print("Your current bot token appears to be invalid.")
    print("Follow these steps to get a new token:")
    print()
    print("1. Open Telegram")
    print("2. Search for @BotFather")
    print("3. Send /newbot command")
    print("4. Choose a name for your bot")
    print("5. Choose a username (must end with 'bot')")
    print("6. Copy the token (looks like: 123456789:ABCdefGHIjklMNOpqrSTUvwxYZ)")
    print()
    
    token = input("Enter your new bot token: ").strip()
    
    if token:
        # Test the token
        is_valid, result = test_bot_token(token)
        
        if is_valid:
            print(f"✅ Valid token! Bot: @{result['username']}")
            update_config_files(token, result['username'])
            return True
        else:
            print(f"❌ Invalid token: {result}")
            return False
    else:
        print("❌ No token provided")
        return False

def update_config_files(token, username):
    """Update all configuration files with the new token"""
    files_to_update = [
        ('config.py', 'BOT_TOKEN', token),
        ('config.py', 'BOT_USERNAME', username),
        ('app.py', 'TELEGRAM_BOT_TOKEN', token),
        ('app_vercel.py', 'TELEGRAM_BOT_TOKEN', token),
        ('telegram_bot.py', 'BOT_TOKEN', token),
        ('telegram_bot.py', 'BOT_USERNAME', username),
        ('get_bot_info.py', 'BOT_TOKEN', token)
    ]
    
    for filename, variable, value in files_to_update:
        try:
            with open(filename, 'r') as f:
                content = f.read()
            
            # Update the variable
            if variable == 'BOT_TOKEN':
                # Find and replace the token
                import re
                content = re.sub(r'BOT_TOKEN\s*=\s*["\'][^"\']*["\']', f'BOT_TOKEN = "{value}"', content)
            elif variable == 'BOT_USERNAME':
                # Find and replace the username
                import re
                content = re.sub(r'BOT_USERNAME\s*=\s*["\'][^"\']*["\']', f'BOT_USERNAME = "{value}"', content)
            elif variable == 'TELEGRAM_BOT_TOKEN':
                # Find and replace the token
                import re
                content = re.sub(r'TELEGRAM_BOT_TOKEN\s*=\s*["\'][^"\']*["\']', f'TELEGRAM_BOT_TOKEN = "{value}"', content)
            
            with open(filename, 'w') as f:
                f.write(content)
            
            print(f"✅ Updated {filename}")
            
        except FileNotFoundError:
            print(f"⚠️  File {filename} not found, skipping...")
        except Exception as e:
            print(f"❌ Error updating {filename}: {e}")

def test_current_setup():
    """Test the current bot setup"""
    print("\n🧪 Testing Current Setup")
    print("=" * 50)
    
    # Test current token
    current_token = "7529698346:AAGwnFvdpVV1mEBSCgIu610rXna0BWhfTVY"
    is_valid, result = test_bot_token(current_token)
    
    if is_valid:
        print(f"✅ Current token is valid!")
        print(f"   Bot: @{result['username']}")
        print(f"   Name: {result['first_name']}")
        print(f"   ID: {result['id']}")
        
        # Update config with correct username
        update_config_files(current_token, result['username'])
        
        print("\n🎉 Bot is ready to use!")
        print("📱 Send a video to your bot to test it")
        
    else:
        print(f"❌ Current token is invalid: {result}")
        print("\n🔧 Let's fix this...")
        get_new_token()

def main():
    """Main function"""
    print("🤖 Telegram Bot Configuration Fixer")
    print("=" * 50)
    
    # Test current setup
    test_current_setup()
    
    print("\n📋 Next Steps:")
    print("1. Run: ./run_bot.sh")
    print("2. Send a video to your bot")
    print("3. The bot should respond with streaming URLs")
    print("4. If it doesn't work, check the logs")

if __name__ == "__main__":
    main() 