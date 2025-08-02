#!/usr/bin/env python3
"""
Simple Telegram Bot for Render Deployment
Minimal version with better error handling
"""

import os
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# Environment variables with fallbacks
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8445456449:AAGE0BaW2pSxJf7t4j5wb0Q09KRPItienPA')
BOT_USERNAME = os.environ.get('BOT_USERNAME', 'MHStreamsBot')
CLOUDFLARE_WORKER_URL = os.environ.get('CLOUDFLARE_WORKER_URL', 'https://telegram-file-proxy.mhstreamer.workers.dev')

print(f"🤖 Bot starting with token: {BOT_TOKEN[:10]}...")
print(f"📱 Bot username: {BOT_USERNAME}")
print(f"🌐 Cloudflare Worker: {CLOUDFLARE_WORKER_URL}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    try:
        message = """
🎬 **Welcome to MH Streams Bot!**

I can convert your videos to streaming URLs.

**How to use:**
1. Send me a video file
2. I'll generate streaming URLs
3. Use the URLs in browser or VLC

**Commands:**
/start - Show this help
/help - Show help message
"""
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        print(f"✅ /start responded to user {update.effective_user.id}")
    except Exception as e:
        print(f"❌ Error in /start: {e}")
        await update.message.reply_text("❌ Error occurred. Please try again.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    try:
        message = """
🤖 **MH Streams Bot Help**

Send me any video file and I'll create streaming URLs for you!

**Supported:**
• All video formats
• Up to 4GB files
• Forwarded videos
"""
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        print(f"✅ /help responded to user {update.effective_user.id}")
    except Exception as e:
        print(f"❌ Error in /help: {e}")
        await update.message.reply_text("❌ Error occurred. Please try again.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video messages"""
    try:
        user_id = update.effective_user.id
        print(f"📹 Processing video from user {user_id}")
        
        video = update.message.video
        file_id = video.file_id
        
        # Create simple streaming URLs
        stream_url = f"{CLOUDFLARE_WORKER_URL}/stream/{file_id}"
        download_url = f"{CLOUDFLARE_WORKER_URL}/dl/{file_id}"
        
        message = f"""
🎬 **Video Streaming URLs**

🌐 **Stream URL:** `{stream_url}`
📥 **Download URL:** `{download_url}`

**How to use:**
• Copy the stream URL to your browser
• Use download URL in VLC media player
"""
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        print(f"✅ Video processed for user {user_id}")
        
    except Exception as e:
        print(f"❌ Error processing video: {e}")
        await update.message.reply_text("❌ Error processing video. Please try again.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document messages"""
    try:
        user_id = update.effective_user.id
        print(f"📄 Processing document from user {user_id}")
        
        document = update.message.document
        file_id = document.file_id
        
        # Check if it's a video file
        mime_type = document.mime_type or ""
        if not mime_type.startswith('video/'):
            await update.message.reply_text("❌ Please send a video file.")
            return
        
        # Create simple streaming URLs
        stream_url = f"{CLOUDFLARE_WORKER_URL}/stream/{file_id}"
        download_url = f"{CLOUDFLARE_WORKER_URL}/dl/{file_id}"
        
        message = f"""
🎬 **Video Streaming URLs**

🌐 **Stream URL:** `{stream_url}`
📥 **Download URL:** `{download_url}`

**How to use:**
• Copy the stream URL to your browser
• Use download URL in VLC media player
"""
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        print(f"✅ Document processed for user {user_id}")
        
    except Exception as e:
        print(f"❌ Error processing document: {e}")
        await update.message.reply_text("❌ Error processing document. Please try again.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    print(f'❌ Update {update} caused error {context.error}')

def main():
    """Start the bot."""
    print("🚀 Starting simple Render bot...")
    
    try:
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.VIDEO, handle_video))
        application.add_handler(MessageHandler(filters.Document.VIDEO, handle_document))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        print("✅ Bot created successfully")
        print("🔄 Starting polling...")
        
        # Start the bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
        raise

if __name__ == '__main__':
    main() 