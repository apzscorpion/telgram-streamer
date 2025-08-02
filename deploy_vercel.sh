#!/bin/bash

echo "🚀 Deploying Telegram Bot to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Deploy to Vercel
echo "📦 Deploying to Vercel..."
vercel --prod

# Get the deployment URL
DEPLOYMENT_URL=$(vercel ls --prod | grep -o 'https://[^[:space:]]*' | head -1)

if [ -n "$DEPLOYMENT_URL" ]; then
    echo "✅ Deployment successful!"
    echo "🌐 Your bot is deployed at: $DEPLOYMENT_URL"
    
    # Set webhook
    echo "🔗 Setting up webhook..."
    curl -X POST "$DEPLOYMENT_URL/set-webhook"
    
    echo ""
    echo "🎉 Bot deployment complete!"
    echo "📱 Your bot is now running on Vercel"
    echo "🔗 Webhook URL: $DEPLOYMENT_URL/webhook"
    echo ""
    echo "To check webhook status, visit: $DEPLOYMENT_URL/get-webhook-info"
else
    echo "❌ Deployment failed or URL not found"
    exit 1
fi 