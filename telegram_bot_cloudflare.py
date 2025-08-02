#!/usr/bin/env python3
"""
Cloudflare Worker Telegram Bot
Uses Cloudflare Workers for streaming (like the other bot)
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

# Cloudflare Worker URL (replace with your deployed worker URL)
CLOUDFLARE_WORKER_URL = "https://telegram-file-proxy.your-subdomain.workers.dev"

def get_file_info(file_id):
    """Get file info from Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile"
    params = {'file_id': file_id}
    response = requests.get(url, params=params)
    return response.json()

def create_cloudflare_stream(file_id):
    """Create streaming URLs using Cloudflare Worker"""
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

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message."""
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

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video messages and create streaming URLs."""
    video = update.message.video
    user_id = update.effective_user.id
    
    if not video:
        await update.message.reply_text("❌ No video found in the message.")
        return
    
    # Send processing message
    processing_msg = await update.message.reply_text("⏳ Processing video... Please wait.")
    
    # Create Cloudflare Worker stream
    result, error = create_cloudflare_stream(video.file_id)
    
    if error:
        await processing_msg.edit_text(f"❌ Error: {error}")
        return
    
    # Create inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("🌐 Open in Browser", url=result['stream_url']),
            InlineKeyboardButton("📥 Download", url=result['download_url'])
        ],
        [
            InlineKeyboardButton("📋 Copy Stream URL", callback_data=f"copy_stream_{video.file_id}"),
            InlineKeyboardButton("📋 Copy Download URL", callback_data=f"copy_download_{video.file_id}")
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

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document messages (video files sent as documents)."""
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
    
    # Send processing message
    processing_msg = await update.message.reply_text("⏳ Processing video document... Please wait.")
    
    # Create Cloudflare Worker stream
    result, error = create_cloudflare_stream(document.file_id)
    
    if error:
        await processing_msg.edit_text(f"❌ Error: {error}")
        return
    
    # Create inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("🌐 Open in Browser", url=result['stream_url']),
            InlineKeyboardButton("📥 Download", url=result['download_url'])
        ],
        [
            InlineKeyboardButton("📋 Copy Stream URL", callback_data=f"copy_stream_{document.file_id}"),
            InlineKeyboardButton("📋 Copy Download URL", callback_data=f"copy_download_{document.file_id}")
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

async def handle_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle bot mentions in groups."""
    message = update.message
    user_id = update.effective_user.id
    
    # Check if bot is mentioned
    if not message.entities:
        return
    
    bot_mentioned = False
    for entity in message.entities:
        if entity.type == "mention" and f"@{BOT_USERNAME}" in message.text:
            bot_mentioned = True
            break
    
    if not bot_mentioned:
        return
    
    # Check if there's a video in the message
    video = message.video
    document = message.document
    
    if not video and not document:
        await message.reply_text("❌ Please include a video file when mentioning me.")
        return
    
    # Process the video
    if video:
        await handle_video(update, context)
    elif document:
        await handle_document(update, context)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith("copy_stream_"):
        file_id = data[12:]
        result, error = create_cloudflare_stream(file_id)
        if not error:
            await query.edit_message_text(f"🌐 **Stream URL:**\n\n`{result['stream_url']}`\n\nCopy this URL and open it in your browser.", parse_mode=ParseMode.MARKDOWN)
    
    elif data.startswith("copy_download_"):
        file_id = data[14:]
        result, error = create_cloudflare_stream(file_id)
        if not error:
            await query.edit_message_text(f"📥 **Download URL:**\n\n`{result['download_url']}`\n\nCopy this URL to download the file.", parse_mode=ParseMode.MARKDOWN)

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Handle videos and documents
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    # Handle mentions in groups
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_mention))
    
    # Handle button callbacks
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Start the bot
    print("🤖 Cloudflare Worker Telegram Bot is starting...")
    print(f"📱 Bot username: @{BOT_USERNAME}")
    print("🌐 Using Cloudflare Worker at:", CLOUDFLARE_WORKER_URL)
    print("")
    print("Features:")
    print("✅ Direct video uploads")
    print("✅ Forwarded videos (works like other bot)")
    print("✅ Group mentions")
    print("✅ Browser and download streaming")
    print("✅ All video formats supported")
    print("✅ Cloudflare Worker backend")
    print("")
    print("Press Ctrl+C to stop the bot")
    
    application.run_polling()

if __name__ == '__main__':
    main() 