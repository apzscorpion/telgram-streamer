# 🚀 Deploy Bot to Railway (No Local Machine Needed)

## Why Railway?

- ✅ **Runs 24/7** - No local machine needed
- ✅ **Auto-restart** - If bot crashes, it restarts
- ✅ **Free tier** - 500 hours/month free
- ✅ **Easy deployment** - Just connect GitHub
- ✅ **Environment variables** - Secure bot token storage

## Step 1: Deploy to Railway

### **Option A: Railway CLI**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy your project
railway up
```

### **Option B: Railway Dashboard**

1. **Go to**: [railway.app](https://railway.app)
2. **Sign up/Login** with GitHub
3. **Click**: "New Project"
4. **Select**: "Deploy from GitHub repo"
5. **Choose**: Your `telgram-streamer` repository
6. **Railway will auto-deploy**

## Step 2: Set Environment Variables

In Railway dashboard, add these variables:

```
BOT_TOKEN = 8445456449:AAGE0BaW2pSxJf7t4j5wb0Q09KRPItienPA
BOT_USERNAME = MHStreamsBot
CLOUDFLARE_WORKER_URL = https://your-worker-url.workers.dev
```

## Step 3: Update Cloudflare Worker URL

Update `telegram_bot_cloudflare.py` with your actual Cloudflare Worker URL:

```python
CLOUDFLARE_WORKER_URL = "https://your-actual-worker-url.workers.dev"
```

## Step 4: Deploy Updated Code

```bash
git add .
git commit -m "Add Railway deployment"
git push
```

Railway will automatically redeploy.

## Step 5: Test Your Bot

Your bot will now:

- ✅ **Run 24/7** on Railway
- ✅ **Auto-restart** if it crashes
- ✅ **No local machine** needed
- ✅ **Respond to messages** automatically

## 🎯 **Benefits**

### **Before (Local)**

- ❌ Need to run `python telegram_bot_cloudflare.py` manually
- ❌ Bot stops when you close terminal
- ❌ Bot stops when computer sleeps
- ❌ Need to restart manually

### **After (Railway)**

- ✅ Bot runs automatically
- ✅ Bot runs 24/7
- ✅ Auto-restart on crashes
- ✅ No local machine needed
- ✅ Professional deployment

## 📱 **Test Your Bot**

After Railway deployment:

1. **Send `/start`** to @MHStreamsBot
2. **Send a video** to test streaming
3. **Bot should respond** automatically

## 🔧 **Monitor Your Bot**

- **Railway Dashboard**: Check logs and status
- **Telegram**: Test bot responses
- **Cloudflare**: Monitor Worker performance

---

**🎉 Your bot will now run 24/7 without your local machine!**
