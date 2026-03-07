#!/bin/bash
# Build script for Frontend - Run this before deploying to Plesk

echo "🔨 Building Frontend for Production..."

cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Build the frontend
echo "🏗️  Building React application..."
npm run build

echo "✅ Frontend build completed!"
echo "📁 Build output is in: frontend/dist"
echo ""
echo "Next steps:"
echo "1. Upload the 'dist' folder contents to your Plesk domain's httpdocs/frontend/dist"
echo "2. Make sure .htaccess files are in place"
echo "3. Configure your domain settings in Plesk"
