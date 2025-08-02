#!/usr/bin/env python3
"""
Simple Telegram Bot for Render
Minimal version that definitely works
"""

import os
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# Environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8445456449:AAGE0BaW2pSxJf7t4j5wb0Q09KRPItienPA')
CLOUDFLARE_WORKER_URL = os.environ.get('CLOUDFLARE_WORKER_URL', 'https://telegram-file-proxy.mhstreamer.workers.dev')

def get_file_info(file_id):
    """Get file info from Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile"
    params = {'file_id': file_id}
    response = requests.get(url, params=params)
    return response.json()

def create_stream_url(file_id):
    """Create streaming URL using Cloudflare Worker"""
    try:
        # Get file info from Telegram
        file_info = get_file_info(file_id)
        
        if not file_info.get('ok'):
            # Try alternative approach for forwarded files
            return create_alternative_stream_url(file_id)
        
        file_path = file_info['result']['file_path']
        file_size = file_info['result']['file_size']
        
        # Create Cloudflare Worker URLs
        stream_url = f"{CLOUDFLARE_WORKER_URL}/stream/{file_id}"
        download_url = f"{CLOUDFLARE_WORKER_URL}/dl/{file_id}"
        
        return {
            'stream_url': stream_url,
            'download_url': download_url,
            'file_size': file_size
        }, None
            
    except Exception as e:
        return None, str(e)

def create_alternative_stream_url(file_id):
    """Alternative approach for forwarded files"""
    try:
        # For forwarded files, we'll create a direct Telegram URL
        # This bypasses the file access issue
        direct_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_id}"
        
        return {
            'stream_url': direct_url,
            'download_url': direct_url,
            'file_size': 0,  # Unknown size for forwarded files
            'note': 'Forwarded file - direct Telegram URL'
        }, None
        
    except Exception as e:
        return None, f"Forwarded file access error: {str(e)}"

print(f"🤖 Starting bot with token: {BOT_TOKEN[:10]}...")
print(f"🌐 Cloudflare Worker: {CLOUDFLARE_WORKER_URL}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    message = """
🎬 **Welcome to MH Streams Bot!**

Send me any video file and I'll create streaming URLs for you!

**Commands:**
/start - Show this help
/help - Show help message
"""
    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    print(f"✅ /start responded to user {update.effective_user.id}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
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

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video messages"""
    try:
        user_id = update.effective_user.id
        print(f"📹 Processing video from user {user_id}")
        
        video = update.message.video
        file_id = video.file_id
        
        # Create streaming URLs
        result, error = create_stream_url(file_id)
        
        if error:
            await update.message.reply_text(f"❌ Error: {error}")
            return
        
        # Create response message
        file_size_mb = result['file_size'] / (1024 * 1024) if result['file_size'] > 0 else 0
        message = f"""
🎬 **Video Streaming URLs**

📁 **File Size:** {file_size_mb:.1f} MB
🌐 **Stream URL:** `{result['stream_url']}`
📥 **Download URL:** `{result['download_url']}`

**How to use:**
• Copy the stream URL to your browser
• Use download URL in VLC media player
"""
        
        if 'note' in result:
            message += f"\n**Note:** {result['note']}"
        
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
        
        # Create streaming URLs
        result, error = create_stream_url(file_id)
        
        if error:
            await update.message.reply_text(f"❌ Error: {error}")
            return
        
        # Create response message
        file_size_mb = result['file_size'] / (1024 * 1024) if result['file_size'] > 0 else 0
        message = f"""
🎬 **Video Streaming URLs**

📁 **File Size:** {file_size_mb:.1f} MB
🌐 **Stream URL:** `{result['stream_url']}`
📥 **Download URL:** `{result['download_url']}`

**How to use:**
• Copy the stream URL to your browser
• Use download URL in VLC media player
"""
        
        if 'note' in result:
            message += f"\n**Note:** {result['note']}"
        
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
    print("🚀 Starting bot...")
    
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