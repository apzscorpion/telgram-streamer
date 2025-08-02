#!/usr/bin/env python3
"""
Telegram Bot for Automatic Video Streaming
Creates streaming URLs when mentioned or when videos are forwarded
"""

import asyncio
import os
import time
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode
import threading
import tempfile
import shutil

# Import configuration
from config import *

# Bot Configuration
BOT_TOKEN = BOT_TOKEN
BOT_USERNAME = BOT_USERNAME

# Flask app URL (for generating stream URLs)
FLASK_BASE_URL = FLASK_BASE_URL

# Store active streams
active_streams = {}

class VideoStream:
    def __init__(self, file_path, filename, file_id, user_id):
        self.file_path = file_path
        self.filename = filename
        self.file_id = file_id
        self.user_id = user_id
        self.created_at = datetime.now()
        self.access_count = 0

def get_file_info(file_id):
    """Get file info from Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile"
    params = {'file_id': file_id}
    response = requests.get(url, params=params)
    return response.json()

def download_telegram_file(file_path, local_path):
    """Download file from Telegram"""
    url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    return False

def create_stream_from_file_id(file_id, user_id):
    """Create a streaming URL from a Telegram file ID"""
    try:
        # Call Flask API to create stream
        response = requests.post(f"{FLASK_BASE_URL}/create_stream", json={
            'file_id': file_id,
            'user_id': user_id
        })
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data['stream_id'], None
            else:
                return None, data.get('error', 'Unknown error')
        else:
            return None, f"HTTP {response.status_code}: {response.text}"
            
    except Exception as e:
        return None, str(e)

def cleanup_old_streams():
    """Remove streams older than 1 hour"""
    current_time = datetime.now()
    to_remove = []
    
    for stream_id, stream in active_streams.items():
        if (current_time - stream.created_at).total_seconds() > 3600:  # 1 hour
            to_remove.append(stream_id)
    
    for stream_id in to_remove:
        stream = active_streams[stream_id]
        try:
            os.remove(stream.file_path)
        except:
            pass
        del active_streams[stream_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    welcome_message = """
🎬 **Welcome to Video Streamer Bot!**

I can convert your videos to streaming URLs that work in:
• 🌐 Chrome browser
• 📱 VLC media player
• 📺 Any video player

**How to use:**
1. Send me a video file
2. Forward a video to me
3. Mention me in a group with a video

I'll create streaming URLs for you automatically!

**Commands:**
/start - Show this help
/streams - Show your active streams
/help - Show help message
    """
    
    await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message."""
    help_text = """
📖 **How to use Video Streamer Bot:**

**Method 1: Direct Upload**
• Send me any video file
• I'll create streaming URLs automatically

**Method 2: Forward Videos**
• Forward any video to me
• I'll convert it to streaming URLs

**Method 3: Group Mentions**
• In a group, mention me with a video
• Example: "@your_bot_username stream this video"

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
    
    # Create stream
    stream_id, error = create_stream_from_file_id(video.file_id, user_id)
    
    if error:
        await processing_msg.edit_text(f"❌ Error: {error}")
        return
    
    # Create streaming URLs
    browser_url = f"{FLASK_BASE_URL}/stream/{stream_id}"
    vlc_url = f"{FLASK_BASE_URL}/stream/{stream_id}"
    
    # Create inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("🌐 Open in Browser", url=browser_url),
            InlineKeyboardButton("📱 VLC Stream URL", callback_data=f"vlc_{stream_id}")
        ],
        [
            InlineKeyboardButton("📋 Copy Browser URL", callback_data=f"copy_browser_{stream_id}"),
            InlineKeyboardButton("📋 Copy VLC URL", callback_data=f"copy_vlc_{stream_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Create response message
    file_size_mb = video.file_size / 1024 / 1024
    duration_min = video.duration // 60
    duration_sec = video.duration % 60
    
    response_text = f"""
✅ **Video converted successfully!**

📹 **Video Info:**
• Size: {file_size_mb:.1f} MB
• Duration: {duration_min}:{duration_sec:02d}
• Resolution: {video.width}x{video.height}

🔗 **Streaming URLs:**
• Browser: `{browser_url}`
• VLC: `{vlc_url}`

⏰ **Expires in:** 1 hour
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
    
    # Create stream
    stream_id, error = create_stream_from_file_id(document.file_id, user_id)
    
    if error:
        await processing_msg.edit_text(f"❌ Error: {error}")
        return
    
    # Create streaming URLs
    browser_url = f"{FLASK_BASE_URL}/stream/{stream_id}"
    vlc_url = f"{FLASK_BASE_URL}/stream/{stream_id}"
    
    # Create inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("🌐 Open in Browser", url=browser_url),
            InlineKeyboardButton("📱 VLC Stream URL", callback_data=f"vlc_{stream_id}")
        ],
        [
            InlineKeyboardButton("📋 Copy Browser URL", callback_data=f"copy_browser_{stream_id}"),
            InlineKeyboardButton("📋 Copy VLC URL", callback_data=f"copy_vlc_{stream_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Create response message
    file_size_mb = document.file_size / 1024 / 1024
    
    response_text = f"""
✅ **Video document converted successfully!**

📹 **Video Info:**
• Filename: {document.file_name}
• Size: {file_size_mb:.1f} MB

🔗 **Streaming URLs:**
• Browser: `{browser_url}`
• VLC: `{vlc_url}`

⏰ **Expires in:** 1 hour
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
    
    if data.startswith("vlc_"):
        stream_id = data[4:]
        if stream_id in active_streams:
            vlc_url = f"{FLASK_BASE_URL}/stream/{stream_id}"
            await query.edit_message_text(f"📱 **VLC Stream URL:**\n\n`{vlc_url}`\n\nCopy this URL and open it in VLC media player.", parse_mode=ParseMode.MARKDOWN)
    
    elif data.startswith("copy_browser_"):
        stream_id = data[13:]
        if stream_id in active_streams:
            browser_url = f"{FLASK_BASE_URL}/stream/{stream_id}"
            await query.edit_message_text(f"🌐 **Browser Stream URL:**\n\n`{browser_url}`\n\nCopy this URL and open it in your browser.", parse_mode=ParseMode.MARKDOWN)
    
    elif data.startswith("copy_vlc_"):
        stream_id = data[9:]
        if stream_id in active_streams:
            vlc_url = f"{FLASK_BASE_URL}/stream/{stream_id}"
            await query.edit_message_text(f"📱 **VLC Stream URL:**\n\n`{vlc_url}`\n\nCopy this URL and open it in VLC media player.", parse_mode=ParseMode.MARKDOWN)

async def list_streams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List user's active streams."""
    user_id = update.effective_user.id
    
    user_streams = [stream for stream in active_streams.values() if stream.user_id == user_id]
    
    if not user_streams:
        await update.message.reply_text("📭 You don't have any active streams.")
        return
    
    message = "📺 **Your Active Streams:**\n\n"
    
    for stream in user_streams:
        time_left = 3600 - (datetime.now() - stream.created_at).total_seconds()
        minutes_left = int(time_left // 60)
        
        stream_url = f"{FLASK_BASE_URL}/stream/{stream.file_id}"
        
        message += f"🎬 **{stream.filename}**\n"
        message += f"🔗 Browser: `{stream_url}`\n"
        message += f"⏰ Expires in: {minutes_left} minutes\n"
        message += f"👁️ Views: {stream.access_count}\n\n"
    
    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("streams", list_streams))
    
    # Handle videos and documents
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    # Handle mentions in groups
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_mention))
    
    # Handle button callbacks
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Start the bot
    print("🤖 Telegram Video Streamer Bot is starting...")
    print(f"📱 Bot username: @{BOT_USERNAME}")
    print("🌐 Make sure Flask app is running at:", FLASK_BASE_URL)
    print("")
    print("Features:")
    print("✅ Direct video uploads")
    print("✅ Forwarded videos")
    print("✅ Group mentions")
    print("✅ Browser and VLC streaming")
    print("✅ All video formats supported")
    print("")
    print("Press Ctrl+C to stop the bot")
    
    application.run_polling()

if __name__ == '__main__':
    main() 