from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
logging.getLogger().setLevel(logging.CRITICAL)

class LoginlessScraper:
    """
    A class to scrape information from a public Facebook page. It does not require any authentication or API keys.
    
    Attributes
    ----------
    + `page_id` : str
        The Facebook page ID to scrape information from.
    + `driver` : webdriver.Chrome
        The Selenium WebDriver instance.
    + `followers` : str
        The followers count of the Facebook page.
    + `post_texts` : list
        The list of texts from the posts.
    + `post_likes` : list
        The list of likes count for the posts.
    + `post_shares` : list
        The list of shares count for the posts.
    + `is_video` : list
        The list indicating whether the post contains a video.
    + `video_links` : list
        The list of video links if the post contains a video.

    Methods
    -------
    `scrape`(self) -> dict:
        Initiates the scraping process and returns a dictionary with the scraped data.

    Returns
    -------
    [dict]
    A dictionary containing the following:-
    + `followers` (str): 
        The followers count of the Facebook page.
    + `post_texts` (list):
        A list of texts from the posts.
    + `post_likes` (list):
        A list of likes count for the posts.
    + `post_shares` (list):
        A list of shares count for the posts.
    + `is_video` (list):
        A list indicating whether the post contains a video.
    + `video_links` (list):
        A list of video links if the post contains a video.

    Example
    -------
    To scrape a Facebook page:

        ```python
        from MetaDataScraper import LoginlessScraper
        scraper = LoginlessScraper("page_id")
        data = scraper.scrape()

        print(f"Followers: {data['followers']}")
        print(f"Post Texts: {data['post_texts']}")
        print(f"Post Likes: {data['post_likes']}")
        print(f"Post Shares: {data['post_shares']}")
        print(f"Is Video: {data['is_video']}")
        print(f"Video Links: {data['video_links']}")
    """

    def __init__(self, page_id: str):
        """
        Constructs all the necessary attributes for the FacebookScraper object.

        Parameters
        ----------
        page_id : str
            The Facebook page ID to scrape information from.
        
        Example
        -------
        To initialize a LoginlessScraper object:
            scraper = LoginlessScraper("page_id")
        """
        self.page_id = page_id
        self.driver = None
        self.followers = None
        self.post_texts = []
        self.post_likes = []
        self.post_shares = []
        self.is_video = []
        self.video_links = []

    def __setup_driver(self):
        """Sets up the Selenium WebDriver with necessary options."""
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        self.driver = webdriver.Chrome(service=service, options=options)

    def __navigate_to_page(self):
        """Navigates to the specified Facebook page."""
        url = f"https://www.facebook.com/{self.page_id}"
        self.driver.get(url)

    def __check_page_accessibility(self):
        """
        Checks if the page is accessible. 
        If not, it quits the driver and raises an exception.
        """
        self.driver.find_element(By.TAG_NAME, "html").send_keys(Keys.TAB)
        self.driver.find_element(By.TAG_NAME, "html").send_keys(Keys.SHIFT + Keys.TAB)
        self.driver.switch_to.active_element.click()

        if "This content isn't available at the moment" in self.driver.find_element(By.TAG_NAME, "body").get_attribute("innerText"):
            self.driver.quit()
            raise Exception("Page is inaccessible. Try the script with login.")

    def __extract_followers_count(self):
        """Extracts the followers count from the Facebook page."""
        for i in range(25):
            followers = self.driver.execute_script(f"return document.getElementsByTagName('a')[{i}].innerText")
            if 'followers' in followers:
                self.followers = followers
                break
        time.sleep(2)

    def __scroll_to_top(self):
        """Scrolls to the top of the page to ensure proper loading of elements."""
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)

    def __get_xpath_constructor(self):
        """Constructs the XPath for locating posts on the Facebook page."""
        _xpath_return_script = r"""
        var iterator = document.evaluate('.//*[starts-with(@aria-label, "Like")]', document);
        var firstelement = iterator.iterateNext()
        var firstpost = firstelement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement

        function getXPath(element) {
            let selector = '';
            let foundRoot;
            let currentElement = element;
            do {
                const tagName = currentElement.tagName.toLowerCase();
                const parentElement = currentElement.parentElement;
                if (parentElement.childElementCount > 1) {
                    const parentsChildren = [...parentElement.children];
                    let tag = [];
                    parentsChildren.forEach(child => {if (child.tagName.toLowerCase() === tagName) tag.push(child)})
                    if (tag.length === 1) selector = `/${tagName}${selector}`;
                    else {
                        const position = tag.indexOf(currentElement) + 1;
                        selector = `/${tagName}[${position}]${selector}`;
                    }
                } 
                else selector = `/${tagName}${selector}`;
                currentElement = parentElement;
                foundRoot = parentElement.tagName.toLowerCase() === 'html';
                if(foundRoot) selector = `/html${selector}`;
            }
            while (foundRoot === false);
            return selector;
        }
        xpath_first = getXPath(firstpost)
        if(!xpath_first.contains('1]/div/div/div/div/div/div/div/div/div/div/div')) {
            firstelement = iterator.iterateNext();
            var firstpost = firstelement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement
            xpath_first = getXPath(firstpost);
        }
        return xpath_first
        """
        _xpath_constructor = self.driver.execute_script(_xpath_return_script)
        _split_xpath = _xpath_constructor.split('[')
        _split_index = _split_xpath.index('1]/div/div/div/div/div/div/div/div/div/div/div')

        self._xpath_first = '['.join(_split_xpath[:_split_index])+'['
        self._xpath_last = '['+'['.join(_split_xpath[_split_index+1:])
        self._xpath_identifier_addum = ']/div/div/div/div/div/div/div/div/div/div/div'

    def __extract_post_details(self):
        """Extracts details of posts including text, likes, shares, and video links."""
        _c = 1
        _error_count = 0
        while True:
            _xpath = self._xpath_first+str(c)+self._xpath_identifier_addum+self._xpath_last
            if not self.driver.find_elements(By.XPATH, _xpath):
                _error_count += 1
                if _error_count < 3:
                    print('Error extracting post', _c, '\b. Retrying extraction...', end='\r')
                    time.sleep(5)
                    self.driver.execute_script("window.scrollBy(0, +20);")
                    continue
                break
            _error_count = 0
            # Scroll until the post is visible
            self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_elements(By.XPATH, _xpath)[0])
            if not self.driver.find_elements(By.XPATH, _xpath):
                _error_count += 1
                if _error_count < 3:
                    print('Error extracting post', _c, '\b. Retrying extraction...', end='\r')
                    time.sleep(5)
                    self.driver.execute_script("window.scrollBy(0, +20);")
                    continue
                break
            _error_count = 0
            print(" "*100, end='\r')
            print('Extracting post', _c, end='\r')
            _post_components = self.driver.find_element(By.XPATH, _xpath).find_elements(By.XPATH, './*')
            if len(_post_components) > 2:
                _post_text = '\n'.join(_post_components[2].text.split('\n'))
                if _post_components[3].text.split('\n')[0]=='All reactions:':
                    _post_like = _post_components[3].text.split('\n')[1]
                    if len(_post_components[3].text.split('\n'))>4:
                        _post_share = _post_components[3].text.split('\n')[3].split(' ')[0]
                elif len(_post_components)>4 and _post_components[4].text.split('\n')[0]=='All reactions:':
                    _post_like = _post_components[4].text.split('\n')[1]
                    _post_share = _post_components[4].text.split('\n')[4].split(' ')[0]
                else:
                    _post_like = 0
                    _post_share = 0
                self.post_texts.append(_post_text)
                self.post_likes.append(_post_like)
                self.post_shares.append(_post_share)
            else:
                try:
                    _post_share = _post_components[1].find_element(By.XPATH, './/*[@aria-label="Share"]').text
                except:
                    _c+=1
                    continue
                _post_like = _post_components[1].find_element(By.XPATH, './/*[@aria-label="Like"]').text
                _post_share = _post_components[1].find_element(By.XPATH, './/*[@aria-label="Share"]').text
                time.sleep(1)
                self.post_texts.append('')
                self.post_likes.append(_post_like)
                self.post_shares.append(_post_share)
            if len(self.driver.find_elements(By.XPATH, _xpath)[0].find_elements(By.TAG_NAME, 'video')) > 0:
                if 'reels' in self.driver.find_elements(By.XPATH, _xpath)[0].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href'):
                    self.video_links.append('https://www.facebook.com'+self.driver.find_elements(By.XPATH, _xpath)[0].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href'))
                else:
                    self.video_links.append(self.driver.find_elements(By.XPATH, _xpath)[0].find_elements(By.TAG_NAME, 'a')[4].get_attribute('href'))
                self.is_video.append(True)
            else:
                self.is_video.append(False)
                self.video_links.append('')
            _c += 1

        self.post_likes = [int(i) if str(i).isdigit() else 0 for i in self.post_likes]
        self.post_shares = [int(i) if str(i).isdigit() else 0 for i in self.post_shares]

    def scrape(self) -> dict:
        """
        Initiates the scraping process.

        This method automates the extraction of followers count and post details from a public Facebook page.
        It returns a dictionary containing the scraped data.

        Returns
        -------
        dict
            A dictionary containing the following keys:
                + 'followers': str
                    The followers count of the Facebook page.
                + 'post_texts': list
                    A list of texts from the posts.
                + 'post_likes': list
                    A list of likes count for the posts.
                + 'post_shares': list
                    A list of shares count for the posts.
                + 'is_video': list
                    A list indicating whether the post contains a video.
                + 'video_links': list
                    A list of video links if the post contains a video.

        Example
        -------
        To scrape a Facebook page:
            scraper = LoginlessScraper("page_id")

            data = scraper.scrape()
            
            print(f"Followers: {data['followers']}")
            print(f"Post Texts: {data['post_texts']}")
            print(f"Post Likes: {data['post_likes']}")
            print(f"Post Shares: {data['post_shares']}")
            print(f"Is Video: {data['is_video']}")
            print(f"Video Links: {data['video_links']}")
        """
        try:
            self.__setup_driver()
            self.__navigate_to_page()
            self.__check_page_accessibility()
            self.__extract_followers_count()
            self.__scroll_to_top()
            self.__get_xpath_constructor()
            self.__extract_post_details()
            print("\033[A\033[A\033[A") # DevTools line deleter
            return {
                'followers': self.followers,
                'post_texts': self.post_texts,
                'post_likes': self.post_likes,
                'post_shares': self.post_shares,
                'is_video': self.is_video,
                'video_links': self.video_links
            }
        finally:
            if self.driver:
                self.driver.quit()

class LoggedInScraper:
    """
    A class to scrape information from a public Facebook page. Handles the drawbacks of Loginless scraper, since some pages aren't 
    accessible without authentication. It requires authentication to scrape information from private pages.
    
    Attributes
    ----------
    + `page_id` : str
        The Facebook page ID to scrape information from.
    + `email` : str
        The email address associated with the Facebook account.
    + `password` : str
        The password of the Facebook account.
    + `driver` : webdriver.Chrome
        The Selenium WebDriver instance.
    + `followers` : str
        The followers count of the Facebook page.
    + `post_texts` : list
        The list of texts from the posts.
    + `post_likes` : list
        The list of likes count for the posts.
    + `post_shares` : list
        The list of shares count for the posts.
    + `is_video` : list
        The list indicating whether the post contains a video.
    + `video_links` : list
        The list of video links if the post contains a video.

    Methods
    -------
    `scrape`(self) -> dict:
        Initiates the scraping process and returns a dictionary with the scraped data.

    Returns
    -------
    [dict]
    A dictionary containing the following:-
    + `followers` (str): 
        The followers count of the Facebook page.
    + `post_texts` (list):
        A list of texts from the posts.
    + `post_likes` (list):
        A list of likes count for the posts.
    + `post_shares` (list):
        A list of shares count for the posts.
    + `is_video` (list):
        A list indicating whether the post contains a video.
    + `video_links` (list):
        A list of video links if the post contains a video.

    Example
    -------
    To scrape a Facebook page:

        ```python
        from MetaDataScraper import LoggedInScraper
        scraper = LoggedInScraper("page_id", "email", "password")
        data = scraper.scrape()

        print(f"Followers: {data['followers']}")
        print(f"Post Texts: {data['post_texts']}")
        print(f"Post Likes: {data['post_likes']}")
        print(f"Post Shares: {data['post_shares']}")
        print(f"Is Video: {data['is_video']}")
        print(f"Video Links: {data['video_links']}")
    """
    def __init__(self, page_id: str, email: str, password: str):
        """
        Constructs all the necessary attributes for the WithLogin object.

        Parameters
        ----------
        page_id : str
            The Facebook page ID to scrape information from.
        email : str
            The email address used for Facebook login.
        password : str
            The password used for Facebook login.

        Example
        -------
        To initialize a LoggedInScraper object:
            scraper = LoggedInScraper("page_id", "email@example.com", "password")
        """
        self.page_id = page_id
        self.email = email
        self.password = password
        self.driver = None
        self.followers = None
        self.post_texts = []
        self.post_likes = []
        self.post_shares = []
        self.is_video = []
        self.video_links = []

    def __setup_driver(self):
        """Sets up the Selenium WebDriver with necessary options."""
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        self.driver = webdriver.Chrome(service=service, options=options)

    def __login(self):
        """Logs into Facebook using the provided credentials."""
        logged_in = False
        while not logged_in:
            if self.driver.find_elements(By.ID, 'not_me_link'):
                self.driver.find_element(By.ID, 'not_me_link').click()
            self.driver.get('https://www.facebook.com/login')
            self.driver.find_element(By.NAME, 'email').clear()
            self.driver.find_element(By.NAME, 'email').send_keys(self.email)
            self.driver.find_element(By.NAME, 'pass').clear()
            self.driver.find_element(By.NAME, 'pass').send_keys(self.password)
            self.driver.find_element(By.ID, 'loginbutton').click()
            # Wait until the login process is completed
            WebDriverWait(self.driver, 10).until(EC.url_changes('https://www.facebook.com/login'))
            if self.driver.current_url != 'https://www.facebook.com/?sk=welcome':
                print("Invalid credentials. Please try again.", end='\r')
            else:
                print(" "*100, end='\r')
                logged_in = True

    def __navigate_to_page(self):
        """Navigates to the specified Facebook page."""
        url = f"https://www.facebook.com/{self.page_id}"
        self.driver.get(url)

    def __check_page_accessibility(self):
        """
        Checks if the page is accessible. 
        If not, it quits the driver and raises an exception.
        """
        if "This content isn't available at the moment" in self.driver.find_element(By.TAG_NAME, "body").get_attribute("innerText"):
            self.driver.quit()
            raise Exception("Page is inaccessible. Try the script with login.")

    def __extract_followers_count(self):
        """Extracts the followers count from the Facebook page."""
        for i in range(25):
            followers = self.driver.execute_script(f"return document.getElementsByTagName('a')[{i}].innerText")
            if 'followers' in followers:
                self.followers = followers
                break
        time.sleep(2)

    def __scroll_to_top(self):
        """Scrolls to the top of the page to ensure proper loading of elements."""
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)

    def __get_xpath_constructor(self):
        """Constructs the XPath for locating posts on the Facebook page."""
        xpath_return_script = r"""
            var iterator = document.evaluate('.//*[@aria-label="Like"]', document);
            var firstelement = iterator.iterateNext()
            var firstpost = firstelement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement

            function getXPath(element) {
                let selector = '';
                let foundRoot;
                let currentElement = element;
                do {
                    const tagName = currentElement.tagName.toLowerCase();
                    const parentElement = currentElement.parentElement;
                    if (parentElement.childElementCount > 1) {
                        const parentsChildren = [...parentElement.children];
                        let tag = [];
                        parentsChildren.forEach(child => {if (child.tagName.toLowerCase() === tagName) tag.push(child)})
                        if (tag.length === 1) selector = `/${tagName}${selector}`;
                        else {
                            const position = tag.indexOf(currentElement) + 1;
                            selector = `/${tagName}[${position}]${selector}`;
                        }
                    } 
                    else selector = `/${tagName}${selector}`;
                    currentElement = parentElement;
                    foundRoot = parentElement.tagName.toLowerCase() === 'html';
                    if(foundRoot) selector = `/html${selector}`;
                }
                while (foundRoot === false);
                return selector;
            }
            xpath_first = getXPath(firstpost)
            if(!xpath_first.contains('1]/div/div/div/div/div/div/div/div/div/div/div')) {
                firstelement = iterator.iterateNext();
                firstpost = firstelement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
                xpath_first = getXPath(firstpost);
            }
            return xpath_first
        """
        xpath_constructor = self.driver.execute_script(xpath_return_script)
        split_xpath = xpath_constructor.split('[')
        split_index = split_xpath.index('1]/div/div/div/div/div/div/div/div/div/div/div')
        self.xpath_first = '['.join(split_xpath[:split_index])+'['
        self.xpath_last = '['+'['.join(split_xpath[split_index+1:])
        self.xpath_identifier_addum = ']/div/div/div/div/div/div/div/div/div/div/div'
        if len(self.driver.find_element(By.XPATH, xpath_constructor).find_elements(By.TAG_NAME, 'video')):
            self.xpath_last = '/'.join(self.xpath_last.split('/')[:3])

    def __extract_post_details(self):
        """Extracts details of posts including text, likes, shares, and video links."""
        c = 1
        error_count = 0
        while True:
            xpath = self.xpath_first + str(c) + self.xpath_identifier_addum + self.xpath_last
            if not self.driver.find_elements(By.XPATH, xpath):
                error_count += 1
                if error_count < 3:
                    print('Error extracting post', c, '\b. Count', error_count,'Retrying extraction...', end='\r')
                    time.sleep(5)
                    self.driver.execute_script("window.scrollBy(0, +40);")
                    continue
                break
            error_count = 0
            print(" "*100, end='\r')
            print("Extracting data of post", c, end='\r')
            self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_elements(By.XPATH, xpath)[0])
            post_components = self.driver.find_element(By.XPATH, xpath).find_elements(By.XPATH, './*')
            if len(post_components) > 2:
                post_text = '\n'.join(post_components[2].text.split('\n'))
                if post_components[3].text.split('\n')[0] == 'All reactions:':
                    post_likes = post_components[3].text.split('\n')[1]
                    if len(post_components[3].text.split('\n')) > 4:
                        post_shares = post_components[3].text.split('\n')[4].split(' ')[0]
                elif len(post_components) > 4 and post_components[4].text.split('\n')[0] == 'All reactions:':
                    post_likes = post_components[4].text.split('\n')[1]
                    if len(post_components[4].text.split('\n')) > 4:
                        post_shares = post_components[4].text.split('\n')[4].split(' ')[0]
                else:
                    post_likes = 0
                    post_shares = 0
                self.post_texts.append(post_text)
                self.post_likes.append(post_likes if post_likes else 0)
                self.post_shares.append(post_shares if post_shares else 0)
            elif len(post_components) == 2:
                try:
                    post_shares = post_components[1].find_element(By.XPATH, './/*[@aria-label="Share"]').text
                except:
                    print("Some error occurred while extracting post", c, ". Skipping post...", end='\r')
                    c += 1
                    continue
                post_likes = post_components[1].find_element(By.XPATH, './/*[@aria-label="Like"]').text
                post_shares = post_components[1].find_element(By.XPATH, './/*[@aria-label="Share"]').text
                self.post_texts.append('')
                self.post_likes.append(post_likes if post_likes else 0)
                self.post_shares.append(post_shares if post_shares else 0)
            elif len(post_components) == 1:
                post_text = post_components[0].text.split('\n')[0]
                post_likes = post_components[0].find_element(By.XPATH, './/*[@aria-label="Like"]').text
                post_shares = post_components[0].find_element(By.XPATH, './/*[@aria-label="Share"]').text
                self.post_texts.append(post_text)
                self.post_likes.append(post_likes if post_likes else 0)
                self.post_shares.append(post_shares if post_shares else 0)
            if len(self.driver.find_elements(By.XPATH, xpath)[0].find_elements(By.TAG_NAME, 'video')) > 0:
                if 'reel' in self.driver.find_elements(By.XPATH, xpath)[0].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href'):
                    self.video_links.append('https://www.facebook.com' + self.driver.find_elements(By.XPATH, xpath)[0].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href'))
                else:
                    self.video_links.append(self.driver.find_elements(By.XPATH, xpath)[0].find_elements(By.TAG_NAME, 'a')[4].get_attribute('href'))
                self.is_video.append(True)
            else:
                self.is_video.append(False)
                self.video_links.append('')
            c += 1

        self.post_likes = [int(i) if str(i).isdigit() else 0 for i in self.post_likes]
        self.post_shares = [int(i) if str(i).isdigit() else 0 for i in self.post_shares]

    def scrape(self):
        """Initiates the scraping process and returns a dictionary with the scraped data."""
        self.__setup_driver()
        self.__login()
        self.__navigate_to_page()
        self.__check_page_accessibility()
        self.__extract_followers_count()
        self.__scroll_to_top()
        self.__get_xpath_constructor()
        self.__extract_post_details()
        self.driver.quit()
        print("\033[A\033[A\033[A") # DevTools line deleter
        return {
            'followers': self.followers,
            'post_texts': self.post_texts,
            'post_likes': self.post_likes,
            'post_shares': self.post_shares,
            'is_video': self.is_video,
            'video_links': self.video_links
        }