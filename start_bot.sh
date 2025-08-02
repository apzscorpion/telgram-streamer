#!/bin/bash

echo "🤖 Starting Telegram Bot..."
echo "📱 Bot: @MHStreamsBot"
echo "🌐 Cloudflare Worker: https://telegram-file-proxy.mhstreamer.workers.dev"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -r requirements.txt

# Set environment variables
export BOT_TOKEN="8445456449:AAGE0BaW2pSxJf7t4j5wb0Q09KRPItienPA"
export CLOUDFLARE_WORKER_URL="https://telegram-file-proxy.mhstreamer.workers.dev"

echo "🚀 Starting bot with improved error handling..."
echo "💡 Press Ctrl+C to stop the bot"
echo ""

# Start the improved bot
python simple_bot_improved.py 