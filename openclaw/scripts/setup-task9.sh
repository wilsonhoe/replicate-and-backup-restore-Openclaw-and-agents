#!/bin/bash
# Task #9 Setup Script
# Lisa Email & Browser Session Setup

set -e

echo "=========================================="
echo "Task #9: Email & Browser Session Setup"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check Prerequisites
echo "Step 1: Checking Prerequisites..."

if ! command -v google-chrome &> /dev/null; then
    echo -e "${RED}❌ Chrome not found${NC}"
    echo "Install Chrome: sudo apt install google-chrome-stable"
    exit 1
fi

if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo -e "${RED}❌ Ollama not running${NC}"
    echo "Start Ollama: ollama serve"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites met${NC}"
echo ""

# Step 2: Create Directories
echo "Step 2: Creating Directories..."
mkdir -p /home/wls/.openclaw/{sessions,config,lib,scripts}
echo -e "${GREEN}✅ Directories created${NC}"
echo ""

# Step 3: Check Chrome CDP
echo "Step 3: Checking Chrome CDP..."
if ! curl -s http://localhost:9222/json/version > /dev/null; then
    echo -e "${YELLOW}⚠️ Chrome CDP not running${NC}"
    echo "Starting Chrome with debugging..."

    google-chrome \
        --remote-debugging-port=9222 \
        --no-first-run \
        --user-data-dir=/home/wls/.chrome-lisa \
        --disable-extensions \
        --window-size=1920,1080 \
        &

    sleep 3

    if curl -s http://localhost:9222/json/version > /dev/null; then
        echo -e "${GREEN}✅ Chrome CDP started${NC}"
    else
        echo -e "${RED}❌ Failed to start Chrome CDP${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Chrome CDP already running${NC}"
fi
echo ""

# Step 4: Install Dependencies
echo "Step 4: Installing Dependencies..."
cd /home/wls/.openclaw

if [ ! -d "node_modules" ]; then
    npm init -y
fi

npm install playwright nodemailer

echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# Step 5: Environment Variables Check
echo "Step 5: Checking Environment Variables..."

missing_vars=0

if [ -z "$TWITTER_USERNAME" ]; then
    echo -e "${YELLOW}⚠️ TWITTER_USERNAME not set${NC}"
    missing_vars=$((missing_vars + 1))
fi

if [ -z "$TWITTER_PASSWORD" ]; then
    echo -e "${YELLOW}⚠️ TWITTER_PASSWORD not set${NC}"
    missing_vars=$((missing_vars + 1))
fi

if [ -z "$LINKEDIN_USERNAME" ]; then
    echo -e "${YELLOW}⚠️ LINKEDIN_USERNAME not set${NC}"
    missing_vars=$((missing_vars + 1))
fi

if [ -z "$LINKEDIN_PASSWORD" ]; then
    echo -e "${YELLOW}⚠️ LINKEDIN_PASSWORD not set${NC}"
    missing_vars=$((missing_vars + 1))
fi

if [ -z "$GMAIL_USER" ]; then
    echo -e "${YELLOW}⚠️ GMAIL_USER not set${NC}"
    missing_vars=$((missing_vars + 1))
fi

if [ -z "$GMAIL_APP_PASSWORD" ]; then
    echo -e "${YELLOW}⚠️ GMAIL_APP_PASSWORD not set${NC}"
    missing_vars=$((missing_vars + 1))
fi

if [ $missing_vars -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}⚠️ $missing_vars environment variables missing${NC}"
    echo "Set them in your .env file:"
    echo "  export TWITTER_USERNAME=your_username"
    echo "  export TWITTER_PASSWORD=your_password"
    echo "  export LINKEDIN_USERNAME=your_email"
    echo "  export LINKEDIN_PASSWORD=your_password"
    echo "  export GMAIL_USER=lisa.openclaw@gmail.com"
    echo "  export GMAIL_APP_PASSWORD=your_16_char_app_password"
    echo ""
fi

echo -e "${GREEN}✅ Environment check complete${NC}"
echo ""

# Step 6: Summary
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Set environment variables in ~/.env"
echo "2. Source the file: source ~/.env"
echo "3. Test email: node scripts/test-email.js"
echo "4. Test browser: node scripts/test-browser-sessions.js"
echo ""
echo "Configuration files:"
echo "  - /home/wls/.openclaw/config/email-setup.md"
echo "  - /home/wls/.openclaw/config/browser-session-setup.md"
echo ""
echo -e "${GREEN}✅ Task #9 setup complete!${NC}"
