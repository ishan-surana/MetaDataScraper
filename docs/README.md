# MetaDataScraper

MetaDataScraper is a Python package designed to automate the extraction of information like follower counts, and post details & interactions from a public Facebook page, in the form of a list. It uses Selenium WebDriver for web automation and scraping.  
The module provides two classes: `LoginlessScraper` and `LoggedInScraper`. The `LoginlessScraper` class does not require any authentication or API keys to scrape the data. However, it has a drawback of being unable to access some Facebook pages. 
The `LoggedInScraper` class overcomes this drawback by utilising the credentials of a Facebook account (of user) to login and scrape the data.

## Installation

You can install MetaDataScraper using pip:

```
pip install MetaDataScraper
```

Make sure you have Python 3.x and pip installed.

## Usage

To use MetaDataScraper, follow these steps:

1. Import the `LoginlessScraper` or the `LoggedInScraper` class:

   ```python
   from MetaDataScraper import LoginlessScraper, LoggedInScraper
   ```

2. Initialize the scraper with the Facebook page ID:

   ```python
   page_id = "your_target_page_id"
   scraper = LoginlessScraper(page_id)
   email = "your_facebook_email"
   password = "your_facebook_password"
   scraper = LoggedInScraper(page_id, email, password)
   ```

3. Scrape the Facebook page to retrieve information:

   ```python
   result = scraper.scrape()
   ```

4. Access the scraped data from the result dictionary:

   ```python
   print(f"Followers: {result['followers']}")
   print(f"Post Texts: {result['post_texts']}")
   print(f"Post Likes: {result['post_likes']}")
   print(f"Post Shares: {result['post_shares']}")
   print(f"Is Video: {result['is_video']}")
   print(f"Video Links: {result['video_links']}")
   ```

## Features

- **Automated Extraction**: Automatically fetches follower counts, post texts, likes, shares, and video links from Facebook pages.
- **Comprehensive Data Retrieval**: Retrieves detailed information about each post, including text content, interaction metrics (likes, shares), and multimedia (e.g., video links).
- **Flexible Handling**: Adapts to diverse post structures and various types of multimedia content present on Facebook pages, like post texts or reels.
- **Enhanced Access with Logged-In Scraper**: Overcomes limitations faced by anonymous scraping (loginless) by utilizing Facebook account credentials for broader page access.
- **Headless Operation**: Executes scraping tasks in headless mode, ensuring seamless and non-intrusive data collection without displaying a browser interface.
- **Scalability**: Supports scaling to handle large volumes of data extraction efficiently, suitable for monitoring multiple Facebook pages simultaneously.
- **Dependency Management**: Utilizes Selenium WebDriver for robust web automation and scraping capabilities, compatible with Python 3.x environments.
- **Ease of Use**: Simplifies the process with straightforward initialization and method calls, facilitating quick integration into existing workflows.

## Dependencies

- selenium
- webdriver_manager

## License

This project is licensed under the Apache Software License Version 2.0 - see the [LICENSE](https://github.com/ishan-surana/MetaDataScraper/blob/main/LICENCE) file for details.