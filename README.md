# Telegram Video Streaming Bot

A simple Telegram bot that creates streaming URLs for video files. Users can send video files to the bot and receive streaming URLs that can be used in browsers or media players.

## Features

- ✅ **Video Streaming**: Creates streaming URLs for any video file
- ✅ **Document Support**: Handles video files sent as documents
- ✅ **Forwarded Videos**: Works with forwarded videos from other chats
- ✅ **Multiple Formats**: Supports all video formats supported by Telegram
- ✅ **Cloudflare Integration**: Uses Cloudflare Workers for streaming
- ✅ **Auto-deployment**: Deploy to Vercel for automatic startup

## Quick Start

### Option 1: Deploy to Vercel (Recommended)

1. **Setup Vercel**:

   ```bash
   ./setup_vercel.sh
   ```

2. **Deploy to Vercel**:

   ```bash
   ./deploy_vercel.sh
   ```

3. **Set Environment Variables**:
   - `BOT_TOKEN`: Your Telegram bot token
   - `CLOUDFLARE_WORKER_URL`: Your Cloudflare Worker URL

### Option 2: Run Locally

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**:

   ```bash
   export BOT_TOKEN="your_bot_token"
   export CLOUDFLARE_WORKER_URL="your_cloudflare_worker_url"
   ```

3. **Run the bot**:
   ```bash
   python simple_bot.py
   ```

## Bot Commands

- `/start` - Show welcome message and help
- `/help` - Show detailed help information
- Send any video file - Get streaming URLs

## How It Works

1. **User sends video** to the bot
2. **Bot extracts file ID** from the video
3. **Creates streaming URLs** using Cloudflare Worker
4. **Returns URLs** to user for streaming

## Streaming URLs

The bot creates two types of URLs:

- **Stream URL**: For browser playback
- **Download URL**: For VLC media player or direct download

## Deployment Options

### Vercel (Recommended)

- ✅ Automatic startup
- ✅ No manual commands needed
- ✅ Scalable and reliable
- ✅ Webhook-based (no polling)

### Local Development

- ✅ Full control
- ✅ Easy debugging
- ✅ No deployment needed
- ⚠️ Requires manual startup

### Other Platforms

- Railway
- Render
- Heroku
- DigitalOcean

## Environment Variables

| Variable                | Description                        | Required |
| ----------------------- | ---------------------------------- | -------- |
| `BOT_TOKEN`             | Telegram bot token from @BotFather | Yes      |
| `CLOUDFLARE_WORKER_URL` | Your Cloudflare Worker URL         | Yes      |

## File Structure

```
streamer/
├── app_vercel.py          # Vercel deployment file
├── simple_bot.py          # Local bot file
├── vercel.json            # Vercel configuration
├── requirements-vercel.txt # Vercel dependencies
├── deploy_vercel.sh       # Deployment script
├── setup_vercel.sh        # Setup script
└── VERCEL_DEPLOYMENT.md   # Deployment guide
```

## Troubleshooting

### Bot not responding?

1. Check if bot token is correct
2. Verify webhook is set (for Vercel)
3. Check logs for errors

### Streaming not working?

1. Verify Cloudflare Worker URL
2. Check if file is accessible
3. Test with smaller video files

### Deployment issues?

1. Check environment variables
2. Verify Vercel CLI installation
3. Check deployment logs

## Support

For issues and questions:

1. Check the deployment guide: `VERCEL_DEPLOYMENT.md`
2. Review the troubleshooting section
3. Check Vercel function logs

## License

This project is open source and available under the MIT License.
