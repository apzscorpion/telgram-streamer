# Telegram Video Streamer

A web application that converts Telegram video files to streaming URLs. Upload a Telegram file ID and get a direct streaming URL that can be played in any web browser.

## Features

- 🎥 Convert Telegram videos to streaming URLs
- 🌐 Modern, responsive web interface
- 📱 Mobile-friendly design
- ⚡ Real-time video streaming
- 🧹 Automatic cleanup of old streams
- 📊 Stream statistics and management

## Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the Flask server:

```bash
python app.py
```

2. Open your web browser and go to:
   ```
   http://localhost:5000
   ```

The application will be available on `http://localhost:5000`

## How to Use

### Getting a Telegram File ID

1. **Using Telegram Bot API:**

   - Send a video to your bot
   - The bot will receive a message with a `file_id`
   - Use this `file_id` in the web interface

2. **Using Telegram Web:**
   - Open Telegram Web
   - Send a video to yourself or a chat
   - Use browser developer tools to find the file ID

### Converting Videos

1. Open the web interface at `http://localhost:5000`
2. Enter the Telegram file ID in the input field
3. Click "Convert to Stream"
4. The application will download the video and create a streaming URL
5. Click the generated URL to play the video in your browser

### Stream URLs

Generated stream URLs follow this format:

```
http://localhost:5000/stream/stream_[timestamp]
```

These URLs can be:

- Opened directly in a web browser
- Embedded in HTML video tags
- Shared with others (if the server is accessible)

## API Endpoints

### POST /upload

Convert a Telegram file ID to a streaming URL.

**Request:**

```json
{
  "file_id": "your_telegram_file_id"
}
```

**Response:**

```json
{
  "success": true,
  "stream_url": "/stream/stream_1234567890",
  "filename": "video_1234567890.mp4"
}
```

### GET /stream/{stream_id}

Stream a video file.

**Headers:**

- `Accept-Ranges: bytes` (for range requests)
- `Content-Type: video/mp4`

### GET /streams

List all active streams.

**Response:**

```json
[
  {
    "id": "stream_1234567890",
    "filename": "video_1234567890.mp4",
    "created_at": "2024-01-01T12:00:00",
    "access_count": 5,
    "stream_url": "/stream/stream_1234567890"
  }
]
```

## Configuration

### Environment Variables

You can set these environment variables:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token (default: provided in code)
- `FLASK_SECRET_KEY`: Flask secret key for sessions
- `MAX_FILE_SIZE`: Maximum file size in bytes (default: 100MB)

### File Limits

- Maximum file size: 100MB
- Stream retention: 1 hour
- Supported formats: MP4, AVI, MOV, and other video formats

## Security Notes

- The application uses your Telegram bot token to access files
- Files are temporarily stored on the server
- Old streams are automatically cleaned up after 1 hour
- The application is designed for development/testing use

## Troubleshooting

### Common Issues

1. **"Invalid file ID" error:**

   - Make sure the file ID is correct
   - Ensure the file is accessible to your bot

2. **"File too large" error:**

   - The file exceeds the 100MB limit
   - Consider using a smaller video file

3. **"Failed to download file" error:**
   - Check your internet connection
   - Verify the bot token is correct
   - Ensure the file still exists on Telegram

### Debug Mode

The application runs in debug mode by default. For production:

1. Set `FLASK_ENV=production`
2. Use a production WSGI server like Gunicorn
3. Configure proper security headers

## Development

### Project Structure

```
streamer/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/         # HTML templates
│   └── index.html    # Main web interface
├── uploads/          # Temporary video storage
└── README.md         # This file
```

### Adding Features

- **New video formats:** Modify the video processing logic in `app.py`
- **Authentication:** Add user authentication to protect streams
- **Database:** Use a database to persist stream information
- **CDN integration:** Add support for CDN streaming

## License

This project is for educational and development purposes. Use responsibly and in accordance with Telegram's terms of service.
