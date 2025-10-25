#!/bin/bash

# GoFormz-Shiftcare Integration Deployment Script for GitHub + Heroku

echo "GoFormz-Shiftcare Integration Deployment"
echo "========================================"

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "Error: Heroku CLI is not installed."
    echo "Please install it from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "Please log in to Heroku first:"
    heroku login
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git remote add origin https://github.com/shulmeister/goformz-automation.git
fi

# Get app name from user
read -p "Enter your Heroku app name (or press Enter to create a new one): " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "Creating new Heroku app..."
    APP_NAME=$(heroku create --region us | grep -o 'https://[^.]*\.herokuapp\.com' | sed 's/https:\/\///' | sed 's/\.herokuapp\.com//')
    echo "Created app: $APP_NAME"
fi

# Set environment variables
echo "Setting up environment variables..."
echo "You'll need to provide your GoFormz API credentials and Shiftcare login details."

read -p "GoFormz Client ID: " GOFORMZ_CLIENT_ID
read -p "GoFormz Client Secret: " GOFORMZ_CLIENT_SECRET
read -p "Shiftcare Username: " SHIFTCARE_USERNAME
read -s -p "Shiftcare Password: " SHIFTCARE_PASSWORD
echo

# Set Heroku config vars
heroku config:set GOFORMZ_CLIENT_ID="$GOFORMZ_CLIENT_ID" --app $APP_NAME
heroku config:set GOFORMZ_CLIENT_SECRET="$GOFORMZ_CLIENT_SECRET" --app $APP_NAME
heroku config:set SHIFTCARE_USERNAME="$SHIFTCARE_USERNAME" --app $APP_NAME
heroku config:set SHIFTCARE_PASSWORD="$SHIFTCARE_PASSWORD" --app $APP_NAME

# Add buildpack for Playwright
echo "Adding Playwright buildpack..."
heroku buildpacks:add --index 1 https://github.com/jontewks/puppeteer-heroku-buildpack.git --app $APP_NAME
heroku buildpacks:add --index 2 heroku/python --app $APP_NAME

# Commit and push to GitHub first
echo "Committing and pushing to GitHub..."
git add .
git commit -m "Deploy GoFormz-Shiftcare integration"
git push origin main

# Deploy to Heroku from GitHub
echo "Deploying to Heroku from GitHub..."
git push heroku main

echo "Deployment complete!"
echo "Your app is available at: https://$APP_NAME.herokuapp.com"
echo ""
echo "To test the integration:"
echo "1. Visit: https://$APP_NAME.herokuapp.com/health"
echo "2. Use the /process-packets endpoint to process forms"
echo ""
echo "To view logs:"
echo "heroku logs --tail --app $APP_NAME"
echo ""
echo "GitHub repository: https://github.com/shulmeister/goformz-automation"
