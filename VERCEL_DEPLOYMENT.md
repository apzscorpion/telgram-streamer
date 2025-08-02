# Vercel Deployment Guide for Telegram Bot

This guide will help you deploy your Telegram bot to Vercel so it runs automatically without needing to start it manually.

## Prerequisites

1. **Node.js and npm** installed on your system
2. **Vercel CLI** (will be installed automatically)
3. **GitHub account** (for Vercel integration)

## Quick Deployment

### Option 1: Using the Deployment Script

1. Make the script executable:

   ```bash
   chmod +x deploy_vercel.sh
   ```

2. Run the deployment script:

   ```bash
   ./deploy_vercel.sh
   ```

3. Follow the prompts to:
   - Login to Vercel (if not already logged in)
   - Set up your project
   - Configure environment variables

### Option 2: Manual Deployment

1. **Install Vercel CLI**:

   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:

   ```bash
   vercel login
   ```

3. **Deploy to Vercel**:

   ```bash
   vercel --prod
   ```

4. **Set Environment Variables**:

   ```bash
   vercel env add BOT_TOKEN
   vercel env add CLOUDFLARE_WORKER_URL
   ```

5. **Set up Webhook** (after deployment):
   ```bash
   curl -X POST "https://your-app.vercel.app/set-webhook"
   ```

## Environment Variables

Set these in your Vercel dashboard or via CLI:

- `BOT_TOKEN`: Your Telegram bot token
- `CLOUDFLARE_WORKER_URL`: Your Cloudflare Worker URL for streaming

## How It Works

1. **Webhook-based**: Instead of polling, the bot uses Telegram webhooks
2. **Serverless**: Runs on Vercel's serverless functions
3. **Auto-start**: No need to manually start the bot
4. **Scalable**: Automatically scales with usage

## Bot Features

- ✅ Handles video files
- ✅ Handles document files (videos)
- ✅ Creates streaming URLs
- ✅ Works with forwarded videos
- ✅ Simple commands (/start, /help)

## Testing Your Bot

1. **Check if bot is running**:
   Visit: `https://your-app.vercel.app/`

2. **Check webhook status**:
   Visit: `https://your-app.vercel.app/get-webhook-info`

3. **Test with Telegram**:
   Send `/start` to your bot

## Troubleshooting

### Bot not responding?

1. Check webhook status: `https://your-app.vercel.app/get-webhook-info`
2. Re-set webhook: `https://your-app.vercel.app/set-webhook`
3. Check Vercel logs in dashboard

### Deployment failed?

1. Check if all environment variables are set
2. Ensure `vercel.json` is in root directory
3. Check `requirements-vercel.txt` has all dependencies

### Webhook not working?

1. Make sure your bot token is correct
2. Check if the domain is accessible
3. Try deleting and re-setting webhook

## Commands

- `/start` - Show welcome message
- `/help` - Show help information
- Send any video file - Get streaming URLs

## Support

If you encounter issues:

1. Check Vercel function logs
2. Verify environment variables
3. Test webhook endpoints manually
