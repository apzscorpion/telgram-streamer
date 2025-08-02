#!/usr/bin/env python3
"""
Setup webhook for Telegram bot
"""

import requests
import json

# Bot configuration
BOT_TOKEN = "8445456449:AAGE0BaW2pSxJf7t4j5wb0Q09KRPItienPA"
WEBHOOK_URL = "https://telgram-streaming-l3gmzmgfb-asifs-projects-ddc64635.vercel.app/webhook"

def set_webhook():
    """Set webhook for the bot"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    data = {
        "url": WEBHOOK_URL,
        "allowed_updates": ["message", "edited_message", "channel_post", "edited_channel_post"]
    }
    
    print(f"🔗 Setting webhook to: {WEBHOOK_URL}")
    
    response = requests.post(url, json=data)
    result = response.json()
    
    if result.get('ok'):
        print("✅ Webhook set successfully!")
        print(f"📱 Bot will now receive updates at: {WEBHOOK_URL}")
        return True
    else:
        print(f"❌ Failed to set webhook: {result.get('description')}")
        return False

def get_webhook_info():
    """Get current webhook info"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    response = requests.get(url)
    result = response.json()
    
    if result.get('ok'):
        webhook_info = result['result']
        print("📊 Current webhook info:")
        print(f"   URL: {webhook_info.get('url', 'Not set')}")
        print(f"   Has custom certificate: {webhook_info.get('has_custom_certificate', False)}")
        print(f"   Pending update count: {webhook_info.get('pending_update_count', 0)}")
        print(f"   Last error date: {webhook_info.get('last_error_date', 'None')}")
        print(f"   Last error message: {webhook_info.get('last_error_message', 'None')}")
        return webhook_info
    else:
        print(f"❌ Error getting webhook info: {result.get('description')}")
        return None

def delete_webhook():
    """Delete webhook"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
    response = requests.post(url)
    result = response.json()
    
    if result.get('ok'):
        print("✅ Webhook deleted successfully!")
        return True
    else:
        print(f"❌ Failed to delete webhook: {result.get('description')}")
        return False

def test_bot():
    """Test if bot is working"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    response = requests.get(url)
    result = response.json()
    
    if result.get('ok'):
        bot_info = result['result']
        print(f"✅ Bot is working: @{bot_info['username']}")
        print(f"   Name: {bot_info['first_name']}")
        print(f"   ID: {bot_info['id']}")
        return True
    else:
        print(f"❌ Bot error: {result.get('description')}")
        return False

def main():
    """Main function"""
    print("🤖 Telegram Bot Webhook Setup")
    print("=" * 40)
    
    # Test bot first
    print("\n1. Testing bot connection...")
    if not test_bot():
        return
    
    # Get current webhook info
    print("\n2. Getting current webhook info...")
    get_webhook_info()
    
    # Set webhook
    print("\n3. Setting webhook...")
    if set_webhook():
        print("\n4. Verifying webhook...")
        get_webhook_info()
        
        print("\n🎉 Setup complete!")
        print("📱 Your bot should now respond to messages automatically.")
        print("💡 Try sending /start to your bot: @MHStreamsBot")
    else:
        print("\n❌ Setup failed. Please check the error message above.")

if __name__ == '__main__':
    main() 