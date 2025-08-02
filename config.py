# Telegram Video Streamer Bot Configuration

# Bot Configuration
BOT_TOKEN = "8445456449:AAGE0BaW2pSxJf7t4j5wb0Q09KRPItienPA"

# IMPORTANT: Replace this with your actual bot username (without @)
# You can find your bot username by messaging @BotFather
BOT_USERNAME = "MHStreamsBot"  # Replace with your actual bot username

# Flask app configuration
FLASK_BASE_URL = "http://localhost:5000"  # Change this if your server is on a different URL

# File limits
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB in bytes
STREAM_RETENTION_HOURS = 1  # How long streams are kept

# Supported video formats
SUPPORTED_VIDEO_EXTENSIONS = [
    '.mp4', '.avi', '.mov', '.mkv', '.webm', 
    '.flv', '.wmv', '.m4v', '.3gp', '.ogv'
]

# Server configuration
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5000        # Flask port

# Development settings
DEBUG = True        # Set to False for production
SECRET_KEY = "your-secret-key-here"  # Change this for production 