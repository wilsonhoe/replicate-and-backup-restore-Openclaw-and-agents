# Programmatic SEO Guide
## Complete AI Blog Factory System

**Version:** 1.0
**Created:** 2026-03-31
**Revenue Potential:** $200-1,000/month per site

---

## System Overview

**Business Model:** Programmatic SEO
**Goal:** Create 100s of AI-generated pages → Rank for long-tail keywords → Monetize via ads/affiliate
**Timeline:** 2-6 months to first revenue

**The Strategy:**
> "Create a page for every [keyword variation] in [niche]. Let AI generate unique content for each. Rank for thousands of low-competition keywords."

---

## Phase 1: Keyword Research (Day 1)

### Find Keyword Patterns

**Python Script:**
```python
#!/usr/bin/env python3
"""
Keyword Pattern Finder
"""

import requests
import json
from itertools import product

def generate_keywords(base_terms, modifiers, locations):
    """
    Generate thousands of keyword variations
    """
    keywords = []

    # Pattern: [service] + [in] + [location]
    for term, loc in product(base_terms, locations):
        keywords.append(f"{term} in {loc}")
        keywords.append(f"{term} near {loc}")
        keywords.append(f"best {term} in {loc}")
        keywords.append(f"cheap {term} in {loc}")
        keywords.append(f"{loc} {term}")

    # Pattern: [modifier] + [service]
    for mod, term in product(modifiers, base_terms):
        keywords.append(f"{mod} {term}")

    return keywords

# Example: Local services
base_terms = [
    "roofing contractor",
    "plumber",
    "electrician",
    "HVAC repair",
    "pest control"
]

modifiers = [
    "best",
    "cheap",
    "emergency",
    "24 hour",
    "licensed",
    "top rated"
]

locations = [
    "Miami FL",
    "Austin TX",
    "Denver CO",
    "Seattle WA",
    "Atlanta GA"
]

keywords = generate_keywords(base_terms, modifiers, locations)
print(f"Generated {len(keywords)} keywords")

# Save
with open('keywords.json', 'w') as f:
    json.dump(keywords, f, indent=2)
```

### Check Keyword Difficulty

```python
def estimate_difficulty(keyword):
    """
    Estimate SEO difficulty (simplified)
    """
    # Search Google and analyze results
    search_url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}"

    # Factors:
    # - Number of results
    # - Presence of major sites (Wikipedia, Yelp, etc.)
    # - Content quality

    difficulty_score = 0

    # Shorter keywords = harder
    if len(keyword.split()) <= 2:
        difficulty_score += 30

    # Major cities = harder
    major_cities = ['new york', 'los angeles', 'chicago', 'houston']
    if any(city in keyword.lower() for city in major_cities):
        difficulty_score += 20

    return min(difficulty_score, 100)

# Filter for easy keywords
easy_keywords = [k for k in keywords if estimate_difficulty(k) < 40]
print(f"Found {len(easy_keywords)} easy keywords")
```

---

## Phase 2: Content Generation (Day 2-3)

### AI Article Generator

```python
#!/usr/bin/env python3
"""
AI Content Generator for Programmatic SEO
"""

import requests
import json
from jinja2 import Template

class SEOContentGenerator:
    def __init__(self, model='kimi-k2.5:cloud'):
        self.model = model
        self.ollama_url = 'http://localhost:11434/api/generate'

    def generate_article(self, keyword, word_count=800):
        """
        Generate SEO-optimized article for keyword
        """

        # Parse keyword
        parts = keyword.split(' in ')
        service = parts[0] if len(parts) > 0 else keyword
        location = parts[1] if len(parts) > 1 else "your area"

        prompt = f"""Write an SEO-optimized article about: "{keyword}"

Target: {word_count} words
Structure:
- H1: {keyword} (exact match)
- Intro: 100 words, include keyword naturally
- H2: Why You Need {service.title()} in {location.title()}
- H2: How to Choose the Best {service.title()}
- H2: {service.title()} Costs in {location.title()}
- H2: Top {service.title()} Companies in {location.title()}
- Conclusion: Include CTA

Requirements:
- Keyword density: 1-2%
- Natural language, not spammy
- Include specific details about {location}
- Add bullet points and lists
- Include FAQ section

Write in a helpful, informative tone."""

        response = requests.post(self.ollama_url, json={
            'model': self.model,
            'prompt': prompt,
            'stream': False
        })

        content = response.json()['response']

        # Add meta tags
        article = {
            'title': f"{keyword.title()} | 2024 Guide",
            'meta_description': f"Find the best {service} in {location}. Compare prices, read reviews, and hire top-rated professionals. Updated 2024.",
            'content': content,
            'keyword': keyword,
            'word_count': len(content.split()),
            'h1': keyword,
            'slug': keyword.replace(' ', '-').lower()
        }

        return article

    def generate_bulk(self, keywords, output_dir='content'):
        """
        Generate articles for all keywords
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        articles = []

        for i, keyword in enumerate(keywords):
            print(f"Generating {i+1}/{len(keywords)}: {keyword}")

            article = self.generate_article(keyword)
            articles.append(article)

            # Save individual file
            filename = f"{output_dir}/{article['slug']}.json"
            with open(filename, 'w') as f:
                json.dump(article, f, indent=2)

            # Rate limiting
            import time
            time.sleep(1)

        return articles

# Usage
if __name__ == "__main__":
    generator = SEOContentGenerator()

    # Load keywords
    with open('easy_keywords.json', 'r') as f:
        keywords = json.load(f)

    # Generate first 50
    articles = generator.generate_bulk(keywords[:50])
    print(f"Generated {len(articles)} articles")
```

### Content Template

**HTML Template:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <meta name="description" content="{{ meta_description }}">
    <link rel="canonical" href="https://yoursite.com/{{ slug }}">

    <!-- Schema markup -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{{ title }}",
        "description": "{{ meta_description }}",
        "datePublished": "{{ date }}",
        "author": {
            "@type": "Organization",
            "name": "Your Site"
        }
    }
    </script>
</head>
<body>
    <article>
        <h1>{{ h1 }}</h1>
        <div class="content">
            {{ content | safe }}
        </div>

        <section class="cta">
            <h2>Ready to Get Started?</h2>
            <p>Contact the best {{ service }} in {{ location }} today.</p>
            <a href="/contact" class="button">Get Free Quotes</a>
        </section>

        <section class="related">
            <h2>Related Articles</h2>
            <ul>
                {% for related in related_articles %}
                <li><a href="/{{ related.slug }}">{{ related.title }}</a></li>
                {% endfor %}
            </ul>
        </section>
    </article>

    <!-- Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'GA_ID');
    </script>
</body>
</html>
```

---

## Phase 3: Site Structure (Day 4)

### Static Site Generator

```python
#!/usr/bin/env python3
"""
Static Site Generator for Programmatic SEO
"""

import json
import os
from jinja2 import Template

class SiteGenerator:
    def __init__(self, template_file='template.html'):
        with open(template_file, 'r') as f:
            self.template = Template(f.read())

    def generate_site(self, content_dir='content', output_dir='site'):
        """
        Generate complete static site
        """
        os.makedirs(output_dir, exist_ok=True)

        # Load all articles
        articles = []
        for filename in os.listdir(content_dir):
            if filename.endswith('.json'):
                with open(f"{content_dir}/{filename}", 'r') as f:
                    articles.append(json.load(f))

        # Generate pages
        for article in articles:
            # Find related articles
            related = [a for a in articles if a['keyword'] != article['keyword']][:5]

            # Render HTML
            html = self.template.render(
                title=article['title'],
                meta_description=article['meta_description'],
                h1=article['h1'],
                content=article['content'],
                slug=article['slug'],
                related_articles=related,
                date=article.get('date', '2024')
            )

            # Save
            output_file = f"{output_dir}/{article['slug']}.html"
            with open(output_file, 'w') as f:
                f.write(html)

            print(f"Generated: {output_file}")

        # Generate index page
        self.generate_index(articles, output_dir)

        # Generate sitemap
        self.generate_sitemap(articles, output_dir)

    def generate_index(self, articles, output_dir):
        """Generate homepage with links to all articles"""
        html = """<!DOCTYPE html>
<html>
<head><title>Your Guide | Home</title></head>
<body>
    <h1>Complete Guides</h1>
    <ul>
"""
        for article in articles:
            html += f'        <li><a href="/{article[\'slug\']}.html">{article[\'title\']}</a></li>\n'

        html += """    </ul>
</body>
</html>"""

        with open(f"{output_dir}/index.html", 'w') as f:
            f.write(html)

    def generate_sitemap(self, articles, output_dir):
        """Generate XML sitemap"""
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

        for article in articles:
            sitemap += f"""  <url>
    <loc>https://yoursite.com/{article['slug']}.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
"""

        sitemap += '</urlset>'

        with open(f"{output_dir}/sitemap.xml", 'w') as f:
            f.write(sitemap)

# Usage
if __name__ == "__main__":
    generator = SiteGenerator()
    generator.generate_site()
```

### Internal Linking

```python
def add_internal_links(articles):
    """
    Add internal links between related articles
    """
    for article in articles:
        content = article['content']

        # Find opportunities to link to other articles
        for other in articles:
            if other['keyword'] != article['keyword']:
                # Check if keyword appears in content
                if other['keyword'] in content:
                    # Replace first occurrence with link
                    content = content.replace(
                        other['keyword'],
                        f'<a href="/{other[\'slug\']}.html">{other[\'keyword\']}</a>',
                        1
                    )

        article['content'] = content

    return articles
```

---

## Phase 4: Deployment (Day 5)

### Hosting Options

**Option 1: Netlify (Free)**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd site
netlify deploy --prod --dir=.
```

**Option 2: GitHub Pages (Free)**
```bash
# Push to GitHub
git init
git add .
git commit -m "Initial site"
git remote add origin https://github.com/username/repo.git
git push -u origin main

# Enable Pages in GitHub settings
```

**Option 3: Cloudflare Pages (Free)**
- Connect GitHub repo
- Auto-deploy on push

### Domain Setup

```bash
# Buy domain (Namecheap, Cloudflare)
# Point DNS to hosting
# Enable SSL (usually automatic)
```

---

## Phase 5: Indexing (Day 6-7)

### Submit to Google

```python
def submit_to_indexnow(urls):
    """
    Submit URLs to search engines via IndexNow
    """
    import requests

    endpoint = "https://api.indexnow.org/IndexNow"

    data = {
        "host": "yoursite.com",
        "key": "YOUR_API_KEY",
        "keyLocation": "https://yoursite.com/YOUR_API_KEY.txt",
        "urlList": urls[:100]  # Max 100 per request
    }

    response = requests.post(
        endpoint,
        json=data,
        headers={"Content-Type": "application/json"}
    )

    return response.status_code == 200
```

### Google Search Console

1. Add property
2. Submit sitemap
3. Request indexing for key pages
4. Monitor performance

---

## Monetization

### Google AdSense

**Requirements:**
- 30+ pages of unique content
- No policy violations
- 6+ months old (sometimes)

**Placement:**
- Above fold
- In-content
- Sidebar

### Affiliate Links

**High-converting niches:**
- Local services (HomeAdvisor, Angi)
- Software (G2, Capterra)
- Products (Amazon)

**Placement:**
- "Recommended" sections
- Comparison tables
- CTA buttons

### Lead Generation

**Model:**
- Collect leads via forms
- Sell to local businesses
- $5-25 per lead

---

## Scaling Strategy

### Month 1: Foundation
- [ ] Pick 1 niche (local services)
- [ ] Generate 50 pages
- [ ] Deploy site
- [ ] Submit to Google

### Month 2: Expansion
- [ ] Add 100 more pages
- [ ] Build backlinks
- [ ] Apply for AdSense
- [ ] Add affiliate links

### Month 3: Optimization
- [ ] Analyze rankings
- [ ] Update top pages
- [ ] Add schema markup
- [ ] Build second site

### Month 6: Portfolio
- [ ] 5+ sites running
- [ ] $1,000+ monthly revenue
- [ ] Systematized process
- [ ] Consider selling sites

---

## Key Metrics to Track

| Metric | Target | Tool |
|--------|--------|------|
| Indexed Pages | 100% | Search Console |
| Organic Traffic | 100/day | Analytics |
| Average Position | <20 | Search Console |
| CTR | >3% | Search Console |
| Revenue | $500/mo | AdSense |

---

## Common Issues

**Pages not indexing?**
- Check robots.txt
- Submit sitemap again
- Build backlinks
- Improve content quality

**No traffic?**
- Keywords too competitive
- Content too thin
- Need more backlinks
- Wrong niche

**Low revenue?**
- Traffic too low
- Wrong ad placement
- Wrong niche for ads
- Try affiliate instead

---

**Revenue Target:** $1,000/month = 10,000 monthly visits @ $100 RPM

**Timeline:** Month 1-2 = Build, Month 3-4 = Rank, Month 5-6 = Revenue

---

**System Status:** READY TO DEPLOY
**Next Action:** Generate first 50 articles
