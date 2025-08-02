#!/bin/bash

# Restart Bot Script - Stops all instances and starts fresh

echo "🔄 Restarting Telegram Bot..."

# Kill all Python processes running telegram_bot.py
echo "🛑 Stopping all bot instances..."
pkill -f "telegram_bot.py" 2>/dev/null
pkill -f "python.*telegram_bot" 2>/dev/null

# Wait a moment for processes to stop
sleep 2

# Check if Flask app is running
if ! curl -s http://localhost:5000 > /dev/null; then
    echo "🌐 Starting Flask app..."
    source venv/bin/activate
    python app.py &
    sleep 3
fi

# Start the improved bot
echo "🤖 Starting improved bot..."
source venv/bin/activate
python telegram_bot_improved.py 