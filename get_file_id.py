#!/usr/bin/env python3
"""
Helper script to get Telegram file IDs using the bot API.
This script demonstrates how to receive messages and extract file IDs.
"""

import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Your bot token
BOT_TOKEN = "7529698346:AAGwnFvdpVV1mEBSCgIu610rXna0BWhfTVY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Hello! I'm a helper bot to get file IDs.\n"
        "Send me a video file and I'll show you the file ID."
    )

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video messages and show file ID."""
    video = update.message.video
    
    if video:
        file_id = video.file_id
        file_size = video.file_size
        duration = video.duration
        width = video.width
        height = video.height
        
        message = f"""
📹 Video File Information:

📋 File ID: `{file_id}`
📏 Size: {file_size} bytes ({file_size / 1024 / 1024:.2f} MB)
⏱️ Duration: {duration} seconds
📐 Resolution: {width}x{height}

💡 Copy the File ID above and use it in the web interface!
        """
        
        await update.message.reply_text(message, parse_mode='Markdown')
    else:
        await update.message.reply_text("Please send a video file.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document messages and show file ID."""
    document = update.message.document
    
    if document:
        file_id = document.file_id
        file_name = document.file_name
        file_size = document.file_size
        
        message = f"""
📄 Document File Information:

📋 File ID: `{file_id}`
📁 Filename: {file_name}
📏 Size: {file_size} bytes ({file_size / 1024 / 1024:.2f} MB)

💡 Copy the File ID above and use it in the web interface!
        """
        
        await update.message.reply_text(message, parse_mode='Markdown')
    else:
        await update.message.reply_text("Please send a document file.")

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Start the bot
    print("🤖 Bot is starting...")
    print("📱 Send /start to the bot to begin")
    print("📹 Send video files to get their file IDs")
    print("📄 Send document files to get their file IDs")
    print("🌐 Then use the file IDs in the web interface at http://localhost:5000")
    print("")
    print("Press Ctrl+C to stop the bot")
    
    application.run_polling()

if __name__ == '__main__':
    main() 