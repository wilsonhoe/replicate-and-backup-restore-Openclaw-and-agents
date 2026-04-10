#!/usr/bin/env python3
"""
Find Skills Skill Integration for OpenClaw
Provides utility functions for discovering and searching skills
"""

import subprocess
import json
import sys
from pathlib import Path

def search_clawhub(keyword, sort_by=None):
    """Search for skills on ClawHub"""
    try:
        cmd = ["npx", "clawhub@latest", "search", keyword]
        if sort_by:
            cmd.extend(["--sort", sort_by])
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error searching ClawHub: {result.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: Search timed out (rate limit likely hit)"
    except FileNotFoundError:
        return "Error: npx/clawhub not found. Make sure Node.js is installed."
    except Exception as e:
        return f"Error: {str(e)}"

def find_skills_by_category(category):
    """Find skills by category"""
    categories = {
        "search": ["web search", "tavily", "search"],
        "integration": ["github", "calendar", "notion", "feishu"],
        "agent": ["proactive", "coding", "automation"],
        "core": ["weather", "skill-creator", "healthcheck"],
        "productivity": ["document", "notes", "tasks"]
    }
    
    if category.lower() in categories:
        keywords = categories[category.lower()]
        results = []
        for keyword in keywords:
            result = search_clawhub(keyword)
            if result and "Error" not in result:
                results.append(f"Results for '{keyword}':\n{result}")
        return "\n\n".join(results) if results else f"No results found for category: {category}"
    else:
        return f"Unknown category: {category}. Available: {', '.join(categories.keys())}"

def list_popular_skills():
    """List popular skills from various sources"""
    popular_skills = [
        "proactive-agent",
        "weather", 
        "skill-creator",
        "healthcheck",
        "tavily-search",
        "github",
        "multi-search-engine",
        "clawsec",
        "ontology"
    ]
    
    results = ["Popular OpenClaw Skills:"]
    results.append("=" * 30)
    
    for skill in popular_skills:
        results.append(f"• {skill}")
        # Try to get more info from clawhub
        info = search_clawhub(skill)
        if info and "Error" not in info and len(info) < 200:  # Avoid long outputs
            results.append(f"  {info[:100]}...")
    
    return "\n".join(results)

def get_skill_install_command(skill_name):
    """Get the installation command for a skill"""
    return f"npx clawhub@latest install {skill_name}"

def show_skill_sources():
    """Show where to find skills"""
    sources = [
        "🔍 ClawHub (Primary): https://clawhub.ai",
        "📁 OpenClaw Directory: https://www.openclawdirectory.dev/skills",
        "🦞 LobeHub Marketplace: https://lobehub.com/skills", 
        "💻 GitHub: Search 'openclaw skill' or 'agent-skill'",
        "💬 Discord Community: https://discord.com/invite/clawd",
        "🌐 SitePoint Forums: https://www.sitepoint.com/community/"
    ]
    
    return "Skill Sources:\n" + "\n".join(sources)

def handle_rate_limits():
    """Provide guidance when hitting rate limits"""
    return """
⚠️ Rate Limit Hit!

Try these alternatives:
1. Wait 1 hour before retrying
2. Browse websites directly (clawhub.ai, openclawdirectory.dev)
3. Search GitHub manually for "openclaw skill"
4. Check the OpenClaw Discord community

For immediate needs, try these popular skills:
- proactive-agent
- weather
- skill-creator  
- healthcheck
- tavily-search
"""

if __name__ == "__main__":
    print("Find Skills Skill - Test Mode")
    print("=" * 40)
    
    # Test popular skills list
    print("\n1. Popular Skills:")
    print(list_popular_skills())
    
    # Test skill sources
    print("\n2. Skill Sources:")
    print(show_skill_sources())
    
    # Test category search (may hit rate limits)
    print("\n3. Testing category search (may hit rate limits):")
    result = find_skills_by_category("core")
    if "Error" in result and "rate limit" in result.lower():
        print(handle_rate_limits())
    else:
        print(result)
    
    print("\n✅ Find Skills Skill test completed!")