#!/bin/bash

# Telegram Video Streamer Startup Script

echo "🚀 Starting Telegram Video Streamer..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Start the application
echo "🎥 Starting the application..."
echo "🌐 Open your browser and go to: http://localhost:5000"
echo "📱 The application will be available on all network interfaces"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py 