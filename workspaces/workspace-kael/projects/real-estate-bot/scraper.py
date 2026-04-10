#!/usr/bin/env python3
"""
Real Estate Lead Bot
Scrapes listings from multiple cities and outputs to CSV + Google Sheets
"""

import csv
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/wls/.openclaw/workspace-kael/projects/real-estate-bot/scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Cities to scrape
CITIES = [
    {"name": "Singapore", "base_url": "https://www.propertyguru.com.sg"},
    {"name": "Kuala Lumpur", "base_url": "https://www.propertyguru.com.my"},
    {"name": "Bangkok", "base_url": "https://www.ddproperty.com"}
]

CSV_OUTPUT = "/home/wls/.openclaw/workspace-kael/projects/real-estate-bot/listings.csv"

def scrape_listings(city):
    """Scrape listings for a given city"""
    logger.info(f"Scraping {city['name']}...")
    
    # Placeholder - in production, implement actual scraping logic
    # For demo, return sample data
    sample_listings = [
        {
            "listing_id": f"{city['name'][:3].upper()}{datetime.now().strftime('%Y%m%d%H%M%S')}001",
            "city": city["name"],
            "title": f"2 Bedroom Condo in {city['name']}",
            "price": "850000",
            "currency": "SGD" if city["name"] == "Singapore" else "MYR" if city["name"] == "Kuala Lumpur" else "THB",
            "bedrooms": "2",
            "bathrooms": "2",
            "area_sqft": "850",
            "address": f"Sample Address, {city['name']}",
            "property_type": "Condo",
            "listing_date": datetime.now().strftime("%Y-%m-%d"),
            "source_url": f"{city['base_url']}/listing/12345",
            "contact_name": "Sample Agent",
            "contact_phone": "+65 9123 4567",
            "contact_email": "agent@example.com"
        }
    ]
    
    logger.info(f"Found {len(sample_listings)} listings in {city['name']}")
    return sample_listings

def save_to_csv(all_listings):
    """Save listings to CSV file"""
    fieldnames = [
        "listing_id", "city", "title", "price", "currency", "bedrooms", 
        "bathrooms", "area_sqft", "address", "property_type", "listing_date",
        "source_url", "contact_name", "contact_phone", "contact_email"
    ]
    
    file_exists = os.path.exists(CSV_OUTPUT)
    
    with open(CSV_OUTPUT, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(all_listings)
    
    logger.info(f"Saved {len(all_listings)} listings to {CSV_OUTPUT}")

def upload_to_google_sheets(listings):
    """Upload listings to Google Sheets"""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        
        # Load credentials from environment or file
        creds_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS', 
                               '/home/wls/.openclaw/workspace-kael/projects/real-estate-bot/credentials.json')
        
        if not os.path.exists(creds_path):
            logger.warning(f"Google Sheets credentials not found at {creds_path}")
            logger.info("Skipping Google Sheets upload")
            return False
        
        credentials = service_account.Credentials.from_service_account_file(
            creds_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        service = build('sheets', 'v4', credentials=credentials)
        
        spreadsheet_id = os.getenv('SPREADSHEET_ID')
        if not spreadsheet_id:
            logger.warning("SPREADSHEET_ID not set")
            return False
        
        # Prepare data
        values = []
        for listing in listings:
            values.append([
                listing.get("listing_id", ""),
                listing.get("city", ""),
                listing.get("title", ""),
                listing.get("price", ""),
                listing.get("currency", ""),
                listing.get("bedrooms", ""),
                listing.get("bathrooms", ""),
                listing.get("area_sqft", ""),
                listing.get("address", ""),
                listing.get("property_type", ""),
                listing.get("listing_date", ""),
                listing.get("source_url", ""),
                listing.get("contact_name", ""),
                listing.get("contact_phone", ""),
                listing.get("contact_email", "")
            ])
        
        body = {'values': values}
        
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range='Sheet1!A1',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        logger.info(f"Uploaded {result.get('updates', {}).get('updatedRows', 0)} rows to Google Sheets")
        return True
        
    except ImportError:
        logger.warning("google-auth and google-api-python-client not installed")
        logger.info("Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        return False
    except Exception as e:
        logger.error(f"Error uploading to Google Sheets: {e}")
        return False

def main():
    """Main execution function"""
    logger.info("=" * 50)
    logger.info("Real Estate Lead Bot - Starting scrape cycle")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info("=" * 50)
    
    all_listings = []
    errors = []
    
    for city in CITIES:
        try:
            listings = scrape_listings(city)
            all_listings.extend(listings)
        except Exception as e:
            logger.error(f"Error scraping {city['name']}: {e}")
            errors.append(f"{city['name']}: {str(e)}")
    
    if all_listings:
        save_to_csv(all_listings)
        upload_to_google_sheets(all_listings)
    else:
        logger.warning("No listings found")
    
    if errors:
        logger.error(f"Errors encountered: {len(errors)}")
        for error in errors:
            logger.error(f"  - {error}")
    
    logger.info("=" * 50)
    logger.info(f"Scrape cycle complete. Total listings: {len(all_listings)}")
    logger.info("=" * 50)
    
    return len(errors) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)