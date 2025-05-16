# fetch_data.py
import requests
import os
import dotenv
import time
import logging

dotenv.load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

NASHEEDIO_BEARER_TOKEN = os.environ.get("NASHEEDIO_BEARER_TOKEN")

# Set up headers with the Bearer token
headers = {
    "Authorization": f"Bearer {NASHEEDIO_BEARER_TOKEN}"
}

def fetch_paginated_data(base_url):
    """
    Fetches all paginated data from a given API endpoint.

    Parameters:
    - base_url (str): The API endpoint URL.

    Returns:
    - list: A list of all collected data items.
    """
    collected_data = []
    
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Raise error for bad status codes

        first_page_data = response.json()

        if isinstance(first_page_data, list):  
            # Handle case where API returns a list directly
            logging.info(f"Total records collected: {len(first_page_data)}")
            return first_page_data  
        
        elif isinstance(first_page_data, dict):  
            # Safely extract pagination details
            total_pages = first_page_data.get("meta", {}).get("pagination", {}).get("pageCount", 1)
            total_records = first_page_data.get("meta", {}).get("pagination", {}).get("total", 1)
            collected_data.extend(first_page_data.get("data", []))  # Add first page data
            
            logging.info(f"Total pages: {total_pages} | Total records: {total_records}")

            pagination_symbol = "&" if "?" in base_url else "?"

            for page in range(2, total_pages + 1):
                try:
                    url = f"{base_url}{pagination_symbol}pagination[page]={page}"
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()

                    data = response.json()
                    collected_data.extend(data.get("data", []))

                    logging.info(f"Page {page} processed successfully.")

                    time.sleep(1)  # Prevent API rate limits
                except requests.RequestException as e:
                    logging.error(f"Error fetching page {page}: {e}")
                    continue  # Skip to the next page

            logging.info(f"Total records collected: {len(collected_data)}")
            return collected_data

    except requests.RequestException as e:
        logging.error(f"Error fetching the first page: {e}")
        return []
    
