#!/bin/bash

# Telegram Video Streamer Bot Startup Script

echo "🚀 Starting Telegram Video Streamer Bot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Start Flask app in background
echo "🌐 Starting Flask web server..."
python app.py &
FLASK_PID=$!

# Wait a moment for Flask to start
sleep 3

# Check if Flask is running
if curl -s http://localhost:5000 > /dev/null; then
    echo "✅ Flask app is running at http://localhost:5000"
else
    echo "❌ Flask app failed to start"
    exit 1
fi

# Start Telegram bot
echo "🤖 Starting Telegram bot..."
echo "📱 Make sure to update BOT_USERNAME in telegram_bot.py"
echo "🌐 Bot will use Flask app at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

# Start the bot
python telegram_bot.py

# Cleanup when bot stops
echo "🛑 Stopping services..."
kill $FLASK_PID 2>/dev/null
echo "✅ All services stopped" 