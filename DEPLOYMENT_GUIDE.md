# 🚀 Complete Deployment Guide: GitHub → Vercel

## Overview

This guide will help you deploy your Telegram Video Streamer Bot to Vercel via GitHub.

## Step 1: Create GitHub Repository

### 1.1 Go to GitHub

- Visit [https://github.com](https://github.com)
- Sign in to your account (or create one if needed)

### 1.2 Create New Repository

- Click the **"+"** icon in the top right
- Select **"New repository"**
- Fill in the details:
  - **Repository name**: `telegram-streamer` (or your preferred name)
  - **Description**: `Telegram Video Streamer Bot - Convert videos to streaming URLs`
  - **Visibility**: Choose Public or Private
  - **DO NOT** check "Add a README file" (we already have one)
  - **DO NOT** check "Add .gitignore" (we already have one)
- Click **"Create repository"**

### 1.3 Copy Repository URL

After creating the repository, copy the URL. It will look like:

```
https://github.com/YOUR_USERNAME/telegram-streamer.git
```

## Step 2: Push Code to GitHub

### 2.1 Connect to Your Repository

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
# Connect to your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/telegram-streamer.git

# Set the main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

### 2.2 Verify Upload

- Go to your GitHub repository page
- You should see all your files uploaded
- Check that these files are present:
  - `app_vercel.py`
  - `vercel.json`
  - `requirements-vercel.txt`
  - `templates/index.html`
  - `config.py`

## Step 3: Deploy to Vercel

### 3.1 Install Vercel CLI

```bash
# Install Vercel CLI globally
npm install -g vercel
```

### 3.2 Login to Vercel

```bash
# Login to your Vercel account
vercel login
```

### 3.3 Deploy to Vercel

```bash
# Deploy to Vercel
vercel --prod
```

### 3.4 Set Environment Variables

After deployment, set these environment variables in Vercel:

1. **Go to Vercel Dashboard**
2. **Select your project**
3. **Go to Settings → Environment Variables**
4. **Add these variables:**

```
TELEGRAM_BOT_TOKEN = 8445456449:AAGE0BaW2pSxJf7t4j5wb0Q09KRPItienPA
SECRET_KEY = your-random-secret-key-here
```

## Step 4: Update Bot Configuration

### 4.1 Get Your Vercel URL

After deployment, Vercel will give you a URL like:

```
https://your-app-name.vercel.app
```

### 4.2 Update Configuration

Update your `config.py` with the Vercel URL:

```python
# Update this line in config.py
FLASK_BASE_URL = "https://your-app-name.vercel.app"
```

### 4.3 Push Updated Configuration

```bash
# Commit and push the updated configuration
git add config.py
git commit -m "Update Flask URL for Vercel deployment"
git push
```

## Step 5: Test Your Deployment

### 5.1 Test Web Interface

- Visit your Vercel URL: `https://your-app-name.vercel.app`
- Try uploading a file ID
- Check if streaming works

### 5.2 Test Bot Locally

```bash
# Start the bot locally to test with Vercel
./restart_bot.sh
```

### 5.3 Test Bot Features

1. **Send a video** to @MHStreamsBot
2. **Forward a video** to @MHStreamsBot
3. **Send a video URL** to @MHStreamsBot
4. **Mention the bot** in a group with a video

## Troubleshooting

### Common Issues

#### 1. "Repository not found"

- Check your GitHub username
- Make sure the repository exists
- Verify the repository URL

#### 2. "Permission denied"

- Make sure you're logged into GitHub
- Check if you have access to the repository

#### 3. "Environment variables not found"

- Go to Vercel dashboard
- Add the environment variables
- Redeploy the project

#### 4. "Bot not responding"

- Check if the bot is running locally
- Verify the bot token is correct
- Test with a simple video first

### Debug Commands

```bash
# Check git status
git status

# Check remote repository
git remote -v

# Check Vercel deployment
vercel ls

# Check environment variables
vercel env ls
```

## Alternative: Deploy via GitHub Integration

### 1. Connect GitHub to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click **"New Project"**
3. Import your GitHub repository
4. Configure the settings

### 2. Set Environment Variables

1. Go to your project settings
2. Add environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `SECRET_KEY`

### 3. Deploy

1. Vercel will automatically deploy
2. Get your deployment URL
3. Update bot configuration

## Final Steps

### 1. Update Bot for Production

```bash
# Update config.py with Vercel URL
# Push changes to GitHub
git add config.py
git commit -m "Update for production deployment"
git push
```

### 2. Test Everything

- ✅ Web interface works
- ✅ Bot responds to messages
- ✅ Streaming URLs work
- ✅ VLC streaming works

### 3. Monitor Usage

- Check Vercel dashboard for logs
- Monitor bot usage
- Check for any errors

## 🎉 Success!

Your Telegram Video Streamer Bot is now deployed and should work with:

- ✅ Direct video uploads
- ✅ Forwarded videos (with limitations)
- ✅ Video URLs
- ✅ Group mentions
- ✅ Browser streaming
- ✅ VLC streaming

---

**Your bot is ready for production use! 🚀**
