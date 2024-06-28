"""
MetaDataScraper Module
----------------------

This module provides a script `MetaDataScraper` to scrape information from a public Facebook page.

Overview:
---------
The `MetaDataScraper` module is designed to automate the extraction of follower counts and post details
from a public Facebook page. It uses Selenium WebDriver for web automation and scraping.

Classes:
--------
+ FacebookScraper
    A class to scrape followers count and post details from a public Facebook page. It does not require any authentication or API keys.

Methods:
------------------------
+ scrape(self) -> dict:
    Initiates the scraping process and returns a dictionary with the scraped data.

Requirements:
-------------
- selenium
- webdriver_manager

Usage:
------

    ```python
    from MetaDataScraper import FacebookScraper
    scraper = FacebookScraper("page_id")
    data = scraper.scrape()
    
    print(f"Followers: {data['followers']}")
    print(f"Post Texts: {data['post_texts']}")
    print(f"Post Likes: {data['post_likes']}")
    print(f"Post Shares: {data['post_shares']}")
    print(f"Is Video: {data['is_video']}")
    print(f"Video Links: {data['video_links']}")
"""

from .FacebookScraper import FacebookScraper

__all__ = ["FacebookScraper"]