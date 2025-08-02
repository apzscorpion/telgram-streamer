#!/bin/bash

# GitHub Setup Script for Telegram Video Streamer

echo "🚀 Setting up GitHub repository..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Initialize git repository
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
fi

# Create .gitignore file
echo "📝 Creating .gitignore file..."
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Environment variables
.env

# Uploads (temporary files)
uploads/
*.mp4
*.avi
*.mov
*.mkv

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp
EOF

# Add all files
echo "📁 Adding files to git..."
git add .

# Initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Telegram Video Streamer Bot"

echo ""
echo "✅ Local git repository is ready!"
echo ""
echo "📋 Next steps:"
echo "1. Create a new repository on GitHub:"
echo "   - Go to https://github.com"
echo "   - Click 'New repository'"
echo "   - Name it 'telegram-streamer' (or your preferred name)"
echo "   - Don't initialize with README (we already have one)"
echo "   - Click 'Create repository'"
echo ""
echo "2. Connect to your GitHub repository:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/telegram-streamer.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Replace YOUR_USERNAME with your actual GitHub username"
echo ""
echo "4. After pushing to GitHub, you can deploy to Vercel!" 