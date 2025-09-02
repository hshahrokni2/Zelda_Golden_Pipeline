#!/bin/bash
# Push Golden Orchestrator Pipeline to GitHub

echo "📦 PUSHING GOLDEN ORCHESTRATOR TO GITHUB"
echo "========================================"

# Check if remote exists
if git remote | grep -q "origin"; then
    echo "Remote 'origin' exists"
else
    echo "Adding GitHub remote..."
    echo "Please enter your GitHub repository URL:"
    echo "Example: git@github.com:yourusername/Golden_Orchestrator_Pipeline.git"
    read -p "GitHub URL: " GITHUB_URL
    git remote add origin "$GITHUB_URL"
fi

# Show current status
echo ""
echo "📊 Current Git Status:"
git status --short

echo ""
echo "📝 Recent commits:"
git log --oneline -5

echo ""
echo "🔗 Remote configuration:"
git remote -v

echo ""
echo "========================================"
echo "Ready to push to GitHub?"
echo "This will push the master branch to origin"
read -p "Continue? (y/n): " CONFIRM

if [ "$CONFIRM" = "y" ] || [ "$CONFIRM" = "Y" ]; then
    echo "🚀 Pushing to GitHub..."
    git push -u origin master
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ SUCCESS! Golden Orchestrator Pipeline pushed to GitHub"
        echo ""
        echo "Next steps:"
        echo "1. Check your GitHub repository"
        echo "2. Add README if needed"
        echo "3. Set up GitHub Actions for CI/CD if desired"
    else
        echo ""
        echo "❌ Push failed. Please check:"
        echo "1. GitHub repository exists"
        echo "2. You have push permissions"
        echo "3. SSH keys are configured"
        echo ""
        echo "To create a new repository:"
        echo "1. Go to https://github.com/new"
        echo "2. Name it 'Golden_Orchestrator_Pipeline'"
        echo "3. Don't initialize with README"
        echo "4. Run this script again"
    fi
else
    echo "Push cancelled"
fi