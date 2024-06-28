# MetaDataScraper

MetaDataScraper is a Python package designed to automate the extraction of information like follower counts, and post details & interactions from a public Facebook page, in the form of a FacebookScraper object. It uses Selenium WebDriver for web automation and scraping.

## Installation

You can install MetaDataScraper using pip:

```
pip install MetaDataScraper
```

Make sure you have Python 3.x and pip installed.

## Usage

To use MetaDataScraper, follow these steps:

1. Import the FacebookScraper class:

   ```python
   from MetaDataScraper import FacebookScraper
   ```

2. Initialize the scraper with the Facebook page ID:

   ```python
   scraper = FacebookScraper("page_id")
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

- **Scraping:** Extracts followers count and post details (text, likes, shares, video links) from Facebook pages.
- **Flexibility:** Handles various post structures and video formats on Facebook pages.
- **Headless Mode:** Runs in headless mode for silent scraping without UI interference.

## Dependencies

- selenium
- webdriver_manager

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.