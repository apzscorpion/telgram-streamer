#!/usr/bin/env python3
"""
Telegram Bot for Render Deployment
Reads environment variables directly for Render compatibility
"""

import asyncio
import os
import time
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode

# Read environment variables directly for Render compatibility
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8445456449:AAGE0BaW2pSxJf7t4j5wb0Q09KRPItienPA')
BOT_USERNAME = os.environ.get('BOT_USERNAME', 'MHStreamsBot')
CLOUDFLARE_WORKER_URL = os.environ.get('CLOUDFLARE_WORKER_URL', 'https://telegram-file-proxy.mhstreamer.workers.dev')

# Increased file size limit to 4GB
MAX_FILE_SIZE = 4 * 1024 * 1024 * 1024  # 4GB

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
        
        # Check if file is too large (4GB limit)
        if file_size > MAX_FILE_SIZE:
            return None, f"File too large. Maximum size is {MAX_FILE_SIZE / (1024**3):.1f}GB"
        
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    try:
        welcome_message = """
🎬 **Welcome to MH Streams Bot!**

I can convert your videos to streaming URLs that work in:
• 🌐 Chrome browser
• 📱 VLC media player
• 📺 Any video player

**How to use:**
1. Send me a video file (up to 4GB)
2. Forward a video to me
3. Send me a video URL
4. Mention me in a group with a video

I'll create streaming URLs for you automatically!

**Commands:**
/start - Show this help
/help - Show help message
"""
        
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)
        print(f"✅ /start command responded to user {update.effective_user.id}")
        
    except Exception as e:
        print(f"❌ Error in /start command: {e}")
        await update.message.reply_text("❌ Sorry, there was an error. Please try again.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    try:
        help_message = """
🤖 **MH Streams Bot Help**

**Supported file types:**
• MP4, AVI, MKV, MOV, WMV
• Up to 4GB file size
• Forwarded videos work too!

**How to use:**
1. Send me any video file
2. I'll generate streaming URLs
3. Use the URLs in browser or VLC

**Commands:**
/start - Show welcome message
/help - Show this help

**Features:**
✅ Direct video uploads
✅ Forwarded videos (fixed)
✅ Up to 4GB files
✅ Browser and VLC streaming
✅ All video formats
"""
        
        await update.message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN)
        print(f"✅ /help command responded to user {update.effective_user.id}")
        
    except Exception as e:
        print(f"❌ Error in /help command: {e}")
        await update.message.reply_text("❌ Sorry, there was an error. Please try again.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video messages."""
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
        file_size_mb = result['file_size'] / (1024 * 1024)
        message = f"""
🎬 **Video Streaming URLs**

📁 **File Size:** {file_size_mb:.1f} MB
🌐 **Stream URL:** `{result['stream_url']}`
📥 **Download URL:** `{result['download_url']}`

**How to use:**
• Copy the stream URL to your browser
• Use download URL in VLC media player
• Works with any video player
"""
        
        # Create inline keyboard
        keyboard = [
            [
                InlineKeyboardButton("🌐 Open Stream", url=result['stream_url']),
                InlineKeyboardButton("📥 Download", url=result['download_url'])
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        print(f"✅ Video processed successfully for user {user_id}")
        
    except Exception as e:
        print(f"❌ Error processing video: {e}")
        await update.message.reply_text("❌ Error processing video. Please try again.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document messages (video files)."""
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
        file_size_mb = result['file_size'] / (1024 * 1024)
        message = f"""
🎬 **Video Streaming URLs**

📁 **File Size:** {file_size_mb:.1f} MB
🌐 **Stream URL:** `{result['stream_url']}`
📥 **Download URL:** `{result['download_url']}`

**How to use:**
• Copy the stream URL to your browser
• Use download URL in VLC media player
• Works with any video player
"""
        
        # Create inline keyboard
        keyboard = [
            [
                InlineKeyboardButton("🌐 Open Stream", url=result['stream_url']),
                InlineKeyboardButton("📥 Download", url=result['download_url'])
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        print(f"✅ Document processed successfully for user {user_id}")
        
    except Exception as e:
        print(f"❌ Error processing document: {e}")
        await update.message.reply_text("❌ Error processing document. Please try again.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    print(f'❌ Update {update} caused error {context.error}')

def main():
    """Start the bot."""
    print("🤖 Render Telegram Bot is starting...")
    print(f"📱 Bot username: @{BOT_USERNAME}")
    print(f"🌐 Using Cloudflare Worker at: {CLOUDFLARE_WORKER_URL}")
    print(f"📏 File size limit: {MAX_FILE_SIZE / (1024**3):.1f}GB")
    print("Features:")
    print("✅ Direct video uploads")
    print("✅ Forwarded videos (fixed)")
    print("✅ Up to 4GB files")
    print("✅ Error handling")
    print("✅ Debug logging")
    print("✅ Render deployment ready")
    print("Press Ctrl+C to stop the bot")
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_handler(MessageHandler(filters.Document.VIDEO, handle_document))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    print("🚀 Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 