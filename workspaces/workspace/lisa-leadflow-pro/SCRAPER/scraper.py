#!/usr/bin/env python3
"""
LeadFlow Pro - Real Estate Lead Scraper
Scrapes property listings and extracts lead information
"""

import os
import json
import csv
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class LeadScraper:
    """Main scraper class for LeadFlow Pro"""

    def __init__(self, config_path: str = 'config.json'):
        """Initialize the scraper with configuration"""
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.cities = self.config.get('cities', [])
        self.property_types = self.config.get('property_types', [])
        self.price_range = self.config.get('price_range', {})
        self.leads = []
        self.seen_phones = set()

        logger.info(f"Initialized scraper for cities: {', '.join(self.cities)}")

    def scrape_city(self, city: str) -> List[Dict]:
        """Scrape listings for a specific city"""
        logger.info(f"Scraping {city}...")
        leads = []

        # Template scraper - customize for your target sources
        # This is a placeholder - replace with actual scraping logic

        for property_type in self.property_types:
            try:
                # Example: Scrape from sample source
                city_leads = self._scrape_source(city, property_type)
                leads.extend(city_leads)
                logger.info(f"Found {len(city_leads)} leads in {city} for {property_type}")
            except Exception as e:
                logger.error(f"Error scraping {city} {property_type}: {e}")

        return leads

    def _scrape_source(self, city: str, property_type: str) -> List[Dict]:
        """
        Scrape a specific source for leads
        CUSTOMIZE THIS METHOD for your target sources
        """
        leads = []

        # EXAMPLE: Generic scraping pattern
        # Replace with actual implementation for your sources

        search_url = f"https://example-real-estate-site.com/search"
        params = {
            'city': city,
            'type': property_type,
            'min_price': self.price_range.get('min', 0),
            'max_price': self.price_range.get('max', 999999999)
        }

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(search_url, params=params, headers=headers, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Example: Find listing containers
            listings = soup.find_all('div', class_='listing')

            for listing in listings:
                lead = self._extract_lead_info(listing)
                if lead and self._is_valid_lead(lead):
                    leads.append(lead)

        except Exception as e:
            logger.error(f"Error in _scrape_source: {e}")

        return leads

    def _extract_lead_info(self, listing_element) -> Optional[Dict]:
        """
        Extract lead information from a listing element
        CUSTOMIZE based on your target website's HTML structure
        """
        try:
            # Example extraction - customize selectors
            name_elem = listing_element.find('span', class_='agent-name')
            phone_elem = listing_element.find('span', class_='phone')
            email_elem = listing_element.find('a', class_='email')
            price_elem = listing_element.find('span', class_='price')

            name = name_elem.text.strip() if name_elem else "Unknown"
            phone = phone_elem.text.strip() if phone_elem else ""
            email = email_elem.get('href', '').replace('mailto:', '') if email_elem else ""

            # Parse price
            price_text = price_elem.text.strip() if price_elem else "0"
            price = self._parse_price(price_text)

            # Skip if we've seen this phone before
            if phone in self.seen_phones:
                return None

            if phone:
                self.seen_phones.add(phone)

            return {
                'name': name,
                'phone': phone,
                'email': email,
                'budget': price,
                'property_interest': '',
                'source': 'scraper',
                'scraped_date': datetime.now().isoformat(),
                'status': 'New'
            }

        except Exception as e:
            logger.error(f"Error extracting lead info: {e}")
            return None

    def _parse_price(self, price_text: str) -> int:
        """Parse price from text"""
        try:
            # Remove non-numeric characters
            price_clean = ''.join(c for c in price_text if c.isdigit())
            return int(price_clean) if price_clean else 0
        except:
            return 0

    def _is_valid_lead(self, lead: Dict) -> bool:
        """Validate lead data"""
        # Must have at least phone or email
        if not lead.get('phone') and not lead.get('email'):
            return False

        # Phone should be at least 10 digits
        phone = lead.get('phone', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        if phone and len(phone) < 10:
            return False

        return True

    def run(self) -> List[Dict]:
        """Run the complete scraping process"""
        logger.info("Starting LeadFlow Pro scraper...")

        for city in self.cities:
            city_leads = self.scrape_city(city)
            self.leads.extend(city_leads)
            time.sleep(2)  # Be nice to servers

        logger.info(f"Scraping complete. Total leads: {len(self.leads)}")
        return self.leads

    def export_to_csv(self, filename: str = 'leads.csv') -> str:
        """Export leads to CSV file"""
        if not self.leads:
            logger.warning("No leads to export")
            return ""

        fieldnames = ['name', 'phone', 'email', 'budget', 'property_interest',
                     'source', 'scraped_date', 'status']

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.leads)

        logger.info(f"Exported {len(self.leads)} leads to {filename}")
        return filename


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='LeadFlow Pro Scraper')
    parser.add_argument('--run-once', action='store_true', help='Run once and exit')
    parser.add_argument('--daemon', action='store_true', help='Run continuously with scheduling')
    parser.add_argument('--output', default='leads.csv', help='Output CSV filename')

    args = parser.parse_args()

    scraper = LeadScraper()

    if args.run_once:
        leads = scraper.run()
        scraper.export_to_csv(args.output)
        print(f"✅ Scraped {len(leads)} leads. Saved to {args.output}")

    elif args.daemon:
        import schedule

        interval_hours = scraper.config.get('schedule', {}).get('interval_hours', 6)
        logger.info(f"Starting daemon mode. Running every {interval_hours} hours")

        def job():
            leads = scraper.run()
            scraper.export_to_csv(args.output)
            logger.info(f"Scheduled scrape complete: {len(leads)} leads")

        schedule.every(interval_hours).hours.do(job)

        # Run immediately on start
        job()

        while True:
            schedule.run_pending()
            time.sleep(60)

    else:
        print("Use --run-once or --daemon flag")
        print("Example: python scraper.py --run-once")


if __name__ == '__main__':
    main()