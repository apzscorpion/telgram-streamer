# 🔐 GitHub Authentication & Deployment Guide

## Current Status

✅ **Repository**: [https://github.com/apzscorpion/telgram-streamer](https://github.com/apzscorpion/telgram-streamer)  
✅ **Local Code**: Ready to push  
❌ **Authentication**: Need to set up GitHub access

## Step 1: GitHub Authentication

You need to authenticate with GitHub to push your code. Choose one of these methods:

### Method 1: Personal Access Token (Recommended)

1. **Go to GitHub Settings**:

   - Visit [https://github.com/settings/tokens](https://github.com/settings/tokens)
   - Click **"Generate new token (classic)"**
   - Give it a name like "Telegram Streamer Bot"
   - Select scopes: `repo`, `workflow`
   - Click **"Generate token"**
   - **Copy the token** (you won't see it again!)

2. **Use the token**:
   ```bash
   # When prompted for password, use the token instead
   git push -u origin main
   ```

### Method 2: GitHub CLI

```bash
# Install GitHub CLI
brew install gh

# Login to GitHub
gh auth login

# Then push
git push -u origin main
```

### Method 3: SSH Key

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to GitHub
# Copy the public key and add it to GitHub Settings > SSH Keys

# Change remote to SSH
git remote set-url origin git@github.com:apzscorpion/telgram-streamer.git

# Push
git push -u origin main
```

## Step 2: Push Code to GitHub

After setting up authentication:

```bash
# Push your code
git push -u origin main
```

## Step 3: Verify Upload

1. **Visit your repository**: [https://github.com/apzscorpion/telgram-streamer](https://github.com/apzscorpion/telgram-streamer)
2. **Check that these files are uploaded**:
   - ✅ `app_vercel.py`
   - ✅ `vercel.json`
   - ✅ `requirements-vercel.txt`
   - ✅ `templates/index.html`
   - ✅ `config.py`
   - ✅ `telegram_bot_improved.py`

## Step 4: Deploy to Vercel

After pushing to GitHub:

### Option A: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### Option B: GitHub Integration

1. **Go to [vercel.com](https://vercel.com)**
2. **Click "New Project"**
3. **Import your GitHub repository**: `apzscorpion/telgram-streamer`
4. **Configure settings**:
   - Framework Preset: `Other`
   - Build Command: Leave empty
   - Output Directory: Leave empty
   - Install Command: `pip install -r requirements-vercel.txt`
5. **Click "Deploy"**

## Step 5: Set Environment Variables

After deployment, set these in Vercel:

```
TELEGRAM_BOT_TOKEN = 8445456449:AAGE0BaW2pSxJf7t4j5wb0Q09KRPItienPA
SECRET_KEY = your-random-secret-key-here
```

## Step 6: Update Configuration

After getting your Vercel URL:

1. **Update `config.py`**:

   ```python
   FLASK_BASE_URL = "https://your-app-name.vercel.app"
   ```

2. **Push the update**:
   ```bash
   git add config.py
   git commit -m "Update for Vercel deployment"
   git push
   ```

## Troubleshooting

### "Permission denied" Error

- Make sure you're using the correct GitHub account
- Check that you have access to the repository
- Verify your authentication method

### "Repository not found" Error

- Check the repository URL
- Make sure the repository exists
- Verify your GitHub username

### "Authentication failed" Error

- Try using a Personal Access Token
- Check your SSH key setup
- Verify your GitHub CLI login

## Quick Commands

```bash
# Set up authentication (choose one method above)
# Then push to GitHub
git push -u origin main

# Deploy to Vercel
npm install -g vercel
vercel login
vercel --prod

# Update configuration
# Edit config.py with Vercel URL
git add config.py
git commit -m "Update for Vercel deployment"
git push
```

---

**🎉 After completing these steps, your bot will be live on Vercel!**
