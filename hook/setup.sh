#!/bin/bash

# GitLab to Azure DevOps Sync Server Setup Script

echo "🚀 Setting up GitLab to Azure DevOps Sync Server..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or later."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate
echo "✅ Virtual environment activated"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before running the server"
fi

# Create work directory
mkdir -p sync_workspace

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your GitLab and Azure DevOps configuration"
echo "2. Run the server with: python server.py"
echo "3. Configure GitLab webhook to point to: http://your-server:5000/webhook/gitlab"
echo ""
echo "For Docker deployment:"
echo "1. Edit .env file with your configuration"
echo "2. Run: docker-compose up -d"
