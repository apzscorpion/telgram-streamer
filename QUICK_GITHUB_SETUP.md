# 🚀 Quick GitHub Setup

## **Step 1: Get GitHub Personal Access Token**

1. **Go to**: [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. **Click**: "Generate new token (classic)"
3. **Name**: "Telegram Streamer Bot"
4. **Select scopes**:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
5. **Click**: "Generate token"
6. **Copy the token** (you won't see it again!)

## **Step 2: Push to GitHub**

After you get the token, run this command:

```bash
git push -u origin main
```

When prompted:

- **Username**: `apzscorpion`
- **Password**: Use the token you just created (not your GitHub password)

## **Step 3: Verify Upload**

1. **Visit**: [https://github.com/apzscorpion/telgram-streamer](https://github.com/apzscorpion/telgram-streamer)
2. **Check that these files are uploaded**:
   - ✅ `app_vercel.py`
   - ✅ `vercel.json`
   - ✅ `requirements-vercel.txt`
   - ✅ `telegram_bot_improved.py`
   - ✅ `config.py`
   - ✅ `templates/index.html`

## **Step 4: Deploy to Vercel**

After pushing to GitHub:

1. **Go to**: [https://vercel.com](https://vercel.com)
2. **Click**: "New Project"
3. **Import**: `apzscorpion/telgram-streamer`
4. **Configure**:
   - Framework Preset: `Other`
   - Build Command: Leave empty
   - Output Directory: Leave empty
   - Install Command: `pip install -r requirements-vercel.txt`
5. **Click**: "Deploy"

## **Step 5: Set Environment Variables**

In Vercel dashboard, add these environment variables:

```
TELEGRAM_BOT_TOKEN = 8445456449:AAGE0BaW2pSxJf7t4j5wb0Q09KRPItienPA
SECRET_KEY = your-random-secret-key-here
```

## **Step 6: Update Configuration**

After getting your Vercel URL:

1. **Edit `config.py`**:

   ```python
   FLASK_BASE_URL = "https://your-app-name.vercel.app"
   ```

2. **Push the update**:
   ```bash
   git add config.py
   git commit -m "Update for Vercel deployment"
   git push
   ```

---

**🎉 That's it! Your bot will be live on Vercel!**
