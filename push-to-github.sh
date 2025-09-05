#!/bin/bash

# Script to push RAG Knowledge Base to GitHub
# Run this after creating the repository on GitHub.com

echo "🚀 Pushing RAG Knowledge Base to GitHub..."
echo "=========================================="

# Add the GitHub remote (replace YOUR_USERNAME with your actual GitHub username)
echo "📝 Adding GitHub remote..."
git remote add origin https://github.com/YOUR_USERNAME/rag-knowledge-base.git

# Push to GitHub
echo "📤 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "✅ Successfully pushed to GitHub!"
echo "🌐 Your repository is now available at: https://github.com/YOUR_USERNAME/rag-knowledge-base"
echo ""
echo "📋 Next steps:"
echo "1. Replace 'YOUR_USERNAME' in the commands above with your actual GitHub username"
echo "2. Run this script: bash push-to-github.sh"
echo "3. Or run the commands manually:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/rag-knowledge-base.git"
echo "   git branch -M main"
echo "   git push -u origin main"