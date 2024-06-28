"""
MetaDataScraper Module
----------------------

This module provides a script `MetaDataScraper` to scrape information from a public Facebook page. It can extract the follower count and post details & interactions from a Facebook page. 
The module provides two classes: `LoginlessScraper` and `LoggedInScraper`. The `LoginlessScraper` class does not require any authentication or API keys to scrape the data. However, it has a drawback of being unable to access some Facebook pages. 
The `LoggedInScraper` class overcomes this drawback by utilising the credentials of a Facebook account (of user) to login and scrape the data.

Overview:
---------
The `MetaDataScraper` module is designed to automate the extraction of follower counts and post details from a public Facebook page. It provides two classes: `LoginlessScraper` and `LoggedInScraper`. 
The `LoginlessScraper` class does not require any authentication or API keys to scrape the data. However, it has a drawback of being unable to access some Facebook pages. 
The `LoggedInScraper` class overcomes this drawback by requiring the credentials of a Facebook account to login and scrape the data. The module uses Selenium WebDriver for web automation and scraping.

Classes:
--------
1) `LoginlessScraper`:
    A class to scrape followers count and post details from a public Facebook page. It does not require any authentication or API keys.
2) `LoggedInScraper`:
    A class to scrape followers count and post details from a public Facebook page. It handles the drawback of the LoginlessScraper involving the inaccessibility of some Facebook pages.
    It requires credentials of a Facebook account to login and scrape the data.

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
#### 1) LoginlessScraper:
    ```python
    from MetaDataScraper import LoginlessScraper
    page_id = "your_target_page_id"
    scraper = LoginlessScraper(page_id)
    data = scraper.scrape()
    
    print(f"Followers: {data['followers']}")
    print(f"Post Texts: {data['post_texts']}")
    print(f"Post Likes: {data['post_likes']}")
    print(f"Post Shares: {data['post_shares']}")
    print(f"Is Video: {data['is_video']}")
    print(f"Video Links: {data['video_links']}")
    ```
#### 2) LoggedInScraper:
    ```python
    from MetaDataScraper import LoggedInScraper
    page_id = "your_target_page_id"
    email = "your_facebook_email"
    password = "your_facebook_password"
    scraper = LoggedInScraper(page_id, email, password)
    data = scraper.scrape()

    print(f"Followers: {data['followers']}")
    print(f"Post Texts: {data['post_texts']}")
    print(f"Post Likes: {data['post_likes']}")
    print(f"Post Shares: {data['post_shares']}")
    print(f"Is Video: {data['is_video']}")
    print(f"Video Links: {data['video_links']}")

"""

from .FacebookScraper import LoggedInScraper, LoginlessScraper

__all__ = ["LoggedInScraper", "LoginlessScraper"]