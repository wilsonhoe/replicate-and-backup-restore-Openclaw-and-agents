#!/usr/bin/env python3
"""
Find Skills Skill - Simple Reference Implementation
Provides guidance on finding OpenClaw skills without external calls
"""

def get_skill_sources():
    """Return list of places to find OpenClaw skills"""
    return [
        "🔍 ClawHub (Primary): https://clawhub.ai",
        "📁 OpenClaw Directory: https://www.openclawdirectory.dev/skills", 
        "🦞 LobeHub Marketplace: https://lobehub.com/skills",
        "💻 GitHub: Search 'openclaw skill' or 'agent-skill'",
        "💬 Discord Community: https://discord.com/invite/clawd",
        "🌐 SitePoint Forums: https://www.sitepoint.com/community/"
    ]

def get_popular_skills():
    """Return list of popular OpenClaw skills"""
    return [
        ("proactive-agent", "Transform agents into proactive partners"),
        ("weather", "Get weather forecasts and conditions"),
        ("skill-creator", "Create new OpenClaw skills"),
        ("healthcheck", "Security audits and system checks"),
        ("tavily-search", "Web search via Tavily API"),
        ("github", "GitHub operations and management"),
        ("multi-search-engine", "Multiple search engine integration"),
        ("clawsec", "Security tools and utilities"),
        ("ontology", "Typed knowledge graph system"),
        ("find-skills", "Discover and search for skills (this one!)")
    ]

def get_skill_categories():
    """Return skill categories and examples"""
    return {
        "Core Skills": ["weather", "skill-creator", "healthcheck"],
        "Search Skills": ["tavily-search", "web-search-plus", "multi-search-engine"],
        "Integration Skills": ["github", "feishu", "notion", "calendar"],
        "Agent Skills": ["proactive-agent", "coding-agent", "self-improving-agent"],
        "Productivity Skills": ["document", "notes", "tasks", "ontology"],
        "Security Skills": ["clawsec", "healthcheck", "security-audit"]
    }

def get_install_command(skill_name):
    """Return the installation command for a skill"""
    return f"npx clawhub@latest install {skill_name}"

def show_rate_limit_help():
    """Show help for when rate limits are hit"""
    return """
⚠️ Rate Limit Hit!

The clawhub API is currently rate limited. Try these alternatives:

1. 🌐 Browse websites directly:
   - https://clawhub.ai
   - https://www.openclawdirectory.dev/skills

2. 🔍 Search GitHub manually:
   - Search: "openclaw skill" or "agent-skill"
   - Look for repositories with SKILL.md files

3. 💬 Check community resources:
   - Discord: https://discord.com/invite/clawd
   - Forums: https://www.sitepoint.com/community/

4. ⏰ Wait and retry:
   - Rate limits typically reset after 1 hour
   - Try again later with: npx clawhub@latest search [keyword]

Popular skills to try:
- proactive-agent
- weather  
- skill-creator
- healthcheck
"""

def main():
    print("🔍 Find Skills Skill - Reference Guide")
    print("=" * 50)
    
    print("\n📍 Skill Sources:")
    for source in get_skill_sources():
        print(f"  {source}")
    
    print("\n⭐ Popular Skills:")
    for skill, description in get_popular_skills():
        print(f"  • {skill:<20} - {description}")
    
    print("\n📂 Skill Categories:")
    categories = get_skill_categories()
    for category, skills in categories.items():
        print(f"  {category}:")
        for skill in skills:
            print(f"    • {skill}")
    
    print(f"\n💾 Installation Command:")
    print(f"  {get_install_command('<skill-name>')}")
    print(f"  Example: {get_install_command('proactive-agent')}")
    
    print(f"\n⚡ Quick Start:")
    print("  1. Browse https://clawhub.ai for available skills")
    print("  2. Search for specific functionality you need")
    print("  3. Install with: npx clawhub@latest install <skill-name>")
    print("  4. Test the skill in your OpenClaw session")
    
    print(f"\n🆘 Rate Limit Help:")
    print(show_rate_limit_help())

if __name__ == "__main__":
    main()