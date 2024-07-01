Welcome to the MetaDataScraper documentation!
===================================

MetaDataScraper is a Python package designed to automate the extraction of information like follower counts, and post details & interactions from a public Facebook page, in the form of a list. It uses Selenium WebDriver for web automation and scraping.  
The module provides two classes: `LoginlessScraper` and `LoggedInScraper`. The `LoginlessScraper` class does not require any authentication or API keys to scrape the data. However, it has a drawback of being unable to access some Facebook pages. 
The `LoggedInScraper` class overcomes this drawback by utilising the credentials of a Facebook account (of user) to login and scrape the data.

.. note::

   This project is under active development.

Contents
--------

.. toctree::

   README
