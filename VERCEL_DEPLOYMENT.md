# 🚀 Vercel Deployment Guide

## Overview

This guide will help you deploy your Telegram Video Streamer to Vercel. The Vercel version uses in-memory storage and proxies Telegram files directly.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Account**: For repository hosting
3. **Valid Bot Token**: Get from @BotFather

## Step 1: Fix Your Bot Token

First, you need to get a valid bot token:

1. **Message @BotFather** on Telegram
2. **Send `/newbot`** command
3. **Choose a name** for your bot
4. **Choose a username** (must end with 'bot')
5. **Copy the token** (looks like: `123456789:ABCdefGHIjklMNOpqrSTUvwxYZ`)

## Step 2: Prepare for Deployment

### Option A: Use Vercel CLI

1. **Install Vercel CLI**:

   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:

   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

### Option B: Deploy via GitHub

1. **Push to GitHub**:

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/telegram-streamer.git
   git push -u origin main
   ```

2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Configure environment variables

## Step 3: Environment Variables

Set these environment variables in Vercel:

### Required Variables

1. **TELEGRAM_BOT_TOKEN**: Your bot token from @BotFather
2. **SECRET_KEY**: A random secret key for Flask

### How to Set Environment Variables

1. **In Vercel Dashboard**:

   - Go to your project
   - Click "Settings"
   - Click "Environment Variables"
   - Add each variable

2. **Via Vercel CLI**:
   ```bash
   vercel env add TELEGRAM_BOT_TOKEN
   vercel env add SECRET_KEY
   ```

## Step 4: Deploy

### Using Vercel CLI

```bash
# Deploy to production
vercel --prod

# Or deploy to preview
vercel
```

### Using GitHub Integration

1. **Push changes** to GitHub
2. **Vercel will auto-deploy**
3. **Check deployment status** in Vercel dashboard

## Step 5: Update Bot Configuration

After deployment, update your bot configuration:

1. **Get your Vercel URL** (e.g., `https://your-app.vercel.app`)
2. **Update `config.py`**:

   ```python
   FLASK_BASE_URL = "https://your-app.vercel.app"
   ```

3. **Update `telegram_bot.py`**:
   ```python
   FLASK_BASE_URL = "https://your-app.vercel.app"
   ```

## Step 6: Test the Deployment

1. **Test the web interface**:

   - Visit your Vercel URL
   - Try uploading a file ID

2. **Test the bot**:
   - Send a video to your bot
   - Check if streaming URLs work

## Vercel-Specific Features

### ✅ What Works on Vercel

- ✅ **Web interface** - Full functionality
- ✅ **API endpoints** - All endpoints work
- ✅ **Video streaming** - Proxies Telegram files
- ✅ **VLC streaming** - Compatible with VLC
- ✅ **File uploads** - Via web interface
- ✅ **Stream management** - List and manage streams

### ⚠️ Limitations

- ⚠️ **No file storage** - Uses in-memory storage
- ⚠️ **Streams reset** - On serverless function restart
- ⚠️ **Timeout limits** - 30-second function timeout
- ⚠️ **Memory limits** - 1024MB per function

### 🔧 Optimizations

1. **Use `app_vercel.py`** instead of `app.py`
2. **Set proper timeouts** in `vercel.json`
3. **Use environment variables** for configuration
4. **Enable caching** for better performance

## Configuration Files

### vercel.json

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app_vercel.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app_vercel.py"
    }
  ],
  "env": {
    "PYTHONPATH": "."
  },
  "functions": {
    "app_vercel.py": {
      "maxDuration": 30
    }
  }
}
```

### requirements-vercel.txt

```
flask==2.3.3
requests==2.31.0
python-dotenv==1.0.0
werkzeug==2.3.7
```

## Troubleshooting

### Common Issues

1. **"Function timeout"**:

   - Reduce video file size
   - Use smaller chunks
   - Increase timeout in `vercel.json`

2. **"Memory limit exceeded"**:

   - Use smaller files
   - Optimize streaming
   - Use external storage

3. **"Environment variable not found"**:

   - Check Vercel dashboard
   - Redeploy after adding variables
   - Use `vercel env ls` to verify

4. **"Bot not responding"**:
   - Check bot token
   - Verify webhook URL
   - Test bot manually

### Debug Mode

Enable debug logging:

```python
# In app_vercel.py
app.run(debug=True)
```

### Logs

Check Vercel logs:

```bash
vercel logs
```

## Production Considerations

### Security

1. **Use HTTPS** (automatic on Vercel)
2. **Set strong SECRET_KEY**
3. **Validate file types**
4. **Rate limiting**

### Performance

1. **Use CDN** for static files
2. **Enable caching**
3. **Optimize images**
4. **Monitor usage**

### Monitoring

1. **Set up alerts**
2. **Monitor errors**
3. **Track usage**
4. **Performance metrics**

## Alternative Deployment

If Vercel doesn't meet your needs, consider:

1. **Railway** - Similar to Vercel
2. **Render** - Good for Python apps
3. **Heroku** - Traditional hosting
4. **DigitalOcean** - VPS hosting

## Support

For deployment issues:

1. **Check Vercel logs**
2. **Verify environment variables**
3. **Test locally first**
4. **Check bot token validity**

---

**🎉 Your Telegram Video Streamer is now deployed on Vercel!**
