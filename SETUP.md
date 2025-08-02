# 🚀 Telegram Video Streamer Bot Setup Guide

## Overview

This bot automatically creates streaming URLs for videos sent to it. It supports:

- ✅ Direct video uploads
- ✅ Forwarded videos
- ✅ Group mentions with videos
- ✅ Browser streaming (Chrome, Firefox, Safari)
- ✅ VLC media player streaming
- ✅ All video formats supported

## Quick Setup

### 1. Get Your Bot Token

1. **Message @BotFather** on Telegram
2. **Send `/newbot`** command
3. **Choose a name** for your bot
4. **Choose a username** (must end with 'bot')
5. **Copy the token** (looks like: `123456789:ABCdefGHIjklMNOpqrSTUvwxYZ`)

### 2. Configure the Bot

1. **Edit `config.py`**:

   ```python
   BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
   BOT_USERNAME = "your_bot_username"  # Without @ symbol
   ```

2. **Find your bot username**:
   - Message your bot
   - Look at the bot's profile
   - Copy the username (without @)

### 3. Start the Bot

```bash
# Make the script executable
chmod +x run_bot.sh

# Start the bot
./run_bot.sh
```

## Detailed Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Internet connection

### Step-by-Step Installation

1. **Clone or download** this repository
2. **Navigate** to the project directory
3. **Edit configuration**:

   ```bash
   nano config.py
   ```

   Update:

   - `BOT_TOKEN` with your bot token
   - `BOT_USERNAME` with your bot username

4. **Start the bot**:
   ```bash
   ./run_bot.sh
   ```

### Testing the Bot

1. **Send a video** to your bot
2. **Forward a video** to your bot
3. **In a group**, mention your bot with a video:
   ```
   @your_bot_username stream this video
   ```

## Features

### 🎥 Video Support

- **All formats**: MP4, AVI, MOV, MKV, WebM, FLV, WMV, M4V, 3GP, OGV
- **File size**: Up to 100MB
- **Duration**: Any length
- **Quality**: Original quality preserved

### 🌐 Streaming Options

- **Browser URL**: Opens directly in Chrome/Firefox/Safari
- **VLC URL**: Works with VLC media player
- **Direct URL**: For embedding in websites

### 📱 Bot Commands

- `/start` - Show welcome message
- `/help` - Show help information
- `/streams` - List your active streams

### 🔄 Automatic Features

- **Auto-conversion**: Videos converted automatically
- **Stream cleanup**: Old streams deleted after 1 hour
- **Error handling**: Clear error messages
- **Progress updates**: Processing status shown

## Usage Examples

### Direct Upload

```
User: [sends video file]
Bot: ✅ Video converted successfully!
     🔗 Browser: http://localhost:5000/stream/stream_123
     📱 VLC: http://localhost:5000/vlc/stream_123
```

### Group Mention

```
User: @your_bot_username stream this video [with video]
Bot: ✅ Video converted successfully!
     🔗 Browser: http://localhost:5000/stream/stream_456
     📱 VLC: http://localhost:5000/vlc/stream_456
```

### Forward Video

```
User: [forwards video from another chat]
Bot: ✅ Video converted successfully!
     🔗 Browser: http://localhost:5000/stream/stream_789
     📱 VLC: http://localhost:5000/vlc/stream_789
```

## Configuration Options

### File Limits

```python
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
STREAM_RETENTION_HOURS = 1          # 1 hour
```

### Server Settings

```python
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5000        # Flask port
DEBUG = True       # Development mode
```

### Supported Formats

```python
SUPPORTED_VIDEO_EXTENSIONS = [
    '.mp4', '.avi', '.mov', '.mkv', '.webm',
    '.flv', '.wmv', '.m4v', '.3gp', '.ogv'
]
```

## Troubleshooting

### Common Issues

1. **"Bot not responding"**

   - Check if bot is running: `ps aux | grep python`
   - Verify token in `config.py`
   - Check internet connection

2. **"Invalid file ID"**

   - File may have been deleted from Telegram
   - Try sending the video again
   - Check bot permissions

3. **"File too large"**

   - Reduce video file size
   - Compress video before sending
   - Maximum size is 100MB

4. **"Flask app not running"**
   - Check if port 5000 is available
   - Try different port in `config.py`
   - Check firewall settings

### Debug Mode

Enable debug logging:

```python
DEBUG = True  # In config.py
```

### Logs

Check logs for errors:

```bash
# Flask logs
tail -f flask.log

# Bot logs
tail -f bot.log
```

## Production Deployment

### Security

1. **Change SECRET_KEY** in `config.py`
2. **Set DEBUG = False**
3. **Use HTTPS** for production
4. **Add authentication** if needed

### Server Setup

1. **Use Gunicorn** for Flask:

   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Use systemd** for auto-start:

   ```bash
   sudo systemctl enable telegram-streamer
   sudo systemctl start telegram-streamer
   ```

3. **Use Nginx** as reverse proxy:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## API Endpoints

### Web Interface

- `GET /` - Main web interface
- `GET /streams` - List active streams
- `POST /upload` - Upload video via web

### Streaming

- `GET /stream/{id}` - Browser streaming
- `GET /vlc/{id}` - VLC streaming
- `POST /create_stream` - Create stream from bot

### Bot Integration

- Automatic video processing
- Inline keyboard buttons
- Progress updates
- Error handling

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the logs
3. Test with a simple video file
4. Verify bot permissions

---

**🎉 Your Telegram Video Streamer Bot is ready to use!**
