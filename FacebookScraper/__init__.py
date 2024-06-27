"""
FacebookScraper Module
----------------------

This module provides a script `FacebookScraper` to scrape information from a public Facebook page.

Overview:
---------
The `FacebookScraper` module is designed to automate the extraction of follower counts and post details
from a public Facebook page. It uses Selenium WebDriver for web automation and scraping.

Classes:
--------
FacebookScraper
    A class to scrape followers count and post details from a public Facebook page.

Methods:
------------------------
scrape(self) -> dict:
    Initiates the scraping process and returns a dictionary with the scraped data.

Requirements:
-------------
- selenium
- webdriver_manager

Usage:
------
    from FacebookScraper import FacebookScraper

    page_id = "your_facebook_page_id"

    scraper = FacebookScraper(page_id)

    result = scraper.scrape()

    print(f"Followers: {result['followers']}")
    print(f"Post Texts: {result['post_texts']}")
    print(f"Post Likes: {result['post_likes']}")
    print(f"Post Shares: {result['post_shares']}")
    print(f"Is Video: {result['is_video']}")
    print(f"Video Links: {result['video_links']}")
"""

from .FacebookScraper import FacebookScraper

__all__ = ["FacebookScraper"]