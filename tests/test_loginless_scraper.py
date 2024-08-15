import unittest
from unittest.mock import patch, MagicMock
from MetaDataScraper.FacebookScraper import LoginlessScraper

class TestLoginlessScraper(unittest.TestCase):
    def setUp(self):
        self.page_id = "test_page_id"
        self.scraper = LoginlessScraper(self.page_id)

    @patch.object(LoginlessScraper, '_LoginlessScraper__setup_driver')
    @patch.object(LoginlessScraper, '_LoginlessScraper__navigate_to_page')
    @patch.object(LoginlessScraper, '_LoginlessScraper__check_page_accessibility')
    @patch.object(LoginlessScraper, '_LoginlessScraper__extract_followers_count')
    @patch.object(LoginlessScraper, '_LoginlessScraper__scroll_to_top')
    @patch.object(LoginlessScraper, '_LoginlessScraper__get_xpath_constructor')
    @patch.object(LoginlessScraper, '_LoginlessScraper__extract_post_details')
    def test_scrape(self, mock_extract_post_details, mock_get_xpath, mock_scroll, mock_extract_followers, mock_check_access, mock_navigate, mock_setup):
        mock_extract_post_details.return_value = None
        mock_get_xpath.return_value = None
        mock_scroll.return_value = None
        mock_extract_followers.return_value = None
        mock_check_access.return_value = None
        mock_navigate.return_value = None
        mock_setup.return_value = None

        result = self.scraper.scrape()

        self.assertIsInstance(result, dict)
        self.assertIn('followers', result)
        self.assertIn('post_texts', result)
        self.assertIn('post_likes', result)
        self.assertIn('post_shares', result)
        self.assertIn('is_video', result)
        self.assertIn('video_links', result)

    @patch('MetaDataScraper.FacebookScraper.webdriver.Chrome')
    @patch('MetaDataScraper.FacebookScraper.ChromeDriverManager')
    def test_setup_driver(self, MockChromeDriverManager, MockChrome):
        mock_service = MagicMock()
        MockChromeDriverManager.return_value.install.return_value = mock_service
        self.scraper._LoginlessScraper__setup_driver()

        MockChrome.assert_called_once()
        MockChromeDriverManager.assert_called_once()
        self.assertIsNotNone(self.scraper.driver)

    def test_initialization(self):
        self.assertEqual(self.scraper.page_id, self.page_id)
        self.assertIsNone(self.scraper.driver)
        self.assertIsNone(self.scraper.followers)
        self.assertEqual(self.scraper.post_texts, [])
        self.assertEqual(self.scraper.post_likes, [])
        self.assertEqual(self.scraper.post_shares, [])
        self.assertEqual(self.scraper.is_video, [])
        self.assertEqual(self.scraper.video_links, [])

if __name__ == '__main__':
    unittest.main()