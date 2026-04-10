#!/usr/bin/env python3
"""
No-Login bb-browser Integration
Safe platforms that work without authentication
"""

from skills.bb-browser.bb_integration_updated import (
    search_platform, get_trending_content, 
    search_stackoverflow, get_wikipedia_summary,
    get_news_headlines, cross_platform_research
)

def research_without_login(topic: str, max_results: int = 5):
    """Research a topic using platforms that don't require login"""
    
    results = {}
    
    # Academic research
    try:
        results["arxiv"] = search_platform("arxiv", topic, max_results)
    except Exception as e:
        results["arxiv"] = {"error": str(e)}
    
    # Developer resources
    try:
        results["stackoverflow"] = search_platform("stackoverflow", topic, max_results)
    except Exception as e:
        results["stackoverflow"] = {"error": str(e)}
    
    # Encyclopedia
    try:
        results["wikipedia"] = search_platform("wikipedia", topic, max_results)
    except Exception as e:
        results["wikipedia"] = {"error": str(e)}
    
    # Tech news
    try:
        results["hackernews"] = get_trending_content("hackernews", max_results)
    except Exception as e:
        results["hackernews"] = {"error": str(e)}
    
    # General web search (privacy-focused)
    try:
        results["duckduckgo"] = search_platform("duckduckgo", topic, max_results)
    except Exception as e:
        results["duckduckgo"] = {"error": str(e)}
    
    return results

def market_research_no_login():
    """Market research without requiring login"""
    
    research = {}
    
    # Tech trends
    research["tech_trends"] = research_without_login("real estate automation AI", 3)
    
    # Financial news
    try:
        research["finance_news"] = get_news_headlines("eastmoney", "房地产")
    except Exception as e:
        research["finance_news"] = {"error": str(e)}
    
    # Academic research on real estate tech
    try:
        research["academic_research"] = search_platform("arxiv", "real estate machine learning", 3)
    except Exception as e:
        research["academic_research"] = {"error": str(e)}
    
    return research

def content_research_no_login(topic: str):
    """Content research without login"""
    
    research = {}
    
    # Multi-platform research
    platforms = ["arxiv", "stackoverflow", "wikipedia", "duckduckgo"]
    research["cross_platform"] = cross_platform_research(topic, platforms)
    
    # Tech trends
    try:
        research["tech_trends"] = get_trending_content("hackernews", 10)
    except Exception as e:
        research["tech_trends"] = {"error": str(e)}
    
    # News headlines
    try:
        research["news"] = get_news_headlines("bbc", "technology")
    except Exception as e:
        research["news"] = {"error": str(e)}
    
    return research

if __name__ == "__main__":
    print("🔍 No-Login Research Demo")
    print("=" * 40)
    
    # Test basic research
    print("\n1. Testing AI agent research:")
    results = research_without_login("AI agent", 3)
    
    for platform, data in results.items():
        if data.get("success"):
            print(f"   ✅ {platform}: Found results")
        else:
            print(f"   ⚠️  {platform}: {data.get('error', 'Failed')}")
    
    print("\n2. Testing market research:")
    market_results = market_research_no_login()
    
    for category, data in market_results.items():
        if data.get("success"):
            print(f"   ✅ {category}: Found data")
        else:
            print(f"   ⚠️  {category}: {data.get('error', 'Failed')}")
    
    print("\n✅ No-login research system ready!")
    print("\nUsage examples:")
    print("  research_without_login('real estate automation')")
    print("  market_research_no_login()")
    print("  content_research_no_login('machine learning')")
