from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from abc import ABC, abstractmethod

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
        self.driver.get("https://nodeflair.com/jobs?countries%5B%5D=Singapore")
        self.driver.implicitly_wait(10)
        self.listings = self._getListings()

    def _getListings(self):
        return self.driver.find_elements(By.XPATH, "//div[@class='jobListingCard-0-3-69 ']")
    
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
        self.driver.get("https://www.linkedin.com/jobs/search/")
        self.driver.implicitly_wait(10)
        self._changeCountry()
        self.listings = self._getListings()
    
    def _changeCountry(self):
        countrySearchBar = self.driver.find_element(By.XPATH, "//input[@id='job-search-bar-location']")
        for _ in range(13):
            countrySearchBar.send_keys(Keys.BACKSPACE)
        countrySearchBar.send_keys('Singapore')

    def _getListings(self):
        return self.driver.find_elements(By.XPATH, "//a[@class='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]']")
    
    def search(self, query:str):
        searchBar = self.driver.find_element(By.XPATH, "//input[@id='job-search-bar-keywords']")
        searchBar.send_keys(query) 
        searchBar.send_keys(Keys.RETURN)
        self.listings = self._getListings()

    def getBasicInfo(self):
        pass

    def getJobPoints(self):
        pass