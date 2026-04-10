#!/usr/bin/env python3
# crypto_signals.py - Daily sentiment analysis service

import subprocess
import json
import datetime
from typing import Dict, List

def get_crypto_sentiment() -> Dict:
    """Get comprehensive crypto market sentiment"""
    
    # Reddit sentiment (primary source)
    reddit_result = subprocess.run([
        'bb-browser', 'site', 'reddit/hot', 'cryptocurrency', '--json'
    ], capture_output=True, text=True)
    
    if reddit_result.returncode == 0:
        reddit_data = json.loads(reddit_result.stdout)
        reddit_posts = reddit_data.get('data', {}).get('posts', [])
        
        # Calculate sentiment score
        bullish_keywords = ['bull', 'buy', 'moon', 'pump', 'green', 'up']
        bearish_keywords = ['bear', 'sell', 'dump', 'red', 'down', 'crash']
        
        sentiment_score = 0
        total_mentions = 0
        
        for post in reddit_posts[:20]:  # Top 20 posts
            title = post.get('title', '').lower()
            
            bullish_count = sum(1 for word in bullish_keywords if word in title)
            bearish_count = sum(1 for word in bearish_keywords if word in title)
            
            sentiment_score += (bullish_count - bearish_count)
            total_mentions += (bullish_count + bearish_count)
        
        reddit_sentiment = {
            'score': sentiment_score,
            'intensity': total_mentions,
            'posts_analyzed': len(reddit_posts[:20])
        }
    else:
        reddit_sentiment = {'score': 0, 'intensity': 0, 'posts_analyzed': 0}
    
    # Weibo sentiment (China market)
    weibo_result = subprocess.run([
        'bb-browser', 'site', 'weibo/hot', '--json'
    ], capture_output=True, text=True)
    
    if weibo_result.returncode == 0:
        weibo_data = json.loads(weibo_result.stdout)
        weibo_topics = weibo_data.get('data', {}).get('items', [])
        
        # Look for crypto-related topics
        crypto_keywords = ['比特币', 'crypto', 'gold', '金价', 'blockchain']
        crypto_mentions = []
        
        for topic in weibo_topics:
            word = topic.get('word', '')
            if any(keyword in word.lower() for keyword in crypto_keywords):
                crypto_mentions.append({
                    'topic': word,
                    'hot_value': topic.get('hot_value', 0),
                    'rank': topic.get('rank', 0)
                })
        
        weibo_sentiment = {
            'crypto_mentions': crypto_mentions,
            'total_topics': len(weibo_topics)
        }
    else:
        weibo_sentiment = {'crypto_mentions': [], 'total_topics': 0}
    
    return {
        'timestamp': datetime.datetime.now().isoformat(),
        'reddit_sentiment': reddit_sentiment,
        'weibo_sentiment': weibo_sentiment,
        'overall_signal': 'BUY' if reddit_sentiment['score'] > 2 else 'SELL' if reddit_sentiment['score'] < -2 else 'HOLD'
    }

def generate_signal_report() -> str:
    """Generate trading signal report"""
    sentiment = get_crypto_sentiment()
    
    report = f"""
🎯 CRYPTO SENTIMENT REPORT
Generated: {sentiment['timestamp']}

📊 REDDIT SENTIMENT:
- Score: {sentiment['reddit_sentiment']['score']}
- Intensity: {sentiment['reddit_sentiment']['intensity']}
- Posts Analyzed: {sentiment['reddit_sentiment']['posts_analyzed']}

🇨🇳 WEIBO SENTIMENT:
- Crypto Topics Found: {len(sentiment['weibo_sentiment']['crypto_mentions'])}
- Top Crypto Topic: {sentiment['weibo_sentiment']['crypto_mentions'][0]['topic'] if sentiment['weibo_sentiment']['crypto_mentions'] else 'None'}

🎯 TRADING SIGNAL: {sentiment['overall_signal']}
"""
    
    return report

if __name__ == "__main__":
    print(generate_signal_report())
    
    # Save report to file
    import os
    os.makedirs('/home/wls/crypto_reports', exist_ok=True)
    
    filename = f"/home/wls/crypto_reports/signal_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(filename, 'w') as f:
        f.write(generate_signal_report())
    
    print(f"Report saved: {filename}")