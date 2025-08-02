#!/bin/bash

# Vercel Deployment Script for Telegram Video Streamer

echo "🚀 Deploying to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Check if user is logged in
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please login to Vercel..."
    vercel login
fi

# Set environment variables
echo "🔧 Setting environment variables..."
vercel env add TELEGRAM_BOT_TOKEN
vercel env add SECRET_KEY

# Deploy to Vercel
echo "🌐 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo "📱 Your bot should now work with the Vercel deployment"
echo "🌐 Check your Vercel dashboard for the deployment URL" 