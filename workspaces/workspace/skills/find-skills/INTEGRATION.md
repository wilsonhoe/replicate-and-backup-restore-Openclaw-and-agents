# Find Skills Skill - Integration Guide

## Overview
The Find Skills Skill helps you discover and search for OpenClaw skills from various sources. Since the clawhub API is currently rate-limited, this implementation provides reference information and alternative search methods.

## Quick Usage

### 1. Browse Available Sources
```python
# Show all skill sources
python3 skills/find-skills/simple_reference.py
```

### 2. Get Popular Skills
```python
# Import the reference module
from skills.find-skills.simple_reference import get_popular_skills, get_skill_categories

# Get popular skills with descriptions
popular = get_popular_skills()
for skill, desc in popular:
    print(f"{skill}: {desc}")

# Get skills by category
categories = get_skill_categories()
for category, skills in categories.items():
    print(f"{category}: {', '.join(skills)}")
```

### 3. Manual Search (When Rate Limited)
When clawhub hits rate limits, use these direct methods:

#### Browse Websites:
- **Primary**: https://clawhub.ai
- **Directory**: https://www.openclawdirectory.dev/skills
- **LobeHub**: https://lobehub.com/skills

#### Search GitHub:
```bash
# Search for OpenClaw skills on GitHub
gh search repos "openclaw skill" --sort stars
gh search repos "agent-skill" --sort updated
```

#### Community Resources:
- **Discord**: https://discord.com/invite/clawd
- **Forums**: https://www.sitepoint.com/community/

## Installation Commands

### Standard Installation:
```bash
npx clawhub@latest install <skill-name>
```

### When Rate Limited - Manual Installation:
```bash
# 1. Find skill on GitHub
git clone https://github.com/<author>/<skill-repo>.git ~/.openclaw/workspace/skills/<skill-name>

# 2. Enable if it has hooks
openclaw hooks enable <skill-name>
```

## Recommended Skills for Your Setup

Based on your current OpenClaw configuration, here are skills that would complement your system:

### ✅ Already Installed:
- `proactive-agent` - Your proactive automation system
- `multi-search-engine` - Multiple search capabilities  
- `clawsec` - Security tools
- `ontology` - Knowledge graph system
- `self-improving-agent` - Self-improvement hooks
- `find-skills` - This skill!

### 🔧 Suggested Next:
- `weather` - Weather forecasts (useful for planning)
- `skill-creator` - Create custom skills for your needs
- `healthcheck` - Regular system security audits
- `tavily-search` - Enhanced web search (if you need more search power)
- `github` - GitHub integration for code projects

### 💼 Business-Focused:
- `calendar` - Calendar integration
- `notion` - Notion workspace integration
- `feishu` - Feishu/Lark integration (if you use it)
- `document` - Document processing

## Rate Limit Workarounds

Since clawhub is rate-limited, here are proven skills you can install manually:

```bash
# High-priority skills to install manually:
git clone https://github.com/openclaw/skills/weather.git ~/.openclaw/workspace/skills/weather
git clone https://github.com/halthelobster/skill-creator.git ~/.openclaw/workspace/skills/skill-creator
git clone https://github.com/openclaw/skills/healthcheck.git ~/.openclaw/workspace/skills/healthcheck
```

## Testing New Skills

After installing any skill:

1. **Read SKILL.md** - Understand what it does
2. **Check requirements** - Install any dependencies
3. **Test in isolation** - Try basic commands
4. **Integrate gradually** - Don't install too many at once
5. **Monitor performance** - Watch for issues

## Getting Help

If you need help finding specific skills:

1. **Describe your need** - "I need a skill for X"
2. **Check categories** - Use the category lists above
3. **Search alternatives** - Try different keywords
4. **Ask community** - Discord or forums
5. **Create custom** - Use skill-creator if nothing exists

Remember: The Find Skills Skill is your gateway to extending OpenClaw's capabilities!