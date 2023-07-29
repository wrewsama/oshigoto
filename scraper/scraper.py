from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from abc import ABC, abstractmethod
from time import sleep

# TODO: set up method to change the country
class Scraper(ABC):

    @abstractmethod
    def __init__(self, options: Options, service: Service):
        self.driver
        self.listings

    @abstractmethod
    def _getListings(self):
        pass

    @abstractmethod
    def setLocation(self, location: str):
        pass

    @abstractmethod
    def search(self, query: str):
        pass

    @abstractmethod
    def getBasicInfo(self):
        pass

    @abstractmethod
    def getJobPoints(self):
        pass

class NodeFlairScraper(Scraper):
    def __init__(self, options: Options, service: Service):
        self.driver = webdriver.Chrome(service=service,
                                options=options)
        self.driver.set_window_size(1280, 720)
        self.driver.get("https://nodeflair.com/jobs")
        self.driver.implicitly_wait(10)
        self.listings = self._getListings()

        self.VALID_COUNTRIES = {'Singapore', 'Malaysia', 'Phillipines', 'Indonesia', 'Vietnam', 'Thailand', 'Taiwan', 'India'}

    def _getListings(self):
        return self.driver.find_elements(By.XPATH, "//div[@class='jobListingCard-0-3-69 ']")
    
    def setLocation(self, location: str):
        if location.title() not in self.VALID_COUNTRIES:
            return 
        self.driver.get(f"https://nodeflair.com/jobs?query=&page=1&sort_by=relevant&countries%5B%5D={location.title()}")
    
    def search(self, query:str):
        print(f'[INFO] search started with {query}')
        searchbar = self.driver.find_element(By.XPATH, "//input[@class='react-autosuggest__input']")
        searchbar.send_keys(query)
        searchbar.send_keys(Keys.RETURN)

        self.listings = self._getListings()

    def getBasicInfo(self):
        res = []
        for listing in self.listings:
            title = listing.find_element(By.XPATH, ".//h2[@class='jobListingCardTitle-0-3-72']").text
            company = listing.find_element(By.XPATH, ".//p[@class='companynameAndRating-0-3-82']/span[1]").text
            link = listing.find_element(By.XPATH, "./a").get_attribute("href")
            res.append({
                "title": title,
                "company": company,
                "link": link
            })
        
        return res

    def getJobPoints(self):
        res = []
        def getCurrJobPoints():
            pts = self.driver.find_elements(By.XPATH, "//div[@class='jobDescriptionContent-0-3-110']//li")
            return list(map(lambda x: x.text, pts))

        for listing in self.listings:
            listing.click()
            res.extend(getCurrJobPoints())

        return res

class LinkedinScraper(Scraper):
    def __init__(self, options: Options, service: Service):
        self.driver = webdriver.Chrome(service=service,
                                options=options)
        self.driver.set_window_size(1280, 720)
        self.driver.get("https://www.linkedin.com/jobs/search")
        self.driver.implicitly_wait(10)
        self.listings = self._getListings()

    def _getListings(self):
        activeListing = self.driver.find_element(By.XPATH, "//div[@class='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card job-search-card--active']")
        otherListings = self.driver.find_elements(By.XPATH, "//div[@class='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card']")
        return [activeListing, *otherListings]


    def setLocation(self, location: str):
        countrySearchBar = self.driver.find_element(By.XPATH, "//input[@id='job-search-bar-location']")
        for _ in range(13):
            countrySearchBar.send_keys(Keys.BACKSPACE)
        countrySearchBar.send_keys(location)

    
    def search(self, query:str):
        searchBar = self.driver.find_element(By.XPATH, "//input[@id='job-search-bar-keywords']")
        searchBar.send_keys(query) 
        searchBar.send_keys(Keys.RETURN)
        self.listings = self._getListings()

    def getBasicInfo(self):
        res = []
        for listing in self.listings:
            title = listing.find_element(By.XPATH, ".//h3[@class='base-search-card__title']").text
            company = listing.find_element(By.XPATH, ".//h4[@class='base-search-card__subtitle']").text 
            link = listing.find_element(By.XPATH, "./a").get_attribute("href")
            res.append({
                "title": title,
                "company": company,
                "link": link
            })
        return res

    def getJobPoints(self):
        # linkedin blocks headless browsers / non logged in users from accessing JDs
        return []

class GlintsScraper(Scraper):
    def __init__(self, options: Options, service: Service):
        self.driver = webdriver.Chrome(service=service,
                                options=options)
        self.driver.set_window_size(1280, 720)
        self.driver.get("https://glints.com/sg/opportunities/jobs/explore?country=SG&locationName=All+Cities%2FProvinces&keyword=intern")
        self.driver.implicitly_wait(10)
        self.listings = self._getListings()

        self.VALID_COUNTRIES = {'Singapore',
                                'Malaysia',
                                'Phillipines',
                                'Indonesia',
                                'Vietnam',
                                'Thailand',
                                'Taiwan',
                                'India',
                                'Hong Kong',
                                'China',
                                'Japan',
                                'Australia',
                                'United States'}

    def _getListings(self):
        pass

    def setLocation(self, location: str):
        if location not in self.VALID_COUNTRIES:
            return

        countryInput = self.driver.find_element(By.XPATH, "//div[@class='SelectStyle__SelectWrapper-sc-gv8n2w-1 driwsF select-inputwrapper']")
        countryInput.click()
        countrySelect = self.driver.find_element(By.XPATH, "//ul[@class='SelectStyle__SelectListWrapper-sc-gv8n2w-4 hNAXQP select-listbox']")
        selectedCountry = countrySelect.find_element(By.XPATH, f".//li[contains(text(), '{location}')]")
        selectedCountry.click()
    
    def search(self, query:str):
        url = self.driver.current_url
        currSearchQueryIdx = url.index('&keyword=') + len('&keyword=')
        self.driver.get(url[:currSearchQueryIdx] + query)

    def getBasicInfo(self):
        res = []
        for listing in self.listings:
            continue
        return res

    def getJobPoints(self):
        pass