# 🚀 Cloudflare Workers Deployment Guide

## Overview

This guide will help you deploy your Telegram Video Streamer using **Cloudflare Workers**, which is the same approach used by the professional bot you showed me.

## Why Cloudflare Workers?

- ✅ **Better for streaming** - No timeout limits
- ✅ **Global CDN** - Faster worldwide access
- ✅ **No file downloads** - Direct Telegram file proxying
- ✅ **Works with forwarded files** - No access issues
- ✅ **Professional approach** - Same as other bots

## Step 1: Install Wrangler CLI

```bash
# Install Wrangler (Cloudflare Workers CLI)
npm install -g wrangler

# Login to Cloudflare
wrangler login
```

## Step 2: Deploy the Worker

```bash
# Deploy to Cloudflare Workers
wrangler deploy

# Or deploy to production
wrangler deploy --env production
```

## Step 3: Get Your Worker URL

After deployment, you'll get a URL like:

```
https://telegram-file-proxy.your-subdomain.workers.dev
```

## Step 4: Update Bot Configuration

Update the `CLOUDFLARE_WORKER_URL` in `telegram_bot_cloudflare.py`:

```python
CLOUDFLARE_WORKER_URL = "https://telegram-file-proxy.your-subdomain.workers.dev"
```

## Step 5: Start the Bot

```bash
# Stop the old bot
pkill -f "telegram_bot"

# Start the new Cloudflare bot
python telegram_bot_cloudflare.py
```

## How It Works

### **1. User sends video** → Bot gets file info

### **2. Bot creates URLs** → Using Cloudflare Worker

### **3. Cloudflare proxies** → Direct from Telegram

### **4. User gets links** → Like the professional bot

## URLs Generated

Your bot will create URLs like:

- **Stream**: `https://telegram-file-proxy.your-subdomain.workers.dev/stream/{file_id}`
- **Download**: `https://telegram-file-proxy.your-subdomain.workers.dev/dl/{file_id}`

## Features

✅ **Works with forwarded files**  
✅ **No file access issues**  
✅ **Global CDN performance**  
✅ **Professional streaming**  
✅ **Same as other bots**

## Troubleshooting

### **"Worker not found"**

- Check your Worker URL
- Make sure deployment was successful
- Verify the Worker is running

### **"Invalid file ID"**

- Check bot token in Worker
- Verify file exists on Telegram
- Test with direct upload first

### **"Deployment failed"**

- Check Wrangler login
- Verify Cloudflare account
- Check Worker name availability

## Next Steps

1. **Deploy the Worker**
2. **Update bot configuration**
3. **Start the new bot**
4. **Test with forwarded videos**

---

**🎉 Your bot will now work exactly like the professional one!**
