# 🚀 Quick Start Guide

## Your Telegram Video Streamer is Ready!

The application is currently running at: **http://localhost:5000**

## How to Use

### Method 1: Using the Helper Bot (Recommended)

1. **Start the helper bot** to get file IDs:

   ```bash
   source venv/bin/activate
   python get_file_id.py
   ```

2. **Send a video to your bot** on Telegram
3. **Copy the file ID** that the bot sends back
4. **Go to http://localhost:5000** in your browser
5. **Paste the file ID** and click "Convert to Stream"
6. **Click the generated URL** to play the video

### Method 2: Manual File ID

1. **Get a file ID** from Telegram (using browser dev tools or other methods)
2. **Go to http://localhost:5000** in your browser
3. **Paste the file ID** and click "Convert to Stream"
4. **Click the generated URL** to play the video

## Features Available

✅ **Web Interface**: Beautiful, modern UI at http://localhost:5000  
✅ **Video Streaming**: Direct streaming URLs for browser playback  
✅ **File Management**: Automatic cleanup of old streams  
✅ **Statistics**: Track stream access and creation times  
✅ **Mobile Friendly**: Responsive design for all devices

## API Endpoints

- `GET /` - Web interface
- `POST /upload` - Convert file ID to stream URL
- `GET /stream/{id}` - Stream video file
- `GET /streams` - List active streams

## Example Usage

1. **Get a file ID**: `BQACAgIAAxkBAAIB...`
2. **Convert to stream**: POST to `/upload` with `{"file_id": "BQACAgIAAxkBAAIB..."}`
3. **Get stream URL**: `/stream/stream_1234567890`
4. **Play in browser**: Open the stream URL directly

## Troubleshooting

- **"Invalid file ID"**: Make sure the file is accessible to your bot
- **"File too large"**: Files must be under 100MB
- **Server not responding**: Check if the Flask app is running

## Next Steps

- The application is ready to use!
- Streams are automatically cleaned up after 1 hour
- All files are temporarily stored in the `uploads/` directory
- The web interface shows all active streams and their statistics

---

**🎉 Your Telegram Video Streamer is now live at http://localhost:5000**
