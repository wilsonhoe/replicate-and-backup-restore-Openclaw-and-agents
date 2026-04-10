#!/usr/bin/env python3
"""
Automated Business Research for Lisamolbot@gmail.com
Automated research workflow using bb-browser
"""

import subprocess
import json
import time
from datetime import datetime

def run_research_query(platform, query, max_results=5):
    """Run a single research query"""
    try:
        cmd = ["bb-browser", "--port", "19825", "site", f"{platform}/search", query, str(max_results)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            return {
                "success": True,
                "platform": platform,
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "data": result.stdout.strip()
            }
        else:
            return {
                "success": False,
                "platform": platform,
                "query": query,
                "error": result.stderr.strip()
            }
    except Exception as e:
        return {
            "success": False,
            "platform": platform,
            "query": query,
            "error": str(e)
        }

def run_daily_research():
    """Run daily business research"""
    
    print("🌐 Daily Business Research - Lisamolbot@gmail.com")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    # Define research queries
    research_queries = [
        # Real Estate Market
        ("twitter", "Singapore property investment 2024"),
        ("reddit", "Singapore real estate market"),
        ("linkedin", "Singapore property technology"),
        
        # Investment Trends
        ("twitter", "AI stock trading Singapore 2024"),
        ("linkedin", "machine learning finance investment"),
        ("xueqiu", "hot-stock"),
        
        # AI Technology
        ("twitter", "LangChain real estate applications"),
        ("github", "real estate automation python"),
        ("reddit", "real estate technology"),
    ]
    
    results = []
    
    for platform, query in research_queries:
        print(f"🔍 Researching: {query} on {platform}")
        result = run_research_query(platform, query, 3)
        results.append(result)
        
        if result["success"]:
            print(f"   ✅ Success - Found data")
        else:
            print(f"   ❌ Failed - {result['error'][:50]}...")
        
        time.sleep(3)  # Rate limiting
    
    # Summary
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    
    print(f"\n📊 Research Complete:")
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/home/wls/.openclaw/workspace/research_results_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {filename}")
    return results

if __name__ == "__main__":
    # Run daily research
    results = run_daily_research()
    
    print("\n✅ Daily research complete!")
    print("\nNext steps:")
    print("1. Review the research results")
    print("2. Store insights in your knowledge system")
    print("3. Set up automated scheduling with cron")
