from dotenv import load_dotenv
import os
from serpapi import GoogleSearch
from google_play_scraper import search

load_dotenv()

def fetch_google_play_reviews(app_name):
    api_key = os.getenv("SerpAPI_Key")
    search_results = search(app_name)

    try:
        product_id = search_results[0]["appId"]
    except (IndexError, KeyError):
        raise ValueError("Could not find the specified app.")

    params = {
        "engine": "google_play_product",
        "product_id": product_id,
        "store": "apps",
        "api_key": api_key,
        "num": 100,
        "all_reviews": True,
        "sort_by": 2
    }

    serpapi_search = GoogleSearch(params)
    results = serpapi_search.get_dict()

    return results
