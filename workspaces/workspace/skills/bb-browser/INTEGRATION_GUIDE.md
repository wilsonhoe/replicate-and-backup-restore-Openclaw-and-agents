# bb-browser Integration Guide for OpenClaw

## Overview
bb-browser is a powerful browser automation tool that turns your browser into an API. It allows AI agents to use your real browser with your login state, bypassing anti-bot measures and accessing websites as if they were you.

## 🔧 Installation Status
- ✅ **bb-browser CLI**: Installed (v0.10.1)
- ✅ **Site Adapters**: 106 community adapters installed
- ⚠️ **Browser Connection**: Needs Chrome running with extension

## 📋 Available Platforms (36 total, 103 commands)

### Search & Information
- **Google**, **Baidu**, **Bing**, **DuckDuckGo** - Web search
- **arxiv** - Academic paper search
- **wikipedia** - Encyclopedia summaries
- **stackoverflow** - Developer Q&A

### Social Media
- **Twitter/X** - Tweets, search, threads, bookmarks
- **Reddit** - Posts, comments, hot content
- **Weibo** - Chinese social media
- **Zhihu** - Chinese Q&A platform
- **Xiaohongshu** - Chinese lifestyle platform
- **LinkedIn** - Professional networking

### Video Platforms
- **YouTube** - Videos, transcripts, comments, search
- **Bilibili** - Chinese video platform

### Development
- **GitHub** - Repository info, issues, user data
- **npm**, **PyPI** - Package search
- **Dev.to** - Developer articles
- **HackerNews** - Tech news

### Finance
- **Xueqiu** - Chinese investment platform
- **Eastmoney** - Chinese financial data
- **Yahoo Finance** - Stock quotes

### Entertainment
- **Douban** - Movies, books, music
- **IMDb** - Movie database

### News
- **BBC**, **Reuters**, **36kr**, **Toutiao** - News headlines

## 🚀 Quick Start

### 1. Start Chrome with Remote Debugging
```bash
# Start Chrome with remote debugging enabled
# Option 1: New Chrome instance
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile

# Option 2: Attach to existing Chrome (if Chrome is already running)
# Kill existing Chrome first, then restart with debugging:
pkill chrome
google-chrome --remote-debugging-port=9222
```

### 2. Install the Browser Extension
```bash
# Load the extension in Chrome
# 1. Open Chrome and go to: chrome://extensions/
# 2. Enable "Developer mode" (toggle in top right)
# 3. Click "Load unpacked"
# 4. Select the folder: /home/wls/Downloads/bb-browser-extension-bb-browser-v0.10.0/
# 5. Extension should now be active
```

### 3. Test Basic Functionality
```bash
# Test with OpenClaw integration
bb-browser site list | head -10

# Test a simple search
bb-browser site twitter/search "AI agent" 5

# Get trending stocks
bb-browser site xueqiu/hot-stock 10
```

## 🎯 Integration with OpenClaw

### Using the Python Integration
```python
# Import the integration
from skills.bb-browser.bb_integration_updated import (
    search_platform, get_trending_content, get_hot_stocks,
    cross_platform_research, get_github_repo_info
)

# Search Twitter for AI agents
results = search_platform('twitter', 'AI agent', 5)

# Get trending Reddit posts
reddit_hot = get_trending_content('reddit', 10)

# Cross-platform research on a topic
research = cross_platform_research('retrieval augmented generation')

# Get GitHub repository info
repo_info = get_github_repo_info('openclaw/openclaw')
```

### Browser Automation Commands
```python
# Advanced browser automation
from skills.bb-browser.bb_integration_updated import (
    take_screenshot, get_page_info, extract_links
)

# Take screenshot of a page
screenshot = take_screenshot('https://example.com', full_page=True)

# Get page information
page_info = get_page_info('https://example.com')

# Extract all links
links = extract_links('https://example.com')
```

## 💡 Use Cases for Your Business

### 1. Market Research
```python
# Research real estate trends
real_estate_trends = search_platform('zhihu', '新加坡房地产趋势', 10)

# Monitor competitor activity
competitor_posts = search_platform('xiaohongshu', '新加坡房产投资', 5)

# Track financial news
finance_news = get_news_headlines('36kr', '房地产')
```

### 2. Investment Research
```python
# Get hot stocks
hot_stocks = get_hot_stocks(20)

# Research specific stocks
stock_info = get_stock_info('AAPL')

# Get market sentiment
market_chatter = search_platform('twitter', 'real estate investment Singapore', 10)
```

### 3. Content & Social Media
```python
# Research content topics
content_ideas = search_platform('youtube', 'real estate tips', 10)

# Monitor trending topics
trending = get_trending_content('weibo', 10)

# Get video transcripts for research
transcript = get_youtube_transcript('VIDEO_ID_HERE')
```

### 4. Technical Research
```python
# Research automation tools
automation_tools = search_platform('stackoverflow', 'real estate automation', 10)

# Get latest papers
papers = search_platform('arxiv', 'property management AI', 5)

# Research development trends
dev_trends = get_trending_content('hackernews', 10)
```

## 🔧 Advanced Configuration

### Custom CDP Port
```bash
# If Chrome is running on a different port
bb-browser --port 9223 site twitter/search "AI"
```

### Multi-tab Operations
```bash
# Use specific tab ID for concurrent operations
bb-browser --tab 1 site twitter/search "AI"
bb-browser --tab 2 site reddit/hot
```

### JSON Output with Filtering
```bash
# Get structured data with jq filtering
bb-browser site xueqiu/hot-stock 5 --json --jq '.items[] | {name, changePercent}'
```

### Browser Automation
```bash
# Direct browser control
bb-browser open https://example.com
bb-browser eval "document.title"
bb-browser click @3  # Click element by index
bb-browser fill @5 "hello world"  # Fill input field
bb-browser screenshot --full-page
```

## ⚠️ Important Notes

### Security & Privacy
- **Your Login State**: bb-browser uses your actual browser cookies and login state
- **Be Careful**: AI agents can access any website you're logged into
- **Permissions**: Extension has broad permissions (`<all_urls>`)
- **Monitoring**: Review what commands are being executed

### Rate Limits & Ethics
- **Respect Rate Limits**: Don't hammer websites with requests
- **Follow Terms of Service**: Some platforms prohibit automated access
- **Use Responsibly**: Don't use for spam or malicious purposes

### Technical Requirements
- **Chrome/Chromium**: Required for the extension
- **Node.js**: Required for bb-browser CLI
- **Network Access**: Extension needs internet connectivity

## 🚨 Troubleshooting

### Common Issues

1. **"Could not start browser"**
   ```bash
   # Chrome not running with debugging
   google-chrome --remote-debugging-port=9222
   ```

2. **"Extension not working"**
   - Check extension is loaded in chrome://extensions/
   - Verify extension has necessary permissions
   - Check browser console for errors

3. **"Command not found"**
   - Ensure bb-browser is installed: `npm list -g bb-browser`
   - Try reinstalling: `npm install -g bb-browser`

4. **"Rate limited"**
   - Add delays between requests
   - Use different user agents if needed
   - Respect website rate limits

### Getting Help
```bash
# Check bb-browser help
bb-browser --help
bb-browser site --help

# Test connection
bb-browser --version
bb-browser site list | head -5
```

## 🎉 Next Steps

1. **Install Extension**: Load the extension in Chrome
2. **Start Chrome**: Run Chrome with debugging port
3. **Test Commands**: Try a few basic commands
4. **Integrate with Ontology**: Store research results in your knowledge graph
5. **Build Workflows**: Create automated research and monitoring workflows

The bb-browser skill is now ready to give your AI agents access to the entire internet through your real browser! 🌐