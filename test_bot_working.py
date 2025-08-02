#!/usr/bin/env python3
"""
Test script to check if bot token is working
"""

import os
import requests
import asyncio
from telegram import Bot
from telegram.ext import Application

# Environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8445456449:AAGE0BaW2pSxJf7t4j5wb0Q09KRPItienPA')

async def test_bot():
    """Test if bot can connect to Telegram"""
    try:
        print(f"🤖 Testing bot token: {BOT_TOKEN[:10]}...")
        
        # Create bot instance
        bot = Bot(token=BOT_TOKEN)
        
        # Test basic connection
        print("🔗 Testing connection to Telegram...")
        me = await bot.get_me()
        print(f"✅ Bot connected successfully!")
        print(f"📱 Bot name: {me.first_name}")
        print(f"👤 Bot username: @{me.username}")
        print(f"🆔 Bot ID: {me.id}")
        
        # Test getting updates
        print("📥 Testing get updates...")
        updates = await bot.get_updates(limit=1)
        print(f"✅ Get updates working! Found {len(updates)} updates")
        
        return True
        
    except Exception as e:
        print(f"❌ Bot test failed: {e}")
        return False

async def test_webhook():
    """Test webhook functionality"""
    try:
        print("🔗 Testing webhook setup...")
        
        # Create application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Test webhook info
        webhook_info = await application.bot.get_webhook_info()
        print(f"✅ Webhook info retrieved: {webhook_info}")
        
        return True
        
    except Exception as e:
        print(f"❌ Webhook test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 Starting bot tests...")
    
    # Test basic bot functionality
    bot_ok = await test_bot()
    
    # Test webhook functionality
    webhook_ok = await test_webhook()
    
    print("\n📊 Test Results:")
    print(f"Bot Connection: {'✅ PASS' if bot_ok else '❌ FAIL'}")
    print(f"Webhook Test: {'✅ PASS' if webhook_ok else '❌ FAIL'}")
    
    if bot_ok and webhook_ok:
        print("\n🎉 All tests passed! Your bot should work fine.")
        print("💡 Try deploying to Vercel now:")
        print("   ./deploy_vercel.sh")
    else:
        print("\n⚠️  Some tests failed. Check your bot token and network connection.")
        print("💡 Make sure your bot token is correct and you have internet access.")

if __name__ == '__main__':
    asyncio.run(main()) 