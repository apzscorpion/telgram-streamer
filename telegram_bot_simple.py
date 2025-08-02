#!/usr/bin/env python3
"""
Simple Telegram Bot for Video Streaming
Fixed version with proper error handling
"""

import asyncio
import os
import time
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode

# Import configuration
from config import *

# Cloudflare Worker URL (UPDATE THIS WITH YOUR ACTUAL URL)
CLOUDFLARE_WORKER_URL = "https://telegram-file-proxy.your-subdomain.workers.dev"

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
            return None, "Invalid file ID or bot doesn't have access to this file"
        
        file_path = file_info['result']['file_path']
        file_size = file_info['result']['file_size']
        
        # Check if file is too large (100MB limit)
        if file_size > 100 * 1024 * 1024:
            return None, "File too large. Maximum size is 100MB"
        
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
1. Send me a video file
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
        print(f"❌ Error in /start: {e}")
        await update.message.reply_text("❌ Sorry, there was an error. Please try again.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message."""
    try:
        help_text = """
📖 **How to use MH Streams Bot:**

**Method 1: Direct Upload**
• Send me any video file
• I'll create streaming URLs automatically

**Method 2: Forward Videos**
• Forward any video to me (even from other groups)
• I'll create direct streaming URLs

**Method 3: Video URLs**
• Send me a direct video URL
• I'll create streaming URLs

**Method 4: Group Mentions**
• In a group, mention me with a video
• Example: "@MHStreamsBot stream this video"

**Supported Formats:**
• MP4, AVI, MOV, MKV, WebM
• Any video format Telegram supports

**Stream URLs:**
• Browser URL: Opens in Chrome/Firefox
• VLC URL: Works with VLC media player
• Direct URL: For embedding in websites

**File Limits:**
• Maximum size: 100MB
• Stream retention: 1 hour
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
        print(f"✅ /help command responded to user {update.effective_user.id}")
        
    except Exception as e:
        print(f"❌ Error in /help: {e}")
        await update.message.reply_text("❌ Sorry, there was an error. Please try again.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video messages and create streaming URLs."""
    try:
        video = update.message.video
        user_id = update.effective_user.id
        
        if not video:
            await update.message.reply_text("❌ No video found in the message.")
            return
        
        print(f"📹 Processing video from user {user_id}")
        
        # Send processing message
        processing_msg = await update.message.reply_text("⏳ Processing video... Please wait.")
        
        # Create streaming URLs
        result, error = create_stream_url(video.file_id)
        
        if error:
            await processing_msg.edit_text(f"❌ Error: {error}")
            print(f"❌ Error processing video: {error}")
            return
        
        # Create inline keyboard
        keyboard = [
            [
                InlineKeyboardButton("🌐 Open in Browser", url=result['stream_url']),
                InlineKeyboardButton("📥 Download", url=result['download_url'])
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Create response message
        file_size_mb = video.file_size / 1024 / 1024
        duration_min = video.duration // 60
        duration_sec = video.duration % 60
        
        response_text = f"""
✅ **Links Generated Successfully!**

📹 **Video Info:**
• File Name: {video.file_name or f"video_{int(time.time())}.mp4"}
• File Size: {file_size_mb:.1f} MB
• Duration: {duration_min}:{duration_sec:02d}
• Resolution: {video.width}x{video.height}

🔗 **Links:**
• Stream: `{result['stream_url']}`
• Download: `{result['download_url']}`
        """
        
        await processing_msg.edit_text(response_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        print(f"✅ Video processed successfully for user {user_id}")
        
    except Exception as e:
        print(f"❌ Error in handle_video: {e}")
        await update.message.reply_text("❌ Sorry, there was an error processing your video. Please try again.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document messages (video files sent as documents)."""
    try:
        document = update.message.document
        user_id = update.effective_user.id
        
        if not document:
            await update.message.reply_text("❌ No document found in the message.")
            return
        
        # Check if it's a video file
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.m4v']
        file_name = document.file_name.lower()
        
        is_video = any(file_name.endswith(ext) for ext in video_extensions)
        
        if not is_video:
            await update.message.reply_text("❌ Please send a video file.")
            return
        
        print(f"📄 Processing document from user {user_id}")
        
        # Send processing message
        processing_msg = await update.message.reply_text("⏳ Processing video document... Please wait.")
        
        # Create streaming URLs
        result, error = create_stream_url(document.file_id)
        
        if error:
            await processing_msg.edit_text(f"❌ Error: {error}")
            print(f"❌ Error processing document: {error}")
            return
        
        # Create inline keyboard
        keyboard = [
            [
                InlineKeyboardButton("🌐 Open in Browser", url=result['stream_url']),
                InlineKeyboardButton("📥 Download", url=result['download_url'])
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Create response message
        file_size_mb = document.file_size / 1024 / 1024
        
        response_text = f"""
✅ **Links Generated Successfully!**

📹 **Video Info:**
• File Name: {document.file_name}
• File Size: {file_size_mb:.1f} MB

🔗 **Links:**
• Stream: `{result['stream_url']}`
• Download: `{result['download_url']}`
        """
        
        await processing_msg.edit_text(response_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        print(f"✅ Document processed successfully for user {user_id}")
        
    except Exception as e:
        print(f"❌ Error in handle_document: {e}")
        await update.message.reply_text("❌ Sorry, there was an error processing your document. Please try again.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    print(f"❌ Error: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("❌ Sorry, there was an error. Please try again.")

def main():
    """Start the bot."""
    try:
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()

        # Add error handler
        application.add_error_handler(error_handler)

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        
        # Handle videos and documents
        application.add_handler(MessageHandler(filters.VIDEO, handle_video))
        application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

        # Start the bot
        print("🤖 Simple Telegram Bot is starting...")
        print(f"📱 Bot username: @{BOT_USERNAME}")
        print("🌐 Using Cloudflare Worker at:", CLOUDFLARE_WORKER_URL)
        print("")
        print("Features:")
        print("✅ Direct video uploads")
        print("✅ Forwarded videos")
        print("✅ Error handling")
        print("✅ Debug logging")
        print("")
        print("Press Ctrl+C to stop the bot")
        
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

if __name__ == '__main__':
    main() 