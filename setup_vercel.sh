#!/bin/bash

echo "🚀 Setting up Telegram Bot for Vercel Deployment..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js first:"
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install npm first."
    exit 1
fi

# Install Vercel CLI if not installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Check if user is logged in to Vercel
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please login to Vercel..."
    vercel login
fi

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Run: ./deploy_vercel.sh"
echo "2. Set your BOT_TOKEN environment variable"
echo "3. Set your CLOUDFLARE_WORKER_URL environment variable"
echo ""
echo "📖 For detailed instructions, see: VERCEL_DEPLOYMENT.md" 