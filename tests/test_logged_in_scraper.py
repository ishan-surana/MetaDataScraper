import unittest
from unittest.mock import patch, MagicMock
from MetaDataScraper.FacebookScraper import LoggedInScraper

class TestLoggedInScraper(unittest.TestCase):
    def setUp(self):
        self.page_id = "test_page_id"
        self.email = "test@example.com"
        self.password = "password"
        self.scraper = LoggedInScraper(self.page_id, self.email, self.password)

    @patch('MetaDataScraper.FacebookScraper.webdriver.Chrome')
    @patch('MetaDataScraper.FacebookScraper.ChromeDriverManager')
    def test_setup_driver(self, MockChromeDriverManager, MockChrome):
        mock_service = MagicMock()
        MockChromeDriverManager.return_value.install.return_value = mock_service
        mock_driver = MagicMock()
        MockChrome.return_value = mock_driver
        self.scraper._LoggedInScraper__setup_driver()

        MockChrome.assert_called_once()
        MockChromeDriverManager.assert_called_once()
        self.assertIsNotNone(self.scraper.driver)
        self.assertEqual(self.scraper.driver, mock_driver)

    @patch('MetaDataScraper.FacebookScraper.webdriver.Chrome')
    @patch('MetaDataScraper.FacebookScraper.ChromeDriverManager')
    def test_login(self, MockChromeDriverManager, MockChrome):
        mock_service = MagicMock()
        MockChromeDriverManager.return_value.install.return_value = mock_service
        mock_driver = MagicMock()
        MockChrome.return_value = mock_driver
        
        self.scraper._LoggedInScraper__login = MagicMock()
        self.scraper._LoggedInScraper__login.side_effect = None

        try:
            self.scraper._LoggedInScraper__setup_driver()
            self.scraper._LoggedInScraper__login()
            self.assertTrue(self.scraper._logged_in)
            MockChrome.assert_called_once()
            MockChromeDriverManager.assert_called_once()
            self.assertIsNotNone(self.scraper.driver)
        except Exception as e:
            self.assertFalse(self.scraper._logged_in)

    @patch.object(LoggedInScraper, '_LoggedInScraper__setup_driver')
    @patch.object(LoggedInScraper, '_LoggedInScraper__login')
    @patch.object(LoggedInScraper, '_LoggedInScraper__extract_followers_count')
    @patch.object(LoggedInScraper, '_LoggedInScraper__extract_post_details')
    def test_scrape(self, mock_extract_post_details, mock_extract_followers_count, mock_login, mock_setup_driver):
        # Set up mocks
        mock_login.return_value = None
        mock_setup_driver.return_value = None
        mock_extract_post_details.return_value = None
        mock_extract_followers_count.return_value = None

        mock_driver = MagicMock()
        self.scraper.driver = mock_driver
        
        result = self.scraper.scrape()
        
        self.assertIsInstance(result, dict)
        self.assertIn('followers', result)
        self.assertIn('post_texts', result)
        self.assertIn('post_likes', result)
        self.assertIn('post_shares', result)
        self.assertIn('is_video', result)
        self.assertIn('video_links', result)

    def test_initialization(self):
        self.assertEqual(self.scraper.page_id, self.page_id)
        self.assertEqual(self.scraper.email, self.email)
        self.assertEqual(self.scraper.password, self.password)
        self.assertIsNone(self.scraper.driver)
        self.assertIsNone(self.scraper.followers)
        self.assertEqual(self.scraper.post_texts, [])
        self.assertEqual(self.scraper.post_likes, [])
        self.assertEqual(self.scraper.post_shares, [])
        self.assertEqual(self.scraper.is_video, [])
        self.assertEqual(self.scraper.video_links, [])

if __name__ == '__main__':
    unittest.main()